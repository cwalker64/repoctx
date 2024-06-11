"""Language-agnostic sliding-window chunking.

Used as a fallback for files we cannot parse (anything that is not Python).
"""

from __future__ import annotations

from ..types import Chunk


def window_chunks(
    source: str,
    path: str,
    window: int = 60,
    overlap: int = 15,
    kind: str = "block",
) -> list[Chunk]:
    """Chunk *source* into overlapping line windows."""
    lines = source.splitlines()
    n = len(lines)
    if n == 0:
        return []
    step = max(window - overlap, 1)
    chunks: list[Chunk] = []
    start = 0
    while start < n:
        end = min(start + window, n)
        chunks.append(
            Chunk(
                id=f"{path}:{start + 1}-{end}",
                path=path,
                text="\n".join(lines[start:end]),
                start_line=start + 1,
                end_line=end,
                kind=kind,
            )
        )
        if end >= n:
            break
        start += step
    return chunks
