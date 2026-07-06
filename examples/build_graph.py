"""Build the dependency graph for a package and inspect a symbol's neighbours.

Run from the project root:

    python examples/build_graph.py
"""

from repoctx import Repoctx


def main() -> None:
    repo = Repoctx.index("repoctx")
    graph = repo.graph
    print(f"graph: {len(graph)} nodes, {len(graph.edges)} edges\n")

    target = "retrieval.search.HybridSearcher.search"
    if target in graph:
        callees = graph.neighbors(target, kinds=("calls",))
        print(f"{target} calls:")
        for callee in callees:
            print(f"  -> {callee}")

        pack = repo.context(target, depth=1)
        print(f"\ncontext pack around it: {len(pack)} chunk(s)")
    else:
        print(f"{target!r} not found — try one of:")
        for node in list(graph.nodes())[:10]:
            print(f"  {node}")


if __name__ == "__main__":
    main()
