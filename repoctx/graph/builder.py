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


def _callee_name(func: ast.expr) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


class _CallVisitor(ast.NodeVisitor):
    """Record ``calls`` edges from the enclosing definition to each callee."""

    def __init__(self, graph: CodeGraph, module: str, local_ids: dict[str, str]) -> None:
        self.graph = graph
        self.module = module
        self.local_ids = local_ids
        self.scope: list[str] = []

    def _current(self) -> str:
        if not self.scope:
            return self.module
        return f"{self.module}." + ".".join(self.scope)

    def _enter(self, node: ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef) -> None:
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._enter(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._enter(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._enter(node)

    def visit_Call(self, node: ast.Call) -> None:
        name = _callee_name(node.func)
        if name:
            self.graph.add_edge(self._current(), self.local_ids.get(name, name), "calls")
        self.generic_visit(node)


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
        local_ids = _add_symbol_edges(graph, source, path, module)
        _CallVisitor(graph, module, local_ids).visit(tree)
    return graph
