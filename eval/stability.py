"""Run-to-run stability (final graph). Model-dependent steps are repeated with small perturbations and compared with the stored result.
  router   : the 60 labelled questions (eval/questions.json + confirm_questions.json) routed as-is, lowercased, with 'Please ' in front and ' Thanks.' behind
             (nimble caches identical requests, so exact repeats are not informative). Reports route agreement with the as-is route, confidence change, and gold accuracy.
  extract  : the 10 recall transcripts re-extracted with the production prompt (v3.3): twice at temperature 0 and twice at temperature 0.3 (seeds 1, 2).
             Compares the set of (kind, quote) items with the stored production extraction.
  judge    : 40 of the 120 edges labelled by qwen2.5:32b in data/eval/judge/precision.jsonl, relabelled at temperature 0.3 with a different seed. Run alone.
Outputs data/eval/final/stability_<step>.json. Run: PYTHONPATH=src:. uv run python eval/stability.py [router|extract|judge]
"""
import json, random, sys, statistics, collections, pathlib
import ollama
from graphrag import config as C, extract as X, router
from graphrag.parse import segments as parse_segments
from graphrag.pipeline import select, unload

HERE = pathlib.Path(__file__).parent; OUT = C.ROOT / "data" / "eval" / "final"; OUT.mkdir(parents=True, exist_ok=True)
RUN = C.ROOT / "data" / "artefacts" / "demo1"


def do_router():
    qs = json.loads((HERE / "questions.json").read_text()) + json.loads((HERE / "confirm_questions.json").read_text())
    variants = {"as_is": lambda q: q, "lower": lambda q: q.lower(), "please": lambda q: "Please " + q[0].lower() + q[1:], "thanks": lambda q: q + " Thanks."}
    res = {v: [router.route_question(f(x["q"])) for x in qs] for v, f in variants.items()}
    out = {"n": len(qs), "variants": {}}
    for v in variants:
        agree = sum(a["route"] == b["route"] for a, b in zip(res["as_is"], res[v]))
        dconf = statistics.mean(abs(a["confidence"] - b["confidence"]) for a, b in zip(res["as_is"], res[v]))
        gold = [x["route"] for x in qs]
        acc = sum(r["route"] == g for r, g in zip(res[v], gold) if g != "out_of_scope"); n = sum(g != "out_of_scope" for g in gold)
        low = sum(r["confidence"] < router.MIN_CONFIDENCE for r in res[v])
        out["variants"][v] = {"agree_with_as_is": agree, "mean_abs_conf_change": round(dconf, 3), "in_scope_route_correct": f"{acc}/{n}", "below_gate": low}
    json.dump(out, open(OUT / "stability_router.json", "w"), indent=1); print(json.dumps(out, indent=1))


def items_of(data):
    return {(it["kind"], X._nq(it["quote"])) for it in data.get("items", []) if it.get("grounded", True)}


def do_extract():
    texts = {tid: t for _, tid, t in select("demo")}
    keys = [json.loads(l)["key"] for l in open(C.ROOT / "data" / "eval" / "judge" / "recall.jsonl")]
    base = {}
    for l in open(RUN / "extract.jsonl"):
        r = json.loads(l)
        if r["key"] in keys: base[r["key"]] = {(it["kind"], X._nq(it["quote"])) for it in r["items"] if it["grounded"]}
    client = ollama.Client(host=C.OLLAMA_URL, timeout=900); rows = []
    from graphrag.ground import score, THRESHOLD
    from graphrag.parse import user_text
    for tid in keys:
        ut = user_text(texts[tid]); runs = {}
        for name, temp, seed in (("t0_a", 0, 1), ("t0_b", 0, 1), ("t03_a", 0.3, 1), ("t03_b", 0.3, 2)):
            r = client.chat(model=C.GEN_MODEL, messages=[{"role": "user", "content": X.build_prompt(texts[tid])}], format=X.SCHEMA, think=False,
                            options={"temperature": temp, "seed": seed, "num_ctx": 16384, "num_predict": X.MAX_NEW_TOKENS})
            try: d = json.loads(r["message"]["content"])
            except Exception: d = {"items": []}
            its = X.dedupe(d.get("items", []))
            runs[name] = {(i["kind"], X._nq(i["quote"])) for i in its if score(i["quote"], ut) >= THRESHOLD}
        jac = lambda a, b: len(a & b) / len(a | b) if a | b else 1.0
        rows.append({"key": tid, "base": len(base[tid]), **{n: len(s) for n, s in runs.items()},
                     "jac_base_t0a": jac(base[tid], runs["t0_a"]), "jac_t0a_t0b": jac(runs["t0_a"], runs["t0_b"]),
                     "jac_base_t03a": jac(base[tid], runs["t03_a"]), "jac_t03a_t03b": jac(runs["t03_a"], runs["t03_b"])})
        print(tid, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in rows[-1].items() if k != "key"}, flush=True)
    summ = {k: round(statistics.mean(r[k] for r in rows), 3) for k in ("jac_base_t0a", "jac_t0a_t0b", "jac_base_t03a", "jac_t03a_t03b")}
    json.dump({"rows": rows, "mean_jaccard": summ}, open(OUT / "stability_extract.json", "w"), indent=1); print(summ)
    unload(C.GEN_MODEL)


def do_judge():
    from graphrag.pipeline import select as sel
    import eval.judge32b as J
    for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
    texts = {tid: t for _, tid, t in sel("demo")}
    recs = {json.loads(l)["transcript_id"]: json.loads(l) for l in open(RUN / "graph_input.v1.jsonl")}
    prior = [json.loads(l) for l in open(C.ROOT / "data" / "eval" / "judge" / "precision.jsonl")]
    sample = random.Random(3).sample(prior, 40); same = 0; rows = []
    claim = {"work_task": "The participant does this work: {n}.", "ai_use": "The participant uses, tries or deliberately avoids AI for: {n}.",
             "concern": "The participant is worried, frustrated or distrustful about AI because of: {n}."}
    for p in sample:
        tid, i = p["key"].rsplit(":", 1); e = recs[tid]["edges"][int(i)]
        s = {x["idx"]: x for x in parse_segments(texts[tid])}[e["segment_idx"]]
        q = (f"You are a strict annotator checking one fact extracted from an interview.\n\nInterviewer: {s['question'][:600]}\nParticipant: {s['answer'][:1800]}\n\n"
             f"Extracted claim: {claim[e['kind']].format(n=e['canonical'])}\nEvidence quote: \"{e['quote']}\"\n\n"
             'Label the claim: "correct" = the participant says this about themselves as something they do, use, avoid or feel now or recently; '
             '"hypothetical" = it is only a wish, prediction, "if", something about other people, or something they stopped doing; '
             '"wrong" = the answer does not say this (a different idea, the opposite, or a stretch). '
             'Return JSON {"label": "correct|hypothetical|wrong", "reason": "<one short sentence>"}.')
        r = J.CLIENT.chat(model=J.MODEL, messages=[{"role": "user", "content": q}], format="json", options={"temperature": 0.3, "seed": 7, "num_predict": 200, "num_ctx": 6144})
        try: lab = json.loads(r.message.content).get("label")
        except json.JSONDecodeError: lab = None
        rows.append({"key": p["key"], "first": p["label"], "second": lab}); same += lab == p["label"]
        print(p["key"], p["label"], lab, flush=True)
    c = collections.Counter((r["first"], r["second"]) for r in rows)
    out = {"n": len(rows), "same_label": same, "agreement": round(same / len(rows), 3), "pairs": {f"{a}->{b}": n for (a, b), n in c.items()},
           "correct_rate_first": round(sum(r["first"] == "correct" for r in rows) / len(rows), 3), "correct_rate_second": round(sum(r["second"] == "correct" for r in rows) / len(rows), 3)}
    json.dump(out, open(OUT / "stability_judge.json", "w"), indent=1); print(json.dumps(out, indent=1))
    unload(J.MODEL)


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["router", "extract", "judge"]): {"router": do_router, "extract": do_extract, "judge": do_judge}[s]()
