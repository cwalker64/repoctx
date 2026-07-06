"""AST-aware chunking for Python sources.

Each function and method becomes its own chunk so a search hit points at a
single, self-contained unit. Lines that live outside any definition (imports,
module constants) are grouped into ``module`` chunks.
"""

from __future__ import annotations

from typing import Iterable

from ..graph.symbols import extract_symbols
from ..types import Chunk


def _contiguous(numbers: list[int]) -> Iterable[tuple[int, int]]:
    if not numbers:
        return
    ordered = sorted(numbers)
    start = prev = ordered[0]
    for value in ordered[1:]:
        if value == prev + 1:
            prev = value
        else:
            yield (start, prev)
            start = prev = value
    yield (start, prev)


def chunk_python(source: str, path: str) -> list[Chunk]:
    """Split *source* into symbol-aligned chunks."""
    lines = source.splitlines()
    n = len(lines)
    if n == 0:
        return []

    symbols = extract_symbols(source, path)
    method_parents = {s.qualname.rsplit(".", 1)[0] for s in symbols if s.kind == "method"}
    chosen = [
        s
        for s in symbols
        if s.kind in ("function", "method")
        or (s.kind == "class" and s.qualname not in method_parents)
    ]

    chunks: list[Chunk] = []
    covered: set[int] = set()
    for sym in chosen:
        start = max(sym.start_line, 1)
        end = min(sym.end_line, n)
        if end < start:
            continue
        chunks.append(
            Chunk(
                id=f"{path}:{start}-{end}",
                path=path,
                text="\n".join(lines[start - 1 : end]),
                start_line=start,
                end_line=end,
                symbol=sym.qualname,
                kind=sym.kind,
            )
        )
        covered.update(range(start, end + 1))

    residual = [i for i in range(1, n + 1) if i not in covered and lines[i - 1].strip()]
    for start, end in _contiguous(residual):
        chunks.append(
            Chunk(
                id=f"{path}:{start}-{end}",
                path=path,
                text="\n".join(lines[start - 1 : end]),
                start_line=start,
                end_line=end,
                kind="module",
            )
        )

    chunks.sort(key=lambda c: c.start_line)
    return chunks
