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
