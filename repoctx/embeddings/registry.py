"""Factory for embedding backends selected by name."""

from __future__ import annotations

from typing import Any

from .base import Embedder
from .hashing import HashingEmbedder


def make_embedder(name: str = "hashing", dim: int = 256, **kwargs: Any) -> Embedder:
    """Build an embedder by name.

    ``"hashing"`` is the offline default; ``"torch"`` loads the optional
    PyTorch backend lazily so importing this module never requires torch.
    """
    key = name.lower()
    if key == "hashing":
        return HashingEmbedder(dim=dim, **kwargs)
    if key == "torch":
        from .torch_backend import TorchEmbedder

        return TorchEmbedder(dim=dim, **kwargs)
    raise ValueError(f"unknown embedder: {name!r}")
