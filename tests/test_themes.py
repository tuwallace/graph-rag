import collections
from graphrag import themes

def _by():
    # two clean clusters of concepts that co-occur within interviews
    by = {}
    for i in range(6):
        by[f"a{i}"] = {("AIUse", f"x{j}") for j in range(6)}
    for i in range(6):
        by[f"b{i}"] = {("Concern", f"y{j}") for j in range(6)}
    return by

def test_detect_separates_clusters_and_is_deterministic():
    by = _by(); g = {t: "workforce" for t in by}
    t1, cov = themes.detect(by, g); t2, _ = themes.detect(by, g)
    assert [sorted(m["name"] for m in t["members"]) for t in t1] == [sorted(m["name"] for m in t["members"]) for t in t2]
    assert len(t1) == 2 and {len(t["members"]) for t in t1} == {6}
    assert t1[0]["id"] == "theme01"

def test_rare_concepts_excluded():
    by = _by(); by["solo"] = {("Task", "only once")}
    t, _ = themes.detect(by, {k: "creatives" for k in by})
    assert all(m["name"] != "only once" for th in t for m in th["members"])

def test_validate_rejects_uncited_and_numbers():
    th = {"members": [{"name": n} for n in "abcdef"]}
    ok = {"label": "Writing and editing", "summary": "Participants use AI to draft and edit text, and some worry about losing their own voice when they do.", "cited_concepts": ["a", "b", "c"]}
    assert themes.validate(ok, th) == []
    assert "cited_concepts not members" in themes.validate({**ok, "cited_concepts": ["a", "zzz"]}, th)
    assert "summary contains a number" in themes.validate({**ok, "summary": ok["summary"] + " 42 percent"}, th)

def test_validate_rejects_generic_and_duplicate_labels():
    th = {"members": [{"name": n} for n in "abcdef"]}
    ok = {"label": "Drafting and editing text", "summary": "Participants use assistants to draft and edit text, and some worry about losing their own voice when they do.", "cited_concepts": ["a", "b"]}
    assert themes.validate(ok, th) == []
    assert "label generic or duplicate" in themes.validate({**ok, "label": "AI in Creative Work"}, th)
    assert "label generic or duplicate" in themes.validate(ok, th, used_labels=["drafting and editing text"])
