"""A tiny directed multigraph tuned for code relationships."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

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

    def neighbors(
        self,
        node_id: str,
        kinds: Optional[tuple[str, ...]] = None,
        direction: str = "out",
    ) -> list[str]:
        """Return adjacent node ids, optionally filtered by edge *kinds*."""
        if direction == "out":
            edges = self._out.get(node_id, [])
            pick = lambda e: e.dst  # noqa: E731
        elif direction == "in":
            edges = self._in.get(node_id, [])
            pick = lambda e: e.src  # noqa: E731
        else:
            raise ValueError("direction must be 'in' or 'out'")
        result: list[str] = []
        for edge in edges:
            if kinds and edge.kind not in kinds:
                continue
            result.append(pick(edge))
        return result

    def bfs(
        self,
        start: str,
        depth: int = 1,
        kinds: Optional[tuple[str, ...]] = None,
        direction: str = "out",
    ) -> list[str]:
        """Breadth-first expansion from *start*, up to *depth* hops.

        The start node itself is not included in the returned list.
        """
        seen = {start}
        frontier = [start]
        order: list[str] = []
        for _ in range(max(depth, 0)):
            nxt: list[str] = []
            for node_id in frontier:
                for neighbor in self.neighbors(node_id, kinds, direction):
                    if neighbor not in seen:
                        seen.add(neighbor)
                        nxt.append(neighbor)
                        order.append(neighbor)
            frontier = nxt
            if not frontier:
                break
        return order

    def to_dict(self) -> dict:
        return {
            "nodes": [{"id": nid, **attrs} for nid, attrs in self._nodes.items()],
            "edges": [{"src": e.src, "dst": e.dst, "kind": e.kind} for e in self._edges],
        }

    @classmethod
    def from_dict(cls, data: dict) -> CodeGraph:
        graph = cls()
        for node in data.get("nodes", []):
            attrs = {k: v for k, v in node.items() if k != "id"}
            graph.add_node(node["id"], **attrs)
        for edge in data.get("edges", []):
            graph.add_edge(edge["src"], edge["dst"], edge["kind"])
        return graph

    def save(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> CodeGraph:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
