"""Hybrid retrieval: fuse dense (embedding) and lexical (BM25) rankings."""

from __future__ import annotations

from typing import Mapping

from ..embeddings.base import Embedder
from ..index.bm25 import BM25Index
from ..index.vector_index import VectorIndex
from ..types import Chunk, SearchHit
from .fusion import reciprocal_rank_fusion


class HybridSearcher:
    """Run a query through both indexes and fuse the results with RRF."""

    def __init__(
        self,
        embedder: Embedder,
        vector_index: VectorIndex,
        bm25: BM25Index,
        chunks: Mapping[str, Chunk],
    ) -> None:
        self.embedder = embedder
        self.vector_index = vector_index
        self.bm25 = bm25
        self.chunks = chunks

    def search(self, query: str, k: int = 10, alpha: float = 0.5) -> list[SearchHit]:
        """Return the top ``k`` hits.

        ``alpha`` weights the dense ranking during fusion; ``1 - alpha`` weights
        the lexical ranking. Each hit is tagged with the source(s) it came from.
        """
        if not query.strip():
            return []
        pool = max(k * 5, 20)
        query_vector = self.embedder.embed_one(query)
        dense = [cid for cid, _ in self.vector_index.search(query_vector, k=pool)]
        lexical = [cid for cid, _ in self.bm25.search(query, k=pool)]
        fused = reciprocal_rank_fusion([dense, lexical], weights=[alpha, 1.0 - alpha])
        dense_set, lexical_set = set(dense), set(lexical)
        hits: list[SearchHit] = []
        for chunk_id, score in fused[:k]:
            chunk = self.chunks.get(chunk_id)
            if chunk is None:
                continue
            in_dense = chunk_id in dense_set
            in_lexical = chunk_id in lexical_set
            source = "hybrid" if in_dense and in_lexical else ("dense" if in_dense else "lexical")
            hits.append(SearchHit(chunk=chunk, score=score, source=source))
        return hits
