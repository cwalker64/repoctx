"""Command-line interface for repoctx."""

from __future__ import annotations

import argparse
from typing import Optional, Sequence

from .config import Config
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

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "func", None):
        parser.print_help()
        return 1
    return int(args.func(args))
