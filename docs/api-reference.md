# API reference

The public surface is intentionally small. Everything below is importable from
the top-level `repoctx` package.

## `Repoctx`

The main facade.

| Method | Description |
| --- | --- |
| `Repoctx.index(root, config=None, embedder=None)` | Index a directory; returns a `Repoctx`. |
| `Repoctx.from_files(files, config=None, embedder=None)` | Index a `{path: source}` mapping. |
| `search(query, k=10, alpha=None)` | Return a list of `SearchHit`, best first. |
| `context(target, depth=1)` | Return a `ContextPack` for a graph node id. |
| `save(path)` / `Repoctx.load(path)` | Persist / restore an index snapshot. |
| `graph` | The underlying `CodeGraph`. |
| `chunks` | All indexed `Chunk` objects. |

## Data types

```python
@dataclass(frozen=True)
class Chunk:
    id: str
    path: str
    text: str
    start_line: int
    end_line: int
    symbol: str | None = None
    kind: str = "block"

@dataclass
class SearchHit:
    chunk: Chunk
    score: float
    source: str  # "dense" | "lexical" | "hybrid"
```

## `Config`

Construct directly or via `Config.from_env()`. Key fields: `embedder`,
`embedding_dim`, `include_ext`, `window_lines`, `window_overlap`, `bm25_k1`,
`bm25_b`, `rrf_k`, `alpha`. See [`config.py`](../repoctx/config.py).

## Building blocks

These are exported for advanced use and testing:

- `HashingEmbedder`, `make_embedder(name, dim, **kwargs)`
- `VectorIndex`
- `CodeGraph`, `build_graph(files)`

## CLI

```
repoctx index <path> [-o DIR]
repoctx search <query> [--index DIR] [-k N]
repoctx context <node-id> [--index DIR] [--depth N]
repoctx graph [--index DIR]
repoctx info [--index DIR]
```
