"""ADR-0008 confirmation on questions written after the router changes were chosen (eval/confirm_questions.json, 20 new questions).
Routing and argument choice only (no answer text). B = router v2; A = qwen3 picks among the 5 typed tools (first call).
Also times the router's route decision on these fresh questions (identical requests are cached by Ollama, so only unseen text is timed).
Run: PYTHONPATH=src:. uv run python eval/confirm_adr0008.py [--old]   (--old also re-scores the original 40 with router v2, routing only)
"""
import json, sys, time, statistics, pathlib
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, router
from graphrag.decision import decide
import eval.run_eval as R

HERE = pathlib.Path(__file__).parent
TOOL_OF = {"local_search": "search_segments", "concept_stats": "concept_stats", "compare_groups": "compare_groups", "evidence": "quotes", "theme_overview": "theme_summary"}


def timed_decide():
    t = []
    def f(state, questions, **kw):
        t0 = time.time(); out = decide(state, questions, **kw); t.append(time.time() - t0); return out
    return f, t


def b_row(x, d, ix):
    f, t = timed_decide()
    p = router.answer(x["q"], d, ix, decide_fn=f)
    r = {"id": x["id"], "route": x["route"], "chose": p["route"], "conf": p["route_confidence"], "abstained": p["status"] == "clarify", "route_decision_secs": round(t[0], 3)}
    r["route_ok"] = p["route"] == x["route"]
    if x["route"] == "concept_stats": r["args_ok"] = r["route_ok"] and p.get("kind") == x["kind"] and p.get("group") == x["group"]
    elif x["route"] in ("compare_groups", "evidence"): r["args_ok"] = r["route_ok"] and p.get("concept") in x["concepts"]
    return r


def a_row(x, d, ix):
    rec = R.config_A(x, d, ix); calls = rec["calls"]; c0 = calls[0] if calls else None
    exp = TOOL_OF.get(x["route"]); chose = c0["name"] if c0 else "none"
    r = {"id": x["id"], "route": x["route"], "chose": chose, "abstained": False, "route_ok": (chose == exp) if exp else c0 is None}
    a = (c0 or {}).get("args", {})
    if x["route"] == "concept_stats": r["args_ok"] = r["route_ok"] and a.get("kind") == x["kind"] and a.get("group", "all") == x["group"]
    elif x["route"] in ("compare_groups", "evidence"):
        import re
        m = re.search(r'"concept": "([^"]+)"', rec["context"].split("\n")[0] if rec["context"] else "")
        r["args_ok"] = bool(r["route_ok"] and m and m.group(1) in x["concepts"])
    return r


def summ(rows, name):
    ins = [r for r in rows if r["route"] != "out_of_scope"]; ans = [r for r in ins if not r["abstained"]]
    args = [r for r in rows if r["route"] in ("concept_stats", "compare_groups", "evidence")]
    oos = [r for r in rows if r["route"] == "out_of_scope"]
    print(f"{name}: route correct {sum(r['route_ok'] for r in ins)}/{len(ins)}; abstained {sum(r['abstained'] for r in ins)}; when answered {sum(r['route_ok'] for r in ans)}/{len(ans)}; "
          f"wrong-argument calls {sum(not r.get('args_ok') for r in args)}/{len(args)}; out-of-scope ok {sum(r['route_ok'] for r in oos)}/{len(oos)}")


if __name__ == "__main__":
    new = json.loads((HERE / "confirm_questions.json").read_text())
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        ix = Q.ConceptIndex(d)
        b = [b_row(x, d, ix) for x in new]; a = [a_row(x, d, ix) for x in new]
        out = {"new": {"B": b, "A": a}}
        summ(b, f"B router {router.ROUTER_VERSION} (20 new)"); summ(a, "A qwen3 picks (20 new)")
        lat = [r["route_decision_secs"] for r in b]
        print(f"router route-decision latency, {len(lat)} unseen questions: p50 {statistics.median(lat):.2f}s p95 {sorted(lat)[int(round(0.95*(len(lat)-1)))]:.2f}s max {max(lat):.2f}s")
        if "--old" in sys.argv:
            old = json.loads((HERE / "questions.json").read_text())
            rows = [b_row(x, d, ix) for x in old]; out["old"] = rows
            for sp in ("dev", "held"):
                summ([r for r, x in zip(rows, old) if x["split"] == sp], f"B router {router.ROUTER_VERSION} on original {sp}")
            summ(rows, f"B router {router.ROUTER_VERSION} on original 40")
    json.dump(out, open(C.ROOT / "data" / "eval" / "confirm.json", "w"), indent=1)
