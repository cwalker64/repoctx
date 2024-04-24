"""A tiny directed multigraph tuned for code relationships."""

from __future__ import annotations

from collections import defaultdict

from ..types import Edge


class CodeGraph:
    """Nodes keyed by string id, edges tagged with a relationship kind."""

    def __init__(self) -> None:
        self._nodes: dict[str, dict] = {}
        self._edges: list[Edge] = []
        self._out: dict[str, list[Edge]] = defaultdict(list)
        self._in: dict[str, list[Edge]] = defaultdict(list)

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node_id: object) -> bool:
        return node_id in self._nodes

    @property
    def edges(self) -> list[Edge]:
        return list(self._edges)

    def nodes(self) -> list[str]:
        return list(self._nodes)

    def node(self, node_id: str) -> dict:
        return self._nodes[node_id]

    def add_node(self, node_id: str, **attrs: object) -> None:
        if node_id in self._nodes:
            self._nodes[node_id].update(attrs)
        else:
            self._nodes[node_id] = dict(attrs)

    def add_edge(self, src: str, dst: str, kind: str) -> None:
        if src not in self._nodes:
            self.add_node(src)
        if dst not in self._nodes:
            self.add_node(dst, kind="external")
        edge = Edge(src, dst, kind)
        self._edges.append(edge)
        self._out[src].append(edge)
        self._in[dst].append(edge)
