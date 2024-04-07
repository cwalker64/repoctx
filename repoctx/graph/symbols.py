"""Extract definitions from Python source using the standard :mod:`ast`.

Sticking to the stdlib parser keeps repoctx offline and dependency-light; the
trade-off is that only Python is understood at the symbol level.
"""

from __future__ import annotations

import ast
from typing import Optional

from ..types import Symbol


def _dotted_name(node: ast.expr) -> Optional[str]:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = _dotted_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    return None


def _walk(node: ast.AST, stack: list[str], path: str, out: list[Symbol], in_class: bool) -> None:
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            qualname = ".".join(stack + [child.name])
            kind = "method" if in_class else "function"
            out.append(
                Symbol(
                    name=child.name,
                    qualname=qualname,
                    kind=kind,
                    path=path,
                    start_line=child.lineno,
                    end_line=getattr(child, "end_lineno", child.lineno) or child.lineno,
                )
            )
            _walk(child, stack + [child.name], path, out, in_class=False)
        elif isinstance(child, ast.ClassDef):
            qualname = ".".join(stack + [child.name])
            bases = tuple(b for b in (_dotted_name(base) for base in child.bases) if b)
            out.append(
                Symbol(
                    name=child.name,
                    qualname=qualname,
                    kind="class",
                    path=path,
                    start_line=child.lineno,
                    end_line=getattr(child, "end_lineno", child.lineno) or child.lineno,
                    bases=bases,
                )
            )
            _walk(child, stack + [child.name], path, out, in_class=True)
        else:
            _walk(child, stack, path, out, in_class)


def extract_symbols(source: str, path: str = "<unknown>") -> list[Symbol]:
    """Return every function, method and class defined in *source*.

    Files that fail to parse yield an empty list rather than raising, so one
    broken file never aborts a whole repository scan.
    """

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    symbols: list[Symbol] = []
    _walk(tree, [], path, symbols, in_class=False)
    return symbols
