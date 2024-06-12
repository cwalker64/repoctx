"""Map file extensions to chunkers and dispatch a file to the right one."""

from __future__ import annotations

from ..types import Chunk
from .base import window_chunks
from .python_ast import chunk_python


def supported_extensions() -> tuple[str, ...]:
    """Extensions we have a dedicated, symbol-aware chunker for."""
    return (".py",)


def chunk_file(path: str, source: str) -> list[Chunk]:
    """Chunk *source* using the best available strategy for its extension."""
    if path.endswith(".py"):
        chunks = chunk_python(source, path)
        if chunks:
            return chunks
    return window_chunks(source, path)
