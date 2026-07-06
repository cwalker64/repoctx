"""Core data structures shared across repoctx."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Chunk:
    """A contiguous slice of a source file that gets embedded and searched."""

    id: str
    path: str
    text: str
    start_line: int
    end_line: int
    symbol: Optional[str] = None
    kind: str = "block"  # module | class | function | method | block

    @property
    def n_lines(self) -> int:
        return self.end_line - self.start_line + 1


@dataclass
class SearchHit:
    """A ranked search result."""

    chunk: Chunk
    score: float
    source: str = "hybrid"  # dense | lexical | hybrid

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        loc = f"{self.chunk.path}:{self.chunk.start_line}"
        return f"SearchHit({loc}, score={self.score:.4f}, source={self.source})"


@dataclass(frozen=True)
class Symbol:
    """A named definition discovered in the AST."""

    name: str
    qualname: str
    kind: str  # function | class | method
    path: str
    start_line: int
    end_line: int
    bases: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class Edge:
    """A directed relationship between two graph nodes."""

    src: str
    dst: str
    kind: str  # imports | contains | inherits | calls
