from repoctx.retrieval.fusion import reciprocal_rank_fusion


def test_shared_items_bubble_up():
    dense = ["a", "b", "c"]
    lexical = ["b", "a", "d"]
    fused = reciprocal_rank_fusion([dense, lexical])
    ids = [item for item, _ in fused]
    assert set(ids[:2]) == {"a", "b"}


def test_weights_break_ties():
    fused = reciprocal_rank_fusion([["x"], ["y"]], weights=[2.0, 1.0])
    assert fused[0][0] == "x"


def test_empty_input():
    assert reciprocal_rank_fusion([]) == []


def test_mismatched_weights_raise():
    import pytest

    with pytest.raises(ValueError):
        reciprocal_rank_fusion([["a"]], weights=[1.0, 2.0])
