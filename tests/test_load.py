import json
from graphrag import load

TEXT = "Assistant: What do you use AI for?\nUser: I use AI tools for brainstorming new ideas every day.\nAssistant: Worries?\nUser: I worry about losing my skills over time."

def _run(tmp_path, edges):
    rec = {"transcript_id": "t1", "group": "creatives", "model": "m", "prompt_version": "v3.3",
           "segments": [{"idx": 0, "attitude": "positive", "attitude_conf": 0.9}, {"idx": 1, "attitude": "negative", "attitude_conf": 0.8}],
           "edges": edges}
    (tmp_path / "graph_input.jsonl").write_text(json.dumps(rec) + "\n")
    return load.build(tmp_path, {"t1": TEXT})

def E(**kw):
    base = {"kind": "ai_use", "raw_name": "brainstorming", "canonical": "brainstorming", "status": "current", "polarity": "affirmed",
            "quote": "I use AI tools for brainstorming new ideas", "segment_idx": 0, "verify": {"supports": 0.9, "own_current": 0.9}, "keep": True}
    return {**base, **kw}

def test_build_keeps_grounded_only(tmp_path):
    iv, segs, edges, st = _run(tmp_path, [E(), E(keep=False), E(quote="completely invented sentence about nothing", canonical="x"),
                                          E(kind="concern", canonical="skill loss", quote="I worry about losing my skills", segment_idx=1)])
    assert len(iv) == 1 and len(segs) == 2
    assert len(edges["ai_use"]) == 1 and len(edges["concern"]) == 1
    assert st["ungrounded"] == 1 and st["edges_kept"] == 3

def test_edge_id_stable_and_distinct():
    a = load.edge_id("t#0", "ai_use", "x", "q")
    assert a == load.edge_id("t#0", "ai_use", "x", "q") and a != load.edge_id("t#0", "ai_use", "y", "q")

def test_embed_cache_reused(tmp_path):
    class C:
        calls = 0
        def embed(self, model, input):
            C.calls += 1; return {"embeddings": [[0.1, 0.2] for _ in input]}
    segs = [{"id": "a#0", "question": "q", "answer": "a"}, {"id": "a#1", "question": "q", "answer": "b"}]
    p = tmp_path / "e.jsonl"
    load.embed_segments(segs, p, client=C()); load.embed_segments(segs, p, client=C())
    assert C.calls == 1
