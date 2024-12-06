# Usage

## Indexing

```python
from repoctx import Repoctx, Config

# Index a directory (walks recursively, skips .git/venv/__pycache__/...).
repo = Repoctx.index("./my_project")

# Or index an in-memory mapping of path -> source.
repo = Repoctx.from_files({"a.py": "def f(): ...", "b.py": "import a"})

# Tune behaviour with a Config.
repo = Repoctx.index("./my_project", config=Config(embedding_dim=512, alpha=0.6))
```

## Searching

```python
hits = repo.search("read a file lazily", k=10)
for hit in hits:
    print(hit.score, hit.source, hit.chunk.path, hit.chunk.start_line)
```

`alpha` controls the balance between dense and lexical rankings at fusion time
(`1.0` = dense only, `0.0` = lexical only). Pass it per-query to override the
config default:

```python
repo.search("HttpClient", k=5, alpha=0.2)  # lean on the lexical index for identifiers
```

## Context packs

```python
pack = repo.context("my_project.server.Server.start", depth=2)
print(len(pack), "chunks")
print(pack.render(max_chars=4000))
```

`depth` is how many graph hops to expand. Edge kinds followed are `calls`,
`inherits`, `imports` and `contains`.

## Persisting an index

```python
repo.save(".repoctx")
later = Repoctx.load(".repoctx")
```

## Environment variables

| Variable | Effect |
| --- | --- |
| `REPOCTX_EMBEDDING_DIM` | Override the vector dimension. |
| `REPOCTX_ALPHA` | Default dense/lexical fusion weight. |
| `REPOCTX_LOG_LEVEL` | Logger level (default `WARNING`). |

See [`Config.from_env`](../repoctx/config.py) for the full list.
