"""Embedding backends.

The default :class:`~repoctx.embeddings.hashing.HashingEmbedder` is fully
offline and deterministic. A PyTorch backend is available as an optional extra.
"""

from __future__ import annotations

from .base import Embedder

__all__ = ["Embedder"]
