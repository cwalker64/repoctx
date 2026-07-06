"""Runtime configuration for the toolkit."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass, field


@dataclass
class Config:
    """Knobs controlling chunking, embedding and retrieval.

    Defaults are chosen so the toolkit runs fully offline with no model
    downloads: the ``hashing`` embedder is deterministic and dependency-free.
    """

    embedder: str = "hashing"
    embedding_dim: int = 256
    include_ext: tuple[str, ...] = (".py",)

    # Chunking
    window_lines: int = 60
    window_overlap: int = 15
    max_chunk_lines: int = 200

    # Lexical (BM25) parameters
    bm25_k1: float = 1.5
    bm25_b: float = 0.75

    # Fusion
    rrf_k: int = 60
    alpha: float = 0.5  # weight of the dense ranking during fusion (0..1)

    extra_ignore: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if not 0.0 <= self.alpha <= 1.0:
            raise ValueError(f"alpha must be in [0, 1], got {self.alpha}")
        if self.embedding_dim <= 0:
            raise ValueError("embedding_dim must be positive")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_env(cls, prefix: str = "REPOCTX_") -> Config:
        """Build a config, overriding fields from ``REPOCTX_*`` env vars."""

        cfg = cls()
        for name in ("embedder",):
            env = os.environ.get(prefix + name.upper())
            if env:
                setattr(cfg, name, env)
        for name in ("embedding_dim", "window_lines", "window_overlap", "rrf_k"):
            env = os.environ.get(prefix + name.upper())
            if env:
                setattr(cfg, name, int(env))
        for name in ("alpha", "bm25_k1", "bm25_b"):
            env = os.environ.get(prefix + name.upper())
            if env:
                setattr(cfg, name, float(env))
        cfg.__post_init__()
        return cfg
