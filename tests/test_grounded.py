from graphrag import grounded

P = {"route": "evidence", "status": "ok", "concept": "losing skills",
     "quotes": [{"interview": "work_0001", "group": "workforce", "quote": "I worry I will lose my writing skills if I keep relying on it"}]}
R = grounded.render(P)

def test_render_contains_quote_and_id():
    assert "work_0001" in R and "lose my writing skills" in R

def test_good_answer_passes():
    a = 'One participant said "I worry I will lose my writing skills if I keep relying on it" (work_0001).'
    assert grounded.validate(a, P, R) == []

def test_invented_quote_fails():
    a = 'Someone said "AI makes me lazy and I forget how to draft anything myself" (work_0001).'
    assert any("quote not in tool output" in i for i in grounded.validate(a, P, R))

def test_uncited_quote_fails():
    a = 'One participant said "I worry I will lose my writing skills if I keep relying on it".'
    assert any("not cited" in i for i in grounded.validate(a, P, R))

def test_wrong_interview_id_fails():
    a = 'One participant said "I worry I will lose my writing skills if I keep relying on it" (work_0001, work_0999).'
    assert any("cited id not in tool output" in i for i in grounded.validate(a, P, R))

def test_figures_must_be_in_facts():
    S = {"route": "concept_stats", "status": "ok", "kind": "concern", "group": "all", "group_size": 500, "ranking": [{"concept": "hallucinations", "interviews": 23}]}
    r = grounded.render(S)
    assert grounded.validate("Hallucinations were mentioned in 23 interviews (4.6%).", S, r) == []
    assert any("figures" in i for i in grounded.validate("Hallucinations were mentioned in 40 interviews.", S, r))

def test_fallback_when_llm_invents():
    class D:  # minimal stand-ins for driver/index are not needed: patch router.answer
        pass
    import graphrag.router as router
    orig = router.answer
    router.answer = lambda q, d, i, **k: P | {"route_confidence": 0.9}
    try:
        out = grounded.grounded_answer("quotes?", None, None, llm=lambda q, r: 'He said "completely made up sentence about nothing at all" (work_0001).')
    finally:
        router.answer = orig
    assert out["source"] == "rendered_fallback" and out["text"] == R
