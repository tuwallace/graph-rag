"""Routing accuracy on questions written by a different model (qwen2.5:32b) from route descriptions only (eval/judge32b.py questions).
B = router v2 (nimble); A = qwen3 picks among the 5 typed tools (first call only). The gold route is the generator's intent, so label noise is possible;
disagreements are listed for reading. Run: PYTHONPATH=src:. uv run python eval/route_generated.py
"""
import json, collections
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, router
import eval.run_eval as R

TOOL_OF = {"local_search": "search_segments", "concept_stats": "concept_stats", "compare_groups": "compare_groups", "evidence": "quotes", "theme_overview": "theme_summary"}
qs = json.load(open(C.ROOT / "data" / "eval" / "judge" / "questions.json"))
rows = []
with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
    ix = Q.ConceptIndex(d)
    for x in qs:
        p = router.answer(x["q"], d, ix)
        r = R.chat([{"role": "system", "content": R.SYSTEM}, {"role": "user", "content": x["q"]}], R.TOOLS)
        tc = (r.message.tool_calls or [None])[0]
        a_tool = tc.function.name if tc else "none"; a_args = dict(tc.function.arguments or {}) if tc else {}
        exp = TOOL_OF.get(x["route"])
        row = {"id": x["id"], "q": x["q"], "route": x["route"], "b_route": p["route"], "b_conf": p["route_confidence"], "b_abstain": p["status"] == "clarify",
               "b_ok": p["route"] == x["route"], "a_tool": a_tool, "a_ok": (a_tool == exp) if exp else (a_tool == "none")}
        if x["route"] == "concept_stats" and x.get("kind") in Q.KINDS:
            row["b_args_ok"] = row["b_ok"] and p.get("kind") == x["kind"] and p.get("group") == x["group"]
            row["a_args_ok"] = row["a_ok"] and a_args.get("kind") == x["kind"] and a_args.get("group", "all") == x["group"]
        rows.append(row)
json.dump(rows, open(C.ROOT / "data" / "eval" / "route_generated.json", "w"), indent=1)
ins = [r for r in rows if r["route"] != "out_of_scope"]; oos = [r for r in rows if r["route"] == "out_of_scope"]
def pct(a, b): return f"{a}/{b} ({a/b:.0%})" if b else "n/a"
print("questions", len(rows), "in scope", len(ins), "out of scope", len(oos))
print("B route correct (in scope):", pct(sum(r["b_ok"] for r in ins), len(ins)), "| abstained:", sum(r["b_abstain"] for r in ins), "| correct when answered:", pct(sum(r["b_ok"] for r in ins if not r["b_abstain"]), sum(not r["b_abstain"] for r in ins)))
print("A tool correct (in scope):", pct(sum(r["a_ok"] for r in ins), len(ins)))
print("out of scope handled: B", pct(sum(r["b_ok"] or r["b_abstain"] for r in oos), len(oos)), "A", pct(sum(r["a_ok"] for r in oos), len(oos)))
st = [r for r in rows if "b_args_ok" in r]; print("stats kind+group correct: B", pct(sum(r["b_args_ok"] for r in st), len(st)), "A", pct(sum(r["a_args_ok"] for r in st), len(st)))
bymis = collections.Counter((r["route"], r["b_route"]) for r in rows if not r["b_ok"]); print("B confusions (gold, got):", dict(bymis))
for r in rows:
    if not r["b_ok"] or not r["a_ok"]: print(f' {r["route"]:<14} B->{r["b_route"]:<14} {r["b_conf"]:.2f} A->{r["a_tool"]:<15} {r["q"][:95]}')
