from repoctx import Repoctx

FILES = {
    "m.py": "def helper():\n    return 1\n\n\ndef main():\n    return helper()\n",
}


def test_context_includes_resolved_callee():
    toolkit = Repoctx.from_files(FILES)
    pack = toolkit.context("m.main", depth=1)
    symbols = {c.symbol for c in pack.chunks}
    assert "main" in symbols
    assert "helper" in symbols


def test_render_contains_both_definitions():
    toolkit = Repoctx.from_files(FILES)
    text = toolkit.context("m.main", depth=1).render()
    assert "def main" in text
    assert "def helper" in text


def test_unknown_target_is_empty():
    toolkit = Repoctx.from_files(FILES)
    assert len(toolkit.context("m.does_not_exist")) == 0
