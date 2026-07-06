"""Index this repository and run a couple of queries.

Run it from the project root:

    python examples/quickstart.py
"""

from repoctx import Repoctx


def main() -> None:
    # Index the package source itself — a convenient, always-present corpus.
    repo = Repoctx.index("repoctx")

    print(f"indexed {len(repo.chunks)} chunks\n")

    for query in ("hybrid search fusion", "build the dependency graph", "normalize vectors"):
        print(f"# {query}")
        for hit in repo.search(query, k=3):
            symbol = hit.chunk.symbol or "<module>"
            print(f"  {hit.score:.3f}  {hit.chunk.path}:{hit.chunk.start_line}  {symbol}")
        print()


if __name__ == "__main__":
    main()
