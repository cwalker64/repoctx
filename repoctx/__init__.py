"""repoctx — repository-level context toolkit.

Index a codebase and pull back the symbols, snippets and dependency edges that
matter for a query. NumPy core, deterministic offline embeddings by default,
optional PyTorch backend.
"""

from __future__ import annotations

from .config import Config
from .embeddings.hashing import HashingEmbedder
from .embeddings.registry import make_embedder
from .graph.builder import build_graph
from .graph.graph import CodeGraph
from .index.vector_index import VectorIndex
from .toolkit import Repoctx
from .types import Chunk, Edge, SearchHit, Symbol

__version__ = "0.1.0"

__all__ = [
    "Repoctx",
    "Config",
    "HashingEmbedder",
    "make_embedder",
    "build_graph",
    "CodeGraph",
    "VectorIndex",
    "Chunk",
    "SearchHit",
    "Symbol",
    "Edge",
    "__version__",
]
