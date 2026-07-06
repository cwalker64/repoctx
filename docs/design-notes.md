# Design notes

A few decisions worth writing down, mostly so I remember why later.

## Why a hashing embedder by default

Most code-search tools reach for a transformer embedding model on the first
run. That means a multi-hundred-MB download, a cold-start delay, and results
that drift between library versions. For a tool whose whole point is
*repository context*, I wanted the default path to be:

- **Offline** — works in CI and air-gapped environments.
- **Deterministic** — the same repo produces the same vectors, so tests can
  assert on ranking.
- **Zero-config** — no model to pick.

Feature hashing gives all three. It is not as strong as a learned model on
pure natural-language paraphrase, but with sub-token splitting and BM25 fusion
it is very competitive on code, where identifiers carry most of the signal.
When you do want learned embeddings, `TorchEmbedder` accepts any encoder with an
`.encode()` method.

## Why NumPy brute force instead of an ANN index

An approximate nearest-neighbour index (FAISS, HNSW, …) earns its keep at
millions of vectors. A single repository is usually tens of thousands of chunks
at most. At that scale a dense `matrix @ query` is sub-millisecond, exact, and
adds no native dependency or index-tuning surface. If repoctx ever needs to
scale past that, the `VectorIndex` interface is small enough to back with an ANN
store without touching callers.

## Why `ast` instead of tree-sitter

tree-sitter would unlock many languages, but it needs a native build step and
per-grammar packages — friction that fights the offline-first goal. The stdlib
`ast` module covers Python (the primary target) with zero dependencies and
gives exact line spans for symbol-aligned chunking. Non-Python files still get
windowed chunks and appear in search; they just don't get graph edges.

## Known limitations

- Call edges are resolved within a module only. A call to an imported function
  is recorded against the bare name, not the fully-qualified target. Proper
  cross-module resolution would sharpen `context()` and is the most likely next
  step.
- Feature hashing has no notion of synonyms; "delete" and "remove" are distinct
  tokens.
