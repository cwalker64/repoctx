# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project adheres
to [Semantic Versioning](https://semver.org/).

## [0.3.0]

### Added
- `Repoctx` facade with `index` / `from_files` / `search` / `context` and
  snapshot `save` / `load`.
- `context()` builds repo-level context packs by expanding the dependency graph.
- CLI subcommands `context`, `graph` and `info`.
- Optional PyTorch embedding backend (`repoctx[torch]`) and an embedder registry.

### Changed
- Renamed the internal `toolkit` module to `api`.
- Search now labels each hit with its source (`dense` / `lexical` / `hybrid`).

## [0.2.0]

### Added
- Hybrid retrieval: dense (NumPy) + BM25 fused with Reciprocal Rank Fusion.
- AST symbol extraction and dependency graph construction (imports, calls,
  inheritance, containment) with traversal helpers.
- On-disk snapshot store.

## [0.1.0]

### Added
- Initial release: deterministic hashing embedder, NumPy vector index,
  AST-aware chunking, and a basic `index` / `search` CLI.

[0.3.0]: https://github.com/cwalker64/repoctx/releases/tag/v0.3.0
[0.2.0]: https://github.com/cwalker64/repoctx/releases/tag/v0.2.0
[0.1.0]: https://github.com/cwalker64/repoctx/releases/tag/v0.1.0
