# Architecture

repoctx is a small pipeline of independent pieces. Each stage has a narrow
interface so backends can be swapped without touching the rest.

```
files ──▶ chunking ──▶ embeddings ──▶ VectorIndex ─┐
   │                                                ├─▶ HybridSearcher ──▶ hits
   └────────────────▶ tokenizer ──▶ BM25Index ──────┘
   │
   └────────────────▶ graph.builder ──▶ CodeGraph ──▶ ContextBuilder ──▶ ContextPack
```

## Modules

| Package | Responsibility |
| --- | --- |
| `repoctx.chunking` | Split source into embeddable units (AST-aware for Python, windowed otherwise). |
| `repoctx.embeddings` | Turn text into L2-normalized vectors. `HashingEmbedder` is the offline default; `TorchEmbedder` is optional. |
| `repoctx.index` | `VectorIndex` (NumPy brute-force cosine), `BM25Index` (lexical), and the snapshot `store`. |
| `repoctx.retrieval` | Reciprocal Rank Fusion and the `HybridSearcher`. |
| `repoctx.graph` | `ast` symbol extraction, dependency graph construction, traversal and context assembly. |
| `repoctx.indexer` | Orchestrates chunk → embed → index → graph. |
| `repoctx.api` | The `Repoctx` facade most callers use. |
| `repoctx.cli` | `repoctx index/search/context/graph/info`. |

## Design goals

- **Offline & reproducible.** No network calls on the default path; the hashing
  embedder is deterministic.
- **One hard dependency.** The core imports only NumPy. Everything else is
  stdlib.
- **Exact over approximate.** For repo-sized corpora a full matrix-vector
  product is fast and avoids an ANN index that would need tuning and a native
  build.

## On-disk snapshot layout

```
.repoctx/
├── manifest.json     # dim, embedder, chunk count, config
├── chunks.jsonl      # one chunk per line
├── vectors/          # vectors.npy + ids.json
└── graph.json        # serialized CodeGraph
```

The BM25 index is not serialized; it is cheap to rebuild from `chunks.jsonl` on
load, which keeps the snapshot format simple.
