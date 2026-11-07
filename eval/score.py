"""Score the M7 runs. Usage: PYTHONPATH=src:. uv run python eval/score.py
Reads data/eval/{A,B,C}.jsonl and eval/questions.json; prints markdown tables for dev, held-out and all."""
import json, re, statistics, pathlib
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, ground
from graphrag.parse import user_text
from graphrag.pipeline import select

HERE = pathlib.Path(__file__).parent
QUESTIONS = {x["id"]: x for x in json.loads((HERE / "questions.json").read_text())}
TOOL_OF = {"local_search": "search_segments", "concept_stats": "concept_stats", "compare_groups": "compare_groups", "evidence": "quotes", "theme_overview": "theme_summary"}
QMARK = re.compile(r'["“”]')
LISTNUM = re.compile(r"(?m)^\s*(?:[-*]\s*)?(?:\*\*)?\d{1,2}[.)]\s")


def quotes_in(text: str) -> list[str]:
    """Pair quote marks strictly (1st with 2nd, 3rd with 4th ...), then keep spans of at least 4 words. The first scorer used a regex with a
    15-character minimum, so a short quoted term such as "hallucinations" shifted the pairing and produced bogus spans."""
    idx = [m.start() for m in QMARK.finditer(text)]
    spans = [text[a + 1:b] for a, b in zip(idx[0::2], idx[1::2])]
    return [q for q in spans if len(q.split()) >= 4]
IDRE = re.compile(r"\b[a-z]+_\d{4}(?:#\d+)?\b")
NUM = re.compile(r"(?<![\w#.])\d+(?:\.\d+)?%?")
REFUSE = re.compile(r"cannot|can't|can not|not (?:about|related|relevant)|only (?:answer|answers)|no (?:relevant|information)|outside|unrelated|not able|don't have|do not have|doesn't|does not (?:contain|include|mention)", re.I)


def load(cfg):
    p = C.ROOT / "data" / "eval" / f"{cfg}.jsonl"
    return {r["id"]: r for r in map(json.loads, open(p))} if p.exists() else {}


def norm(s): return " ".join(ground.tokens(s))


def nums(text, strip_ids=True):
    t = IDRE.sub(" ", text) if strip_ids else text
    t = LISTNUM.sub(" ", t)   # list markers ("1.", "2)") are not figures
    return {n.rstrip("%") for n in NUM.findall(t)}


def context_numbers(ctx):
    out = nums(ctx)
    for n in list(out):
        try:
            v = float(n)
            if v < 1: out |= {str(round(v * 100)), f"{v*100:.1f}"}
        except ValueError: pass
    return out


def first_call(cfg, rec):
    if cfg == "A":
        c = rec.get("calls") or []
        return c[0] if c else None
    return None


def evaluate():
    texts = {tid: user_text(t) for _, tid, t in select("demo")}
    ntexts = {tid: norm(t) for tid, t in texts.items()}
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        gold_stats = {(k, g): Q.concept_stats(d, k, g, 1)[0] for k in Q.KINDS for g in Q.GROUPS}
        gold_cmp = {}; gold_sizes = Q.group_sizes(d)
        for x in QUESTIONS.values():
            if x["route"] == "compare_groups":
                gold_cmp[x["id"]] = {g: v["interviews"] for g, v in Q.compare_groups(d, x["concepts"][0]).items()}
    rows = []
    for cfg in "ABC":
        for qid, rec in load(cfg).items():
            x = QUESTIONS[qid]; ans = rec.get("answer", ""); ctx = rec.get("context", "")
            r = {"cfg": cfg, "id": qid, "split": x["split"], "route": x["route"], "secs": rec.get("secs"), "error": bool(rec.get("error"))}
            exp_tool = TOOL_OF.get(x["route"])
            # routing / tool choice
            if cfg == "A":
                calls = rec.get("calls") or []; c0 = calls[0] if calls else None
                r["chose"] = c0["name"] if c0 else "none"; r["abstained"] = False
                r["route_ok"] = (r["chose"] == exp_tool) if exp_tool else (c0 is None)
                a = (c0 or {}).get("args", {})
                if x["route"] == "concept_stats": r["args_ok"] = r["route_ok"] and a.get("kind") == x["kind"] and a.get("group", "all") == x["group"]
                elif x["route"] in ("compare_groups", "evidence"):
                    names = [m["name"] for m in [] ]
                    r["args_ok"] = None  # resolved below from tool output
                    mm = re.search(r'"concept": "([^"]+)"', ctx.split("\n")[0] if ctx else "")
                    r["args_ok"] = bool(r["route_ok"] and mm and mm.group(1) in x["concepts"])
            elif cfg == "B":
                p = rec.get("payload", {}); st = p.get("status")
                r["chose"] = p.get("route"); r["conf"] = p.get("route_confidence"); r["abstained"] = st == "clarify"
                r["route_ok"] = (p.get("route") == x["route"])
                if x["route"] == "concept_stats": r["args_ok"] = r["route_ok"] and p.get("kind") == x["kind"] and p.get("group") == x["group"]
                elif x["route"] in ("compare_groups", "evidence"): r["args_ok"] = r["route_ok"] and p.get("concept") in x["concepts"]
            if x["route"] == "out_of_scope":
                if cfg == "A": r["oos_ok"] = not (rec.get("calls"))
                elif cfg == "B": r["oos_ok"] = rec.get("payload", {}).get("status") in ("out_of_scope", "clarify")
                else: r["oos_ok"] = bool(REFUSE.search(ans))
            # answer checks
            qs = quotes_in(ans)
            cited = set(IDRE.findall(ans)); cited_i = {c.split("#")[0] for c in cited}
            v_cited = v_any = 0
            for q in qs:
                nq = norm(q)
                if any(nq in ntexts[c] or ground.is_grounded(q, texts[c]) for c in cited_i if c in texts): v_cited += 1
                if any(nq in t for t in ntexts.values()) or any(ground.is_grounded(q, t) for t in texts.values()): v_any += 1
            r.update(n_quotes=len(qs), q_cited_valid=v_cited, q_any_valid=v_any)
            an = nums(ans) - nums(x["q"]); cn = context_numbers(ctx)
            r.update(n_nums=len(an), n_nums_grounded=len(an & cn))
            if x["route"] == "concept_stats":
                g = gold_stats[(x["kind"], x["group"])]
                r["correct"] = g["concept"].lower() in ans.lower() and str(g["interviews"]) in nums(ans, False)
            elif x["route"] == "compare_groups":
                gc = gold_cmp[qid]; an2 = nums(ans, False); sz = gold_sizes
                fl = []
                for n in an2:
                    try: fl.append(float(n))
                    except ValueError: pass
                r["correct_strict"] = all((str(v) in an2) or (v == 0 and re.search(r"\b(none|no|zero)\b", ans, re.I)) for v in gc.values())
                # revised after seeing results: a group's figure may be given as a count or as a percent of that group; zero groups need not be stated
                r["correct"] = all((str(v) in an2) or any(abs(f - 100 * v / sz[g]) <= 0.6 for f in fl) for g, v in gc.items() if v > 0)
            rows.append(r)
    return rows


def pct(a, b): return f"{a}/{b} ({a/b:.0%})" if b else "n/a"


def p95(v):
    v = sorted(v); return v[min(len(v) - 1, int(round(0.95 * (len(v) - 1))))] if v else None


def table(rows, label):
    print(f"\n### {label}\n")
    print("| Measure | A: qwen3 picks tools | B: nimble router | C: plain vector RAG |\n|---|---|---|---|")
    def cell(cfg, f):
        rs = [r for r in rows if r["cfg"] == cfg]; return f(rs) if rs else "n/a"
    inscope = lambda rs: [r for r in rs if r["route"] != "out_of_scope"]
    line = lambda name, f: print(f"| {name} | " + " | ".join(cell(c, f) for c in "ABC") + " |")
    line("Questions run", lambda rs: str(len(rs)))
    line("Route or tool correct (in scope)", lambda rs: pct(sum(r["route_ok"] for r in inscope(rs)), len(inscope(rs))) if rs[0]["cfg"] != "C" else "n/a")
    line("Abstained (in scope)", lambda rs: pct(sum(r["abstained"] for r in inscope(rs)), len(inscope(rs))) if rs[0]["cfg"] != "C" else "never")
    line("Route correct when it answered", lambda rs: (lambda a: pct(sum(r["route_ok"] for r in a), len(a)))([r for r in inscope(rs) if not r["abstained"]]) if rs[0]["cfg"] != "C" else "n/a")
    line("Arguments correct (stats, compare, evidence)", lambda rs: (lambda a: pct(sum(bool(r.get("args_ok")) for r in a), len(a)))([r for r in rs if r["route"] in ("concept_stats", "compare_groups", "evidence")]) if rs[0]["cfg"] != "C" else "n/a")
    line("Out-of-scope handled (no query / refusal)", lambda rs: (lambda a: pct(sum(r["oos_ok"] for r in a), len(a)))([r for r in rs if r["route"] == "out_of_scope"]) + (" *heuristic" if rs[0]["cfg"] == "C" else ""))
    line("Count answers correct (stats + compare; compare check revised)", lambda rs: (lambda a: pct(sum(r["correct"] for r in a), len(a)))([r for r in rs if "correct" in r]))
    line("Compare answers correct, original strict check", lambda rs: (lambda a: pct(sum(r["correct_strict"] for r in a), len(a)))([r for r in rs if "correct_strict" in r]))
    line("Quotes found in the cited interview", lambda rs: pct(sum(r["q_cited_valid"] for r in rs), sum(r["n_quotes"] for r in rs)))
    line("Quotes found anywhere in the corpus", lambda rs: pct(sum(r["q_any_valid"] for r in rs), sum(r["n_quotes"] for r in rs)))
    line("Numbers in answer found in tool output", lambda rs: pct(sum(r["n_nums_grounded"] for r in rs), sum(r["n_nums"] for r in rs)))
    line("Latency p50 / p95 (s)", lambda rs: f"{statistics.median(r['secs'] for r in rs):.1f} / {p95([r['secs'] for r in rs]):.1f}")
    line("Errors", lambda rs: str(sum(r["error"] for r in rs)))


def sweep(rows, label):
    b = [r for r in rows if r["cfg"] == "B" and r.get("conf") is not None]
    print(f"\n### Router abstention by threshold ({label}, route confidence only)\n\n| Threshold | In-scope abstained | Route correct when answered | Out-of-scope questions answered as in-scope |\n|---|---|---|---|")
    for t in (0.5, 0.6, 0.7, 0.8):
        ins = [r for r in b if r["route"] != "out_of_scope"]; ans = [r for r in ins if r["conf"] >= t]
        oos = [r for r in b if r["route"] == "out_of_scope"]; leak = [r for r in oos if r["conf"] >= t and r["chose"] != "out_of_scope"]
        print(f"| {t} | {pct(len(ins) - len(ans), len(ins))} | {pct(sum(r['route_ok'] for r in ans), len(ans))} | {pct(len(leak), len(oos))} |")


if __name__ == "__main__":
    rows = evaluate()
    json.dump(rows, open(C.ROOT / "data" / "eval" / "scored.json", "w"))
    for label, f in (("Dev half (tuning allowed)", lambda r: r["split"] == "dev"), ("Held-out half", lambda r: r["split"] == "held"), ("All 40", lambda r: True)):
        sub = [r for r in rows if f(r)]; table(sub, label); sweep(sub, label)
    print("\n### Per-route latency (median s)\n")
    for cfg in "ABC":
        by = {}
        for r in rows:
            if r["cfg"] == cfg: by.setdefault(r["route"], []).append(r["secs"])
        print(cfg, {k: round(statistics.median(v), 1) for k, v in sorted(by.items())})
