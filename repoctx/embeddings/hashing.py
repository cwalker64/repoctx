"""Deterministic, offline feature-hashing embedder.

This backend needs no model download and produces identical vectors on every
machine, which keeps tests reproducible and CI free of network access.
"""

from __future__ import annotations

import hashlib
from typing import Sequence

import numpy as np

from ..text_utils import tokenize_code
from .base import Embedder

_BIGRAM_SEP = "\x1f"


def _l2_normalize(matrix: np.ndarray) -> None:
    """Scale each row to unit length in place, leaving zero rows untouched."""
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    np.divide(matrix, norms, out=matrix, where=norms > 0)


class HashingEmbedder(Embedder):
    """Embed text by hashing tokens into a fixed number of buckets."""

    name = "hashing"

    def __init__(self, dim: int = 256, seed: int = 0, use_bigrams: bool = True) -> None:
        if dim <= 0:
            raise ValueError("dim must be positive")
        self.dim = dim
        self.seed = seed
        self.use_bigrams = use_bigrams

    def _bucket(self, token: str) -> tuple[int, float]:
        """Map a token to a (bucket index, sign) pair with a stable hash.

        We use blake2b rather than the builtin ``hash`` because the latter is
        salted per-process, which would make embeddings non-reproducible.
        """

        digest = hashlib.blake2b(
            token.encode("utf-8"), digest_size=8, key=self.seed.to_bytes(8, "little")
        ).digest()
        value = int.from_bytes(digest, "little")
        index = value % self.dim
        sign = 1.0 if (value >> 63) & 1 else -1.0
        return index, sign

    def _features(self, text: str) -> list[str]:
        tokens = tokenize_code(text)
        if self.use_bigrams and len(tokens) > 1:
            bigrams = [f"{a}{_BIGRAM_SEP}{b}" for a, b in zip(tokens, tokens[1:])]
            tokens = tokens + bigrams
        return tokens

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        matrix = np.zeros((len(texts), self.dim), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in self._features(text):
                index, sign = self._bucket(token)
                matrix[row, index] += sign
        _l2_normalize(matrix)
        return matrix
