"""Consistency checks on the model-judged label files (data/eval/judge/, data/eval/concern_pass/). Structural only: it confirms the files
are complete and well formed, not that the labels are right. Label correctness was confirmed by the project owner (docs/08, 'Label confirmation').
Run: PYTHONPATH=src:. uv run python eval/check_labels.py   (exit 1 on any failure)
"""
import json, collections, sys
from graphrag import config as C

J, P = C.ROOT / "data" / "eval" / "judge", C.ROOT / "data" / "eval" / "concern_pass"
LABELS = {"correct", "hypothetical", "wrong"}
res = []


def jl(p): return [json.loads(l) for l in open(p)] if p.exists() else []


def check(name, ok, detail=""): res.append(ok); print(("PASS " if ok else "FAIL ") + name + (": " + detail if detail else ""))


pr = jl(J / "precision.jsonl")
check("precision: 120 unique edges", len({r["key"] for r in pr}) == len(pr) == 120, str(len(pr)))
check("precision: every label valid", all(r["label"] in LABELS for r in pr), str(collections.Counter(r["label"] for r in pr)))
kept = collections.Counter(r["kind"] for r in pr if r["keep"])
check("precision: 30 kept per kind, 30 rejected", set(kept.values()) == {30} and len(kept) == 3 and sum(not r["keep"] for r in pr) == 30, f"{dict(kept)}, rejected {sum(not r['keep'] for r in pr)}")
rc = jl(J / "recall.jsonl")
check("recall: 10 transcripts (4 workforce, 3 creatives, 3 scientists)", collections.Counter(r["group"] for r in rc) == {"workforce": 4, "creatives": 3, "scientists": 3})
check("recall: every listed item was judged", all(r["n_items"] == r["n_judged"] for r in rc), f"{sum(r['n_judged'] for r in rc)}/{sum(r['n_items'] for r in rc)}")
for fn in ("questions.json", "questions2.json"):
    if (J / fn).exists():
        q = json.load(open(J / fn)); c = collections.Counter(x["route"] for x in q)
        check(f"{fn}: 8 questions per route, 6 routes", len(c) == 6 and set(c.values()) == {8}, str(dict(c)))
cp = jl(P / "precision.jsonl")
check("concern pass: every label valid", all(r["label"] in LABELS for r in cp), f"{len(cp)} edges")
cv = jl(P / "coverage.jsonl")
check("concern pass: coverage on the same 10 transcripts", {r["key"] for r in cv} == {r["key"] for r in rc}, f"{len(cv)}")
check("concern pass: coverage never decreases", all(r["after"] >= r["before"] for r in cv))
sys.exit(0 if all(res) else 1)
