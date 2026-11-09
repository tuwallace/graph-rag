"""Second extraction pass for concerns with a looser prompt, on the 10 transcripts used for the recall check (data/eval/judge/recall.jsonl).
Stages (resumable, outputs in data/eval/concern_pass/): extract (qwen3 8b), verify (nimble, same VERIFY_MIN), judge (qwen2.5:32b alone).
The judge stage re-uses the concern items the judge already listed for these transcripts, and re-judges coverage twice with identical code:
against the original kept concepts, and against original + new concern edges. It also labels every new edge (correct / hypothetical / wrong).
Run: PYTHONPATH=src:. uv run python eval/concern_pass.py [extract|verify|judge|all]
Model-judged, one run each, 10 transcripts: small and noisy.
"""
import json, sys, time, pathlib
import ollama
from graphrag import config as C, extract as X, verify as V
from graphrag.parse import segments as parse_segments, user_text
from graphrag.pipeline import select, unload, VERIFY_MIN
from graphrag.ground import score, locate, THRESHOLD

OUT = C.ROOT / "data" / "eval" / "concern_pass"; OUT.mkdir(parents=True, exist_ok=True)
JUDGE = C.ROOT / "data" / "eval" / "judge"
RUN = C.ROOT / "data" / "artefacts" / "demo1"
PASS_VERSION = "concern-loose-v1"

PROMPT = """You read an interview transcript about how a professional uses AI at work. Extract ONLY what the participant said (the "User" turns). Never use the interviewer's words.

List every concern the participant expresses about AI. Be inclusive: count worries, frustrations, distrust, doubts, limitations, risks, things AI gets wrong or cannot do, and fears about quality, accuracy, jobs, skills, dependence, privacy, ethics, fairness, creativity or human connection. Brief, indirect and general remarks count, and so do concerns about the future or about other people.

Each item has:
- kind: always "concern".
- name: a short lowercase noun phrase that restates what the quote itself complains about or fears; do not name a broader theme the quote does not state.
- status: current (the participant feels or has experienced this) or not_current (a prediction, a "might" or "would", or about other people).
- polarity: affirmed, or negated if the participant says they do NOT have this concern.
- quote: an exact copied span of at most 25 words from a participant turn.

Rules: each quote is used for at most one item. Do not invent items. An empty list is fine.
Also give role_guess (job if stated, else null) and overall_attitude_to_ai.

TRANSCRIPT:
"""


def ids():
    return [json.loads(l)["key"] for l in open(JUDGE / "recall.jsonl")]


def jl(path):
    return [json.loads(l) for l in open(path)] if path.exists() else []


def extract():
    texts = {tid: (sp, t) for sp, tid, t in select("demo")}; path = OUT / "extract.jsonl"; done = {r["key"] for r in jl(path)}
    client = ollama.Client(host=C.OLLAMA_URL, timeout=900)
    for j, tid in enumerate(ids(), 1):
        if tid in done: continue
        text = texts[tid][1]; t0 = time.time()
        r = client.chat(model=C.GEN_MODEL, messages=[{"role": "user", "content": PROMPT + text}], format=X.SCHEMA, think=False,
                        options={"temperature": 0, "num_ctx": 16384, "num_predict": X.MAX_NEW_TOKENS})
        try: data = json.loads(r["message"]["content"])
        except Exception: data = {"items": []}
        items = X.dedupe([i for i in data.get("items", []) if i.get("kind") == "concern"])
        segs, ut = parse_segments(text), user_text(text)
        for it in items:
            it["ground_score"] = round(score(it["quote"], ut), 3); it["grounded"] = it["ground_score"] >= THRESHOLD
            idx, sc = locate(it["quote"], segs); it["segment_idx"] = idx if sc >= THRESHOLD else None
        open(path, "a").write(json.dumps({"key": tid, "group": texts[tid][0], "items": items, "secs": round(time.time() - t0, 1), "version": PASS_VERSION}) + "\n")
        print(f"[extract {j}/10] {tid} {len(items)} items {time.time()-t0:.0f}s", flush=True)
    unload(C.GEN_MODEL)


def verify():
    path = OUT / "verify.jsonl"; done = {r["key"] for r in jl(path)}
    for j, r in enumerate(jl(OUT / "extract.jsonl"), 1):
        if r["key"] in done: continue
        sc = [V.verify_item(it) for it in r["items"]]
        open(path, "a").write(json.dumps({"key": r["key"], "scores": sc}) + "\n"); print(f"[verify {j}/10] {r['key']} {len(sc)}", flush=True)
    unload(C.ROUTER_MODEL)


def new_edges():
    """Kept new concern edges whose quote is not already the quote of an original kept concern edge."""
    orig = {}
    for l in open(RUN / "graph_input.jsonl"):
        r = json.loads(l); orig[r["transcript_id"]] = [e for e in r["edges"] if e["keep"]]
    vr = {r["key"]: r for r in jl(OUT / "verify.jsonl")}; out = {}
    for r in jl(OUT / "extract.jsonl"):
        oq = {X._nq(e["quote"]) for e in orig[r["key"]] if e["kind"] == "concern"}
        rows = []
        for it, sc in zip(r["items"], vr[r["key"]]["scores"]):
            keep = bool(it["grounded"]) and V.keep(sc, VERIFY_MIN)
            rows.append({**it, "verify": sc, "keep": keep, "dup_of_original": X._nq(it["quote"]) in oq})
        out[r["key"]] = {"group": r["group"], "rows": rows, "orig_kept": sorted({e["canonical"] for e in orig[r["key"]]})}
    return out


def judge():
    import eval.judge32b as J
    unload(C.GEN_MODEL); unload(C.ROUTER_MODEL); unload(C.EMBED_MODEL)
    texts = {tid: (sp, t) for sp, tid, t in select("demo")}; data = new_edges(); recall = {r["key"]: r for r in jl(JUDGE / "recall.jsonl")}
    cpath, ppath = OUT / "coverage.jsonl", OUT / "precision.jsonl"; cdone = {r["key"] for r in jl(cpath)}
    for j, (tid, d) in enumerate(data.items(), 1):
        added = sorted({it["name"].strip().lower() for it in d["rows"] if it["keep"] and not it["dup_of_original"]})
        items = [v for k, v in recall[tid]["items"] if k == "concerns"]
        if tid not in cdone:
            def cov(concepts):
                if not items or not concepts: return [False] * len(items)
                a = J.ask("An extraction system produced this list of concepts for an interview:\n" + "\n".join(f"- {k}" for k in concepts) +
                          "\n\nFor each item below, say whether one of the extracted concepts means essentially the same thing (a near-synonym or a slightly broader or narrower version counts). "
                          'Return JSON {"results": [{"item": "<item>", "covered": true|false}]} in the same order.\n\nItems:\n' + "\n".join(f"- {v}" for v in items), 900)
                res = [bool(x.get("covered")) for x in (a.get("results") or []) if isinstance(x, dict)]
                return (res + [False] * len(items))[:len(items)]
            before = cov(d["orig_kept"]); after = cov(sorted(set(d["orig_kept"]) | set(added)))
            open(cpath, "a").write(json.dumps({"key": tid, "group": d["group"], "n_items": len(items), "before": sum(before), "after": sum(after), "n_added": len(added)}) + "\n")
            print(f"[coverage {j}/10] items {len(items)} before {sum(before)} after {sum(after)} added {len(added)}", flush=True)
    pdone = {r["key"] for r in jl(ppath)}
    claim = "The participant is worried, frustrated or distrustful about AI because of: {n}."
    for tid, d in data.items():
        segs = {s["idx"]: s for s in parse_segments(texts[tid][1])}
        for i, it in enumerate(d["rows"]):
            key = f"{tid}:{i}"
            if not it["keep"] or it["dup_of_original"] or key in pdone or it["segment_idx"] not in segs: continue
            s = segs[it["segment_idx"]]
            p = (f"You are a strict annotator checking one fact extracted from an interview.\n\nInterviewer: {s['question'][:600]}\nParticipant: {s['answer'][:1800]}\n\n"
                 f"Extracted claim: {claim.format(n=it['name'])}\nEvidence quote: \"{it['quote']}\"\n\n"
                 'Label the claim: "correct" = the participant says this about themselves as something they do, use, avoid or feel now or recently; '
                 '"hypothetical" = it is only a wish, prediction, "if", something about other people, or something they stopped doing; '
                 '"wrong" = the answer does not say this (a different idea, the opposite, or a stretch). '
                 'Return JSON {"label": "correct|hypothetical|wrong", "reason": "<one short sentence>"}.')
            a = J.ask(p, 200)
            open(ppath, "a").write(json.dumps({"key": key, "status": it["status"], "polarity": it["polarity"], "supports": it["verify"]["supports"], "label": a.get("label"), "reason": a.get("reason")}) + "\n")
            print(f"[precision {key}] {a.get('label')}", flush=True)
    unload(J.MODEL)


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    for name, fn in (("extract", extract), ("verify", verify), ("judge", judge)):
        if "all" in which or name in which: fn()
