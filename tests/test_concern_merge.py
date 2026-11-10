import numpy as np
from graphrag import concern_merge as M


def fake_embed(names):
    table = {"a": [1, 0, 0], "a2": [0.99, 0.1, 0], "b": [0, 1, 0], "b2": [0, 0.99, 0.1]}
    v = np.array([table[n] for n in names], dtype=np.float32)
    return v / np.linalg.norm(v, axis=1, keepdims=True)


def test_assign_joins_existing_or_clusters_new():
    m = M.assign({"a2": 3, "b": 2, "b2": 1}, ["a"], fake_embed)
    assert m["a2"] == "a"                 # close to an existing canonical
    assert m["b"] == "b" and m["b2"] == "b"   # new, clustered together, most frequent leads


def test_new_items_skips_used_quotes_and_unverified():
    ex = [{"key": "t", "items": [
        {"kind": "concern", "name": "x", "quote": "I worry a lot", "grounded": True, "segment_idx": 1},
        {"kind": "concern", "name": "y", "quote": "Already used", "grounded": True, "segment_idx": 1},
        {"kind": "concern", "name": "z", "quote": "weak one", "grounded": True, "segment_idx": 2}]}]
    vr = {"t": {"scores": [{"supports": 0.9, "own_current": 0.9}, {"supports": 0.9, "own_current": 0.9}, {"supports": 0.05, "own_current": 0.9}]}}
    out = M.new_items(ex, vr, {"t": {"already used"}})
    assert [i["name"] for i in out["t"]] == ["x"]
