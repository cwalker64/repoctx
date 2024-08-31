"""Command-line interface for repoctx."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Optional, Sequence

from .config import Config
from .index.store import MANIFEST
from .toolkit import Repoctx

DEFAULT_INDEX_DIR = ".repoctx"


def _cmd_index(args: argparse.Namespace) -> int:
    toolkit = Repoctx.index(args.path, config=Config())
    toolkit.save(args.output)
    print(f"indexed {len(toolkit.chunks)} chunks from {args.path} -> {args.output}")
    return 0


def _cmd_search(args: argparse.Namespace) -> int:
    toolkit = Repoctx.load(args.index)
    hits = toolkit.search(args.query, k=args.k)
    for hit in hits:
        location = f"{hit.chunk.path}:{hit.chunk.start_line}"
        symbol = f"  {hit.chunk.symbol}" if hit.chunk.symbol else ""
        print(f"{hit.score:.4f}  [{hit.source:<7}] {location}{symbol}")
    return 0


def _cmd_context(args: argparse.Namespace) -> int:
    toolkit = Repoctx.load(args.index)
    pack = toolkit.context(args.target, depth=args.depth)
    if not len(pack):
        print(f"no context found for {args.target!r}")
        return 1
    print(pack.render())
    return 0


def _cmd_graph(args: argparse.Namespace) -> int:
    toolkit = Repoctx.load(args.index)
    graph = toolkit.graph
    kinds = Counter(edge.kind for edge in graph.edges)
    print(f"nodes: {len(graph)}")
    print(f"edges: {len(graph.edges)}")
    for kind, count in sorted(kinds.items()):
        print(f"  {kind}: {count}")
    return 0


def _cmd_info(args: argparse.Namespace) -> int:
    manifest = json.loads((Path(args.index) / MANIFEST).read_text(encoding="utf-8"))
    print(json.dumps(manifest, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="repoctx", description="Repository-level code context.")
    sub = parser.add_subparsers(dest="command")

    p_index = sub.add_parser("index", help="index a directory and save a snapshot")
    p_index.add_argument("path", help="directory to index")
    p_index.add_argument("-o", "--output", default=DEFAULT_INDEX_DIR, help="snapshot directory")
    p_index.set_defaults(func=_cmd_index)

    p_search = sub.add_parser("search", help="search an index")
    p_search.add_argument("query", help="natural-language or identifier query")
    p_search.add_argument("--index", default=DEFAULT_INDEX_DIR, help="snapshot directory")
    p_search.add_argument("-k", type=int, default=10, help="number of results")
    p_search.set_defaults(func=_cmd_search)

    p_context = sub.add_parser("context", help="gather graph context around a symbol")
    p_context.add_argument("target", help="node id, e.g. 'pkg.mod.func'")
    p_context.add_argument("--index", default=DEFAULT_INDEX_DIR, help="snapshot directory")
    p_context.add_argument("--depth", type=int, default=1, help="graph expansion depth")
    p_context.set_defaults(func=_cmd_context)

    p_graph = sub.add_parser("graph", help="print graph statistics")
    p_graph.add_argument("--index", default=DEFAULT_INDEX_DIR, help="snapshot directory")
    p_graph.set_defaults(func=_cmd_graph)

    p_info = sub.add_parser("info", help="print snapshot manifest")
    p_info.add_argument("--index", default=DEFAULT_INDEX_DIR, help="snapshot directory")
    p_info.set_defaults(func=_cmd_info)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return int(args.func(args))
