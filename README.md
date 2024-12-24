# repoctx

[![CI](https://github.com/cwalker64/repoctx/actions/workflows/ci.yml/badge.svg)](https://github.com/cwalker64/repoctx/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Repository-level context for code. Point `repoctx` at a codebase and it builds
three complementary views — dense embeddings, a lexical index, and a
symbol/dependency graph — then answers two questions:

- **"where is the code about X?"** via hybrid semantic + lexical search
- **"what does this symbol depend on?"** via graph-expanded context packs

It is **offline-first and dependency-light**: the core needs only NumPy. The
default embedder is a deterministic feature-hasher, so indexing never downloads
a model and results are byte-for-byte reproducible across machines. A PyTorch
backend is available when you want learned embeddings.

## Install

```bash
pip install repoctx           # core (numpy only)
pip install "repoctx[torch]"  # + optional PyTorch backend
```

## Quickstart

```python
from repoctx import Repoctx

repo = Repoctx.index("./my_project")

for hit in repo.search("parse the config file", k=5):
    print(f"{hit.score:.3f} {hit.chunk.path}:{hit.chunk.start_line} {hit.chunk.symbol}")

# Pull a symbol plus everything it calls / inherits / imports.
pack = repo.context("my_project.config.load_config", depth=2)
print(pack.render())
```

From the command line:

```bash
repoctx index ./my_project -o .repoctx
repoctx search "retry with backoff" --index .repoctx
repoctx context my_project.http.Client.get --index .repoctx
repoctx graph --index .repoctx
```

## How it works

1. **Chunking** — Python files are split along `ast` boundaries so every
   function and method is its own chunk. Other files fall back to overlapping
   line windows.
2. **Embedding** — each chunk becomes an L2-normalized vector. The default
   `HashingEmbedder` hashes code tokens (with sub-token splitting, so `readFile`
   matches `read file`) into a fixed-width vector.
3. **Indexing** — vectors live in a single NumPy matrix; a pure-Python BM25
   index handles lexical matches.
4. **Search** — dense and lexical rankings are merged with Reciprocal Rank
   Fusion.
5. **Graph** — imports, calls, inheritance and containment are extracted with
   `ast` and used to expand a query symbol into a context pack.

## Documentation

- [Architecture](docs/architecture.md)
- [Usage](docs/usage.md)
- [API reference](docs/api-reference.md)
- [Design notes](docs/design-notes.md)

## Contributing

Issues and PRs welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). The test suite
is fully offline, so `pip install -e ".[dev]" && pytest` is all you need.

## License

MIT — see [LICENSE](LICENSE).