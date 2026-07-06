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

    def search(self, query: str, k: int = 10) -> list[SearchHit]:
        pool = max(k * 5, 20)
        query_vector = self.embedder.embed_one(query)
        dense = [cid for cid, _ in self.vector_index.search(query_vector, k=pool)]
        lexical = [cid for cid, _ in self.bm25.search(query, k=pool)]
        fused = reciprocal_rank_fusion([dense, lexical])
        hits: list[SearchHit] = []
        for chunk_id, score in fused[:k]:
            chunk = self.chunks.get(chunk_id)
            if chunk is not None:
                hits.append(SearchHit(chunk=chunk, score=score, source="hybrid"))
        return hits
