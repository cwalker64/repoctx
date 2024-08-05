"""Persist and restore an index snapshot on disk.

Layout under the snapshot directory::

    manifest.json      # dim, embedder name, chunk count, config
    chunks.jsonl       # one JSON object per chunk
    vectors/           # VectorIndex (vectors.npy + ids.json)
    graph.json         # serialized CodeGraph
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from ..graph.graph import CodeGraph
from ..types import Chunk
from .vector_index import VectorIndex

MANIFEST = "manifest.json"
CHUNKS = "chunks.jsonl"
VECTORS = "vectors"
GRAPH = "graph.json"


def save_snapshot(
    path: str | Path,
    *,
    chunks: list,
    vector_index: VectorIndex,
    graph: CodeGraph,
    embedder_name: str,
    config: dict | None = None,
) -> None:
    """Write an index snapshot to *path*."""
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    manifest = {
        "version": 1,
        "embedder": embedder_name,
        "dim": vector_index.dim,
        "n_chunks": len(chunks),
        "config": config or {},
    }
    (directory / MANIFEST).write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    with (directory / CHUNKS).open("w", encoding="utf-8") as handle:
        for chunk in chunks:
            handle.write(json.dumps(asdict(chunk)) + "\n")
    vector_index.save(directory / VECTORS)
    graph.save(directory / GRAPH)


def load_snapshot(path: str | Path) -> dict:
    """Read a snapshot written by :func:`save_snapshot`.

    Returns a dict with ``manifest``, ``chunks``, ``vector_index`` and
    ``graph``. The BM25 index is intentionally rebuilt by the caller since it
    is cheap and avoids serializing term-frequency tables.
    """
    directory = Path(path)
    manifest = json.loads((directory / MANIFEST).read_text(encoding="utf-8"))
    chunks: list[Chunk] = []
    with (directory / CHUNKS).open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                chunks.append(Chunk(**json.loads(line)))
    return {
        "manifest": manifest,
        "chunks": chunks,
        "vector_index": VectorIndex.load(directory / VECTORS),
        "graph": CodeGraph.load(directory / GRAPH),
    }
