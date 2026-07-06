"""Build a :class:`CodeGraph` from a set of Python source files."""

from __future__ import annotations

import ast

from ..text_utils import tokenize_code
from .graph import CodeGraph
from .symbols import extract_symbols


def _module_name(path: str) -> str:
    """Turn a repo-relative path into a dotted module name."""
    normalized = path.replace("\\", "/")
    if normalized.endswith(".py"):
        normalized = normalized[:-3]
    parts = [seg for seg in normalized.split("/") if seg not in ("", ".")]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else "<root>"


def _add_import_edges(graph: CodeGraph, tree: ast.AST, module: str) -> None:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                graph.add_edge(module, alias.name, "imports")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                graph.add_edge(module, node.module, "imports")


def _add_symbol_edges(graph: CodeGraph, source: str, path: str, module: str) -> dict[str, str]:
    """Add symbol nodes with ``contains`` and ``inherits`` edges.

    Returns a mapping of ``qualname -> node id`` for the call pass to reuse.
    """
    symbols = extract_symbols(source, path)
    local_ids = {sym.qualname: f"{module}.{sym.qualname}" for sym in symbols}
    for sym in symbols:
        node_id = local_ids[sym.qualname]
        graph.add_node(
            node_id,
            kind=sym.kind,
            path=path,
            name=sym.name,
            start_line=sym.start_line,
            end_line=sym.end_line,
        )
        graph.add_edge(module, node_id, "contains")
        for base in sym.bases:
            graph.add_edge(node_id, local_ids.get(base, base), "inherits")
    return local_ids


def build_graph(files: dict[str, str]) -> CodeGraph:
    """Construct a dependency graph from ``{path: source}``."""
    graph = CodeGraph()
    for path, source in sorted(files.items()):
        module = _module_name(path)
        graph.add_node(module, kind="module", path=path)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        _add_import_edges(graph, tree, module)
        _add_symbol_edges(graph, source, path, module)
    return graph
