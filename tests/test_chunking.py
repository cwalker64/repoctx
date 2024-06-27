from repoctx.chunking.base import window_chunks
from repoctx.chunking.python_ast import chunk_python
from repoctx.chunking.registry import chunk_file

SRC = (
    "import os\n"
    "\n"
    "def alpha():\n"
    "    return 1\n"
    "\n"
    "class Widget:\n"
    "    def render(self):\n"
    "        return 2\n"
)


def test_python_chunks_have_symbols():
    chunks = chunk_python(SRC, "m.py")
    symbols = {c.symbol for c in chunks if c.symbol}
    assert "alpha" in symbols
    assert "Widget.render" in symbols


def test_chunks_are_ordered_by_line():
    chunks = chunk_python(SRC, "m.py")
    starts = [c.start_line for c in chunks]
    assert starts == sorted(starts)


def test_registry_dispatches_python():
    chunks = chunk_file("m.py", SRC)
    assert any(c.symbol == "alpha" for c in chunks)


def test_registry_falls_back_to_windows():
    text = "\n".join(f"line {i}" for i in range(200))
    chunks = chunk_file("notes.txt", text)
    assert len(chunks) >= 2
    assert all(c.kind == "block" for c in chunks)


def test_window_overlap_positions():
    text = "\n".join(str(i) for i in range(100))
    chunks = window_chunks(text, "f.txt", window=40, overlap=10)
    assert chunks[0].start_line == 1
    assert chunks[1].start_line == 31
