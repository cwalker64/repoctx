"""Deterministic, offline feature-hashing embedder.

This backend needs no model download and produces identical vectors on every
machine, which keeps tests reproducible and CI free of network access.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np

from .base import Embedder


class HashingEmbedder(Embedder):
    """Embed text by hashing tokens into a fixed number of buckets."""

    name = "hashing"

    def __init__(self, dim: int = 256, seed: int = 0, use_bigrams: bool = True) -> None:
        if dim <= 0:
            raise ValueError("dim must be positive")
        self.dim = dim
        self.seed = seed
        self.use_bigrams = use_bigrams

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        # TODO: hash tokens into buckets; skeleton returns zeros for now.
        return np.zeros((len(texts), self.dim), dtype=np.float32)
