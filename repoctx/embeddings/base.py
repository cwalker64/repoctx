"""Abstract embedder interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np


class Embedder(ABC):
    """Turn text into dense float32 vectors.

    Implementations must return an ``(n, dim)`` array. Rows are expected to be
    L2-normalized so a dot product is a cosine similarity.
    """

    name: str = "base"
    dim: int

    @abstractmethod
    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Embed a batch of texts into an ``(len(texts), dim)`` array."""
        raise NotImplementedError

    def embed_one(self, text: str) -> np.ndarray:
        """Embed a single string into a ``(dim,)`` vector."""
        return self.embed([text])[0]
