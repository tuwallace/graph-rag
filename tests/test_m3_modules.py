import json
import numpy as np
from graphrag import verify, attributes, normalise, manifest, decision

def test_stage_is_resumable_and_ignores_half_written_line(tmp_path):
    s = manifest.Stage("r1", "extract", root=tmp_path)
    s.write("a", {"x": 1}); s.write("b", {"x": 2})
    with open(s.path, "a") as f: f.write('{"key": "c", "x"')            # crash mid-write
    s2 = manifest.Stage("r1", "extract", root=tmp_path)
    assert s2.done("a") and s2.done("b") and not s2.done("c")
    assert [r["key"] for r in s2.records()] == ["a", "b"]

def test_verify_claim_text_per_kind_and_underscore_cleanup():
    it = {"kind": "ai_use", "name": "idea_sounding_board", "quote": "I bounce ideas off it."}
    assert "idea sounding board" in verify.claim_for(it) and "uses, tries or deliberately avoids AI" in verify.claim_for(it)
    assert 'Participant said: "I bounce ideas off it."' in verify.state_for(it)

def test_verify_item_and_keep_threshold(monkeypatch):
    monkeypatch.setattr(verify, "decide", lambda state, q: {"supports": {"noul": 0.91}, "own_current": {"noul": 0.2}})
    v = verify.verify_item({"kind": "concern", "name": "x", "quote": "q"})
    assert v == {"supports": 0.91, "own_current": 0.2}
    assert verify.keep(v, 0.5) and not verify.keep(v, 0.5, current_min=0.5) and not verify.keep(v, 0.95)

def test_attributes_is_one_call_per_segment(monkeypatch):
    calls = []
    def fake(state, qs):
        calls.append(sorted(qs)); return {"attitude": {"choice": "mixed", "confidence": 0.7}}
    monkeypatch.setattr(attributes, "decide", fake)
    r = attributes.attributes({"question": "q", "answer": "a"})
    assert r == {"attitude": "mixed", "attitude_conf": 0.7, "calls": 1} and calls == [["attitude"]]

def test_clean_names():
    assert normalise.clean("Idea_Sounding-board  ") == "idea sounding board"

def test_cluster_merges_close_names_and_keeps_most_frequent_as_canonical():
    names = ["drafting emails", "email drafting", "data analysis"]
    vecs = np.array([[1, 0, 0], [0.98, 0.199, 0], [0, 0, 1]], dtype=np.float32)
    vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
    m = normalise.cluster(names, vecs, {"drafting emails": 3, "email drafting": 1, "data analysis": 2}, threshold=0.9)
    assert m == {"drafting emails": "drafting emails", "email drafting": "drafting emails", "data analysis": "data analysis"}

def test_decide_raises_after_retries(monkeypatch):
    class R: status_code = 500; text = "boom"
    monkeypatch.setattr(decision.requests, "post", lambda *a, **k: R())
    monkeypatch.setattr(decision.time, "sleep", lambda s: None)
    try: decision.decide("s", {}); assert False
    except decision.DecisionError as e: assert "500" in str(e)

def test_strip_ai_before_embedding_keeps_meaning_and_never_returns_empty():
    assert normalise.strip_ai("ai for fact checking") == "for fact checking"
    assert normalise.strip_ai("AI's role".lower()) == "role"
    assert normalise.strip_ai("ai") == "ai"
