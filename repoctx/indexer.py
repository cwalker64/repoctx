"""Turn a set of source files into searchable indexes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .chunking.registry import chunk_file
from .config import Config
from .embeddings.base import Embedder
from .embeddings.hashing import HashingEmbedder
from .index.vector_index import VectorIndex
from .types import Chunk
from .walk import iter_files


@dataclass
class IndexResult:
    """Everything produced by a single indexing pass."""

    chunks: list[Chunk]
    vector_index: VectorIndex
    chunks_by_id: dict[str, Chunk] = field(default_factory=dict)


class Indexer:
    """Chunk, embed and index a repository."""

    def __init__(self, config: Optional[Config] = None, embedder: Optional[Embedder] = None) -> None:
        self.config = config or Config()
        self.embedder = embedder or HashingEmbedder(dim=self.config.embedding_dim)

    def index_files(self, files: dict[str, str]) -> IndexResult:
        chunks: list[Chunk] = []
        for path, source in sorted(files.items()):
            chunks.extend(chunk_file(path, source))

        vector_index = VectorIndex(self.embedder.dim)
        if chunks:
            vectors = self.embedder.embed([c.text for c in chunks])
            vector_index.add([c.id for c in chunks], vectors)

        chunks_by_id = {c.id: c for c in chunks}
        return IndexResult(
            chunks=chunks,
            vector_index=vector_index,
            chunks_by_id=chunks_by_id,
        )

    def index_path(self, root: str | Path) -> IndexResult:
        root_path = Path(root)
        files: dict[str, str] = {}
        for file_path in iter_files(
            root_path, include_ext=self.config.include_ext, extra_globs=self.config.extra_ignore
        ):
            rel = str(file_path.relative_to(root_path))
            files[rel] = file_path.read_text(encoding="utf-8", errors="ignore")
        return self.index_files(files)


__all__ = ["Indexer", "IndexResult"]
