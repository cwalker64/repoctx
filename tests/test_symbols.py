from repoctx.graph.symbols import extract_symbols

SOURCE = '''
import os


def top_level():
    return 1


class Widget(Base):
    def render(self):
        return "html"

    async def refresh(self):
        return None
'''


def test_finds_all_definitions():
    symbols = {s.qualname: s for s in extract_symbols(SOURCE, "w.py")}
    assert set(symbols) == {"top_level", "Widget", "Widget.render", "Widget.refresh"}


def test_kinds_are_correct():
    symbols = {s.qualname: s for s in extract_symbols(SOURCE, "w.py")}
    assert symbols["top_level"].kind == "function"
    assert symbols["Widget"].kind == "class"
    assert symbols["Widget.render"].kind == "method"


def test_class_bases_are_captured():
    symbols = {s.qualname: s for s in extract_symbols(SOURCE, "w.py")}
    assert symbols["Widget"].bases == ("Base",)


def test_syntax_error_returns_empty():
    assert extract_symbols("def (:\n", "bad.py") == []
