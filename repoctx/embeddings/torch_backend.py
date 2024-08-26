"""Optional PyTorch embedding backend.

This is a thin bring-your-own-model adapter: pass any object exposing
``encode(list[str]) -> array`` (for example a ``sentence_transformers`` model)
and repoctx will normalize and index the output. It is deliberately kept out of
the default dependency set so the core stays offline and lightweight.
"""

from __future__ import annotations

from typing import Any, Optional, Sequence

import numpy as np

from .base import Embedder


class TorchEmbedder(Embedder):
    """Wrap a PyTorch-backed encoder in the :class:`Embedder` interface."""

    name = "torch"

    def __init__(
        self,
        model: Any = None,
        dim: Optional[int] = None,
        device: Optional[str] = None,
        normalize: bool = True,
    ) -> None:
        try:
            import torch
        except ImportError as exc:  # pragma: no cover - exercised only without torch
            raise ImportError(
                "PyTorch backend requires the optional extra: pip install 'repoctx[torch]'"
            ) from exc
        self._torch = torch
        self.model = model
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.normalize = normalize
        if dim is None and model is not None:
            dim = getattr(model, "embedding_dim", None) or getattr(model, "dim", None)
        if dim is None:
            raise ValueError("dim is required when no model is provided")
        self.dim = int(dim)

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        if self.model is None:
            raise RuntimeError("TorchEmbedder needs a model exposing .encode(list[str])")
        raw = self.model.encode(list(texts))
        array = np.asarray(raw, dtype=np.float32)
        if array.ndim == 1:
            array = array.reshape(1, -1)
        if self.normalize:
            norms = np.linalg.norm(array, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            array = array / norms
        return array
