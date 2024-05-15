from repoctx.graph.graph import CodeGraph


def _build() -> CodeGraph:
    graph = CodeGraph()
    graph.add_node("m", kind="module")
    graph.add_node("m.A", kind="class")
    graph.add_node("m.f", kind="function")
    graph.add_edge("m", "m.A", "contains")
    graph.add_edge("m", "m.f", "contains")
    graph.add_edge("m.f", "m.A", "calls")
    return graph


def test_len_and_contains():
    graph = _build()
    assert len(graph) == 3
    assert "m.A" in graph


def test_neighbors_filtered_by_kind():
    graph = _build()
    assert set(graph.neighbors("m", kinds=("contains",))) == {"m.A", "m.f"}


def test_incoming_neighbors():
    graph = _build()
    assert graph.neighbors("m.A", direction="in") == ["m", "m.f"]


def test_bfs_reaches_both_hops():
    graph = _build()
    order = graph.bfs("m", depth=2)
    assert "m.A" in order and "m.f" in order


def test_json_roundtrip(tmp_path):
    graph = _build()
    path = tmp_path / "g.json"
    graph.save(path)
    restored = CodeGraph.load(path)
    assert len(restored) == len(graph)
    assert set(restored.neighbors("m")) == set(graph.neighbors("m"))
