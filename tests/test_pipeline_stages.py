import json, pathlib
from graphrag import pipeline as P, manifest

TEXT = "Assistant: Hi.\n\nUser: Hello.\n\nAI: What do you use AI for?\n\nUser: I draft emails with it."

def fake_extract(text):
    return {"valid_json": True, "truncated": False, "n_raw_items": 2, "secs": 0.1, "prompt_version": "t", "model": "m", "extraction": {"items": [
        {"kind": "ai_use", "name": "drafting_emails", "status": "current", "polarity": "affirmed", "quote": "I draft emails with it.", "grounded": True, "segment_idx": 1},
        {"kind": "concern", "name": "made up", "status": "current", "polarity": "affirmed", "quote": "x", "grounded": True, "segment_idx": None}]}}

def test_scope_sizes_are_deterministic():
    assert set(P.SCOPES) >= {"demo", "tiny"}
    assert P.SCOPES["tiny"] == {"workforce": 2, "creatives": 2, "scientists": 1}

def test_stages_resume_and_assemble(tmp_path, monkeypatch):
    monkeypatch.setattr(manifest.C, "ROOT", tmp_path)
    picks = [("workforce", "work_1", TEXT)]
    calls = []
    def ext(text): calls.append(1); return fake_extract(text)
    P.stage_extract("t", picks, ext); P.stage_extract("t", picks, ext)           # second call must skip
    assert len(calls) == 1
    scores = iter([{"supports": 0.9, "own_current": 0.8}, {"supports": 0.05, "own_current": 0.1}])
    P.stage_verify("t", lambda it: next(scores))
    P.stage_attributes("t", {"work_1": TEXT}, lambda seg: {"attitude": "positive"})
    class Fake:                                                                    # embedding client stub: two distinct unit vectors
        def embed(self, model, input): return {"embeddings": [[1.0, 0.0] if "draft" in s else [0.0, 1.0] for s in input]}
    t = P.stage_normalise("t", Fake())
    assert t["mapping"]["ai_use"] == {"drafting emails": "drafting emails"}
    assert "made up" not in t["mapping"].get("concern", {})                         # dropped by the verify threshold
    out = P.assemble("t", {"work_1": TEXT})
    assert out["interviews"] == 1 and out["edges"] == 2 and out["kept"] == 1
    rec = json.loads(pathlib.Path(out["path"]).read_text().splitlines()[0])
    assert rec["group"] == "workforce" and [e["keep"] for e in rec["edges"]] == [True, False]
    assert rec["edges"][0]["canonical"] == "drafting emails" and len(rec["segments"]) == 2
