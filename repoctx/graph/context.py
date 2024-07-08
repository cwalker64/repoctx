"""Assemble repository-level context by walking the dependency graph.

Given a symbol, we pull its own chunk plus the chunks of its graph neighbours
(callees, base classes, imported modules) so a downstream consumer sees the
code *and* what it depends on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from ..types import Chunk
from .graph import CodeGraph

DEFAULT_KINDS = ("calls", "inherits", "imports", "contains")


@dataclass
class ContextPack:
    """A target node plus the chunks gathered around it."""

    target: str
    chunks: list[Chunk] = field(default_factory=list)


class ContextBuilder:
    """Expand a target node into a :class:`ContextPack`."""

    def __init__(self, graph: CodeGraph, symbol_chunks: Mapping[str, Chunk]) -> None:
        self.graph = graph
        self.symbol_chunks = symbol_chunks

    def build(
        self,
        target: str,
        depth: int = 1,
        kinds: tuple[str, ...] = DEFAULT_KINDS,
    ) -> ContextPack:
        node_ids = [target] + self.graph.bfs(target, depth=depth, kinds=kinds)
        seen: set[str] = set()
        chunks: list[Chunk] = []
        for node_id in node_ids:
            chunk = self.symbol_chunks.get(node_id)
            if chunk is not None and chunk.id not in seen:
                seen.add(chunk.id)
                chunks.append(chunk)
        return ContextPack(target=target, chunks=chunks)
