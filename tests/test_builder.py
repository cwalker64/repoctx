from repoctx.graph.builder import build_graph

FILES = {
    "pkg/util.py": "def helper():\n    return 1\n",
    "pkg/app.py": (
        "from pkg.util import helper\n"
        "import os\n"
        "\n"
        "class Base:\n"
        "    pass\n"
        "\n"
        "class App(Base):\n"
        "    def run(self):\n"
        "        return helper()\n"
    ),
}


def test_module_nodes_present():
    graph = build_graph(FILES)
    assert "pkg.util" in graph
    assert "pkg.app" in graph


def test_import_edges():
    graph = build_graph(FILES)
    imports = set(graph.neighbors("pkg.app", kinds=("imports",)))
    assert "pkg.util" in imports
    assert "os" in imports


def test_contains_and_inherits_edges():
    graph = build_graph(FILES)
    contained = set(graph.neighbors("pkg.app", kinds=("contains",)))
    assert "pkg.app.App" in contained
    inherits = set(graph.neighbors("pkg.app.App", kinds=("inherits",)))
    assert "pkg.app.Base" in inherits


def test_call_edges():
    graph = build_graph(FILES)
    calls = set(graph.neighbors("pkg.app.App.run", kinds=("calls",)))
    assert "helper" in calls
