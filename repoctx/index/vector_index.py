"""In-memory NumPy vector index.

The whole index is a single ``(n, dim)`` float32 matrix. For the repository
sizes repoctx targets, a brute-force matrix-vector product is fast, exact and
free of any native dependency.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np


class VectorIndex:
    """A growable matrix of row vectors keyed by string ids."""

    def __init__(self, dim: int) -> None:
        if dim <= 0:
            raise ValueError("dim must be positive")
        self.dim = dim
        self._vectors = np.zeros((0, dim), dtype=np.float32)
        self._ids: list[str] = []

    def __len__(self) -> int:
        return len(self._ids)

    @property
    def ids(self) -> list[str]:
        return list(self._ids)

    def add(self, ids: Sequence[str], vectors: np.ndarray) -> None:
        """Append rows to the index."""
        matrix = np.asarray(vectors, dtype=np.float32)
        if matrix.ndim != 2 or matrix.shape[1] != self.dim:
            raise ValueError(f"expected vectors of shape (n, {self.dim}), got {matrix.shape}")
        if len(ids) != matrix.shape[0]:
            raise ValueError("number of ids must match number of vectors")
        if len(self._ids):
            self._vectors = np.vstack([self._vectors, matrix])
        else:
            self._vectors = matrix.copy()
        self._ids.extend(ids)

    def _scores(self, query: np.ndarray) -> np.ndarray:
        vector = np.asarray(query, dtype=np.float32).reshape(-1)
        if vector.shape[0] != self.dim:
            raise ValueError(f"query must have dimension {self.dim}")
        norm = float(np.linalg.norm(vector))
        if norm > 0:
            vector = vector / norm
        row_norms = np.linalg.norm(self._vectors, axis=1)
        row_norms[row_norms == 0] = 1.0
        return (self._vectors @ vector) / row_norms

    def search(self, query: np.ndarray, k: int = 10) -> list[tuple[str, float]]:
        """Return the ``k`` closest ids and their cosine scores, best first."""
        if len(self._ids) == 0:
            return []
        scores = self._scores(query)
        order = np.argsort(-scores)
        return [(self._ids[i], float(scores[i])) for i in order[:k]]
