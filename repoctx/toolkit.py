"""High-level facade tying indexing, search and context together."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .config import Config
from .embeddings.base import Embedder
from .embeddings.hashing import HashingEmbedder
from .graph.context import ContextBuilder, ContextPack
from .graph.graph import CodeGraph
from .index.bm25 import BM25Index
from .index.store import load_snapshot, save_snapshot
from .indexer import IndexResult, Indexer, _symbol_chunk_map
from .retrieval.search import HybridSearcher
from .types import Chunk, SearchHit


class Repoctx:
    """The one object most users need.

    Build one with :meth:`index` (a directory) or :meth:`from_files` (an
    in-memory mapping), then call :meth:`search` and :meth:`context`.
    """

    def __init__(self, result: IndexResult, embedder: Embedder, config: Config) -> None:
        assert result.bm25 is not None and result.graph is not None
        self._result = result
        self.embedder = embedder
        self.config = config
        self._searcher = HybridSearcher(
            embedder, result.vector_index, result.bm25, result.chunks_by_id
        )
        self._context = ContextBuilder(result.graph, result.symbol_chunks)

    @classmethod
    def index(
        cls,
        root: str | Path,
        config: Optional[Config] = None,
        embedder: Optional[Embedder] = None,
    ) -> Repoctx:
        config = config or Config()
        embedder = embedder or HashingEmbedder(dim=config.embedding_dim)
        result = Indexer(config=config, embedder=embedder).index_path(root)
        return cls(result, embedder, config)

    @classmethod
    def from_files(
        cls,
        files: dict[str, str],
        config: Optional[Config] = None,
        embedder: Optional[Embedder] = None,
    ) -> Repoctx:
        config = config or Config()
        embedder = embedder or HashingEmbedder(dim=config.embedding_dim)
        result = Indexer(config=config, embedder=embedder).index_files(files)
        return cls(result, embedder, config)

    def search(self, query: str, k: int = 10, alpha: Optional[float] = None) -> list[SearchHit]:
        weight = self.config.alpha if alpha is None else alpha
        return self._searcher.search(query, k=k, alpha=weight)

    def context(self, target: str, depth: int = 1) -> ContextPack:
        return self._context.build(target, depth=depth)

    @property
    def graph(self) -> CodeGraph:
        assert self._result.graph is not None
        return self._result.graph

    @property
    def chunks(self) -> list[Chunk]:
        return self._result.chunks

    def save(self, path: str | Path) -> None:
        """Persist the index to *path* for later :meth:`load`."""
        assert self._result.graph is not None
        save_snapshot(
            path,
            chunks=self._result.chunks,
            vector_index=self._result.vector_index,
            graph=self._result.graph,
            embedder_name=self.embedder.name,
            config=self.config.to_dict(),
        )

    @classmethod
    def load(
        cls,
        path: str | Path,
        config: Optional[Config] = None,
        embedder: Optional[Embedder] = None,
    ) -> Repoctx:
        data = load_snapshot(path)
        config = config or Config()
        vector_index = data["vector_index"]
        embedder = embedder or HashingEmbedder(dim=vector_index.dim)
        chunks: list[Chunk] = data["chunks"]
        bm25 = BM25Index(k1=config.bm25_k1, b=config.bm25_b)
        bm25.index([c.id for c in chunks], [c.text for c in chunks])
        result = IndexResult(
            chunks=chunks,
            vector_index=vector_index,
            chunks_by_id={c.id: c for c in chunks},
            bm25=bm25,
            graph=data["graph"],
            symbol_chunks=_symbol_chunk_map(chunks),
        )
        return cls(result, embedder, config)
