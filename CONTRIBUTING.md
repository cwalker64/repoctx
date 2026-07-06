# Contributing

Thanks for taking a look! repoctx is small and I'm happy to take issues and PRs.

## Development setup

```bash
git clone https://github.com/cwalker64/repoctx
cd repoctx
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Before you push

The same three checks run in CI:

```bash
ruff check .
ruff format --check .
mypy repoctx
pytest
```

`pre-commit` runs the linters automatically on `git commit`.

## Guidelines

- Keep the core dependency-free beyond NumPy. New heavyweight dependencies
  belong behind an optional extra (like `[torch]`).
- Add a test alongside any behaviour change. The suite must stay fully offline
  and deterministic — no network, no model downloads.
- Prefer small, focused commits.
- Public API changes should update `docs/` and `CHANGELOG.md`.

## Reporting bugs

Open an issue with a minimal snippet that reproduces the problem, your Python
version, and which embedder backend you're using.
