from graphrag import router

class FakeIndex:
    def __init__(self, sim): self.sim = sim
    def match_question(self, q, top=3): return [{"name": "losing skills", "similarity": self.sim}]

def fake(route, conf, kind=("concern", 0.9), group=("all", 0.9)):
    def f(state, questions):
        out = {}
        if "route" in questions: out["route"] = {"choice": route, "confidence": conf, "probabilities": {route: conf}}
        if "kind" in questions: out["kind"] = {"choice": kind[0], "confidence": kind[1]}
        if "group" in questions: out["group"] = {"choice": group[0], "confidence": group[1]}
        return out
    return f

def test_low_confidence_clarifies_and_runs_nothing():
    r = router.answer("hmm", None, None, decide_fn=fake("local_search", 0.4))
    assert r["status"] == "clarify"

def test_out_of_scope_calls_no_query():
    r = router.answer("2+2", None, None, decide_fn=fake("out_of_scope", 0.99))   # driver None would raise if queried
    assert r["status"] == "out_of_scope"

def test_weak_concept_match_clarifies():
    r = router.answer("quotes about x", None, FakeIndex(0.7), decide_fn=fake("evidence", 0.95))
    assert r["status"] == "clarify"

def test_concept_stats_low_enum_confidence_clarifies():
    r = router.answer("top concerns", None, None, decide_fn=fake("concept_stats", 0.95, kind=("concern", 0.3)))
    assert r["status"] == "clarify" and r["kind_guess"] == "concern"
