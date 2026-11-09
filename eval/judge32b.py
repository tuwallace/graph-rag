"""Independent checks by a larger model (qwen2.5:32b, run alone), so the 8B extractor and the nimble verifier do not grade themselves.
Stages (resumable, outputs in data/eval/judge/):
  precision  - 90 kept edges (30 per kind) + 30 rejected edges, labelled correct / hypothetical / wrong
  recall     - 10 transcripts: the judge lists what the participant says; then says whether the kept edges cover each item
  questions  - 8 new questions per route written from route descriptions only (the writer has not seen the graph)
Run: PYTHONPATH=src:. uv run python eval/judge32b.py [precision|recall|questions|all]
Still model-judged: a human check of a subsample is needed to trust the labels (see docs/07 'Open items').
"""
import json, os, random, sys, time, pathlib
import ollama
from graphrag import config as C
from graphrag.parse import segments as parse_segments, user_text
from graphrag.pipeline import select, unload

MODEL = "qwen2.5:32b-instruct-q4_K_M"
OUT = C.ROOT / "data" / "eval" / "judge"; OUT.mkdir(parents=True, exist_ok=True)
RUN = C.ROOT / "data" / "artefacts" / "demo1"
CLIENT = ollama.Client(host=C.OLLAMA_URL, timeout=900)


def ask(prompt, num_predict=600, temperature=0.0, seed=1):
    r = CLIENT.chat(model=MODEL, messages=[{"role": "user", "content": prompt}], format="json",
                    options={"temperature": temperature, "num_predict": num_predict, "seed": seed})
    try:
        return json.loads(r.message.content)
    except json.JSONDecodeError:
        return {}


def load_records():
    texts = {tid: (sp, t) for sp, tid, t in select("demo")}
    recs = [json.loads(l) for l in open(RUN / "graph_input.jsonl")]
    return texts, recs


def done_ids(path):
    return {json.loads(l)["key"] for l in open(path)} if path.exists() else set()


def precision():
    texts, recs = load_records(); rnd = random.Random(11)
    pool = {"kept": {k: [] for k in ("ai_use", "work_task", "concern")}, "rejected": []}
    for r in recs:
        segs = {s["idx"]: s for s in parse_segments(texts[r["transcript_id"]][1])}
        for i, e in enumerate(r["edges"]):
            if e["segment_idx"] is None or e["segment_idx"] not in segs: continue
            item = {"key": f'{r["transcript_id"]}:{i}', "group": r["group"], "kind": e["kind"], "name": e["canonical"], "quote": e["quote"],
                    "status": e["status"], "polarity": e["polarity"], "supports": e["verify"]["supports"], "keep": e["keep"],
                    "question": segs[e["segment_idx"]]["question"], "answer": segs[e["segment_idx"]]["answer"]}
            (pool["kept"][e["kind"]] if e["keep"] else pool["rejected"]).append(item)
    sample = [x for k in pool["kept"].values() for x in rnd.sample(k, 30)] + rnd.sample(pool["rejected"], 30)
    path = OUT / "precision.jsonl"; done = done_ids(path)
    claim = {"work_task": "The participant does this work: {n}.", "ai_use": "The participant uses, tries or deliberately avoids AI for: {n}.",
             "concern": "The participant is worried, frustrated or distrustful about AI because of: {n}."}
    for j, x in enumerate(sample, 1):
        if x["key"] in done: continue
        p = (f"You are a strict annotator checking one fact extracted from an interview.\n\nInterviewer: {x['question'][:600]}\nParticipant: {x['answer'][:1800]}\n\n"
             f"Extracted claim: {claim[x['kind']].format(n=x['name'])}\nEvidence quote: \"{x['quote']}\"\n\n"
             'Label the claim: "correct" = the participant says this about themselves as something they do, use, avoid or feel now or recently; '
             '"hypothetical" = it is only a wish, prediction, "if", something about other people, or something they stopped doing; '
             '"wrong" = the answer does not say this (a different idea, the opposite, or a stretch). '
             'Return JSON {"label": "correct|hypothetical|wrong", "reason": "<one short sentence>"}.')
        a = ask(p, 200); t = time.time()
        rec = {"key": x["key"], "group": x["group"], "kind": x["kind"], "keep": x["keep"], "supports": x["supports"], "label": a.get("label"), "reason": a.get("reason")}
        open(path, "a").write(json.dumps(rec) + "\n"); print(f"[precision {j}/{len(sample)}] {rec['label']}", flush=True)


def recall():
    texts, recs = load_records(); rnd = random.Random(5)
    by = {r["transcript_id"]: r for r in recs}
    ids = []
    for g, n in (("workforce", 4), ("creatives", 3), ("scientists", 3)):
        ids += rnd.sample([t for t, (sp, _) in texts.items() if sp == g], n)
    path = OUT / "recall.jsonl"; done = done_ids(path)
    for j, tid in enumerate(ids, 1):
        if tid in done: continue
        ut = user_text(texts[tid][1])[:9000]
        listed = ask("Below is everything a participant said in an interview about using AI. List what they themselves say, as short noun phrases, in three groups: "
                     '"ai_uses" (things they use, try or avoid AI for), "tasks" (work tasks they do), "concerns" (worries, frustrations or distrust about AI). '
                     "Include only things they state about themselves, not wishes, predictions or other people. At most 12 per group. "
                     'Return JSON {"ai_uses": [], "tasks": [], "concerns": []}.\n\nParticipant:\n' + ut, 700)
        items = [(k, v) for k in ("ai_uses", "tasks", "concerns") for v in (listed.get(k) or []) if isinstance(v, str)]
        kept = sorted({e["canonical"] for e in by[tid]["edges"] if e["keep"]})
        cov = ask("An extraction system produced this list of concepts for an interview:\n" + "\n".join(f"- {k}" for k in kept) +
                  "\n\nFor each item below, say whether one of the extracted concepts means essentially the same thing (a near-synonym or a slightly broader or narrower version counts). "
                  'Return JSON {"results": [{"item": "<item>", "covered": true|false}]} in the same order.\n\nItems:\n' + "\n".join(f"- {v}" for _, v in items), 900) if items and kept else {}
        res = [x for x in (cov.get("results") or []) if isinstance(x, dict)]
        rec = {"key": tid, "group": texts[tid][0], "n_items": len(items), "n_covered": sum(bool(x.get("covered")) for x in res), "n_judged": len(res), "n_kept": len(kept),
               "items": items, "results": res}
        open(path, "a").write(json.dumps(rec) + "\n"); print(f"[recall {j}/{len(ids)}] listed {len(items)} covered {rec['n_covered']}/{rec['n_judged']} extracted {len(kept)}", flush=True)


ROUTES = {
    "local_search": "asking what participants said about a topic or how a kind of person uses AI (an open question answered by reading a few answers)",
    "concept_stats": "asking to count or rank what participants mentioned: AI uses, work tasks or concerns, overall or within one group (workforce, creatives, scientists)",
    "compare_groups": "asking to compare how the workforce, creatives and scientists groups differ on one specific topic",
    "theme_overview": "asking for the overall themes or a big-picture summary of the interviews",
    "evidence": "asking to see quotes or examples about one specific thing",
    "out_of_scope": "unrelated to the interviews at all (arithmetic, trivia, greetings, coding help, translation)",
}


def questions():
    path = OUT / os.environ.get("QFILE", "questions.json"); seed = int(os.environ.get("QSEED", "3"))
    if path.exists(): return
    out = []
    for route, desc in ROUTES.items():
        a = ask("A dataset holds interviews in which workers, creative professionals and scientists describe how they use AI at work, what tasks they do and what worries them. "
                f"Write 8 different, natural questions that a user might type to a chat assistant over this dataset, each {desc}. Vary the wording and length; do not name the dataset or mention the type of question. "
                + ('For each, also give "kind" (ai_use, task or concern) and "group" (all, workforce, creatives or scientists) that the question asks about. ' if route == "concept_stats" else "")
                + 'Return JSON {"questions": [{"q": "...", ' + ('"kind": "...", "group": "..."' if route == "concept_stats" else '') + "}]}.", 1200, temperature=0.9, seed=seed)
        for i, x in enumerate(a.get("questions") or []):
            if isinstance(x, dict) and isinstance(x.get("q"), str):
                out.append({"id": f"{os.environ.get('QPREFIX', 'g')}_{route}_{i}", "route": route, "q": x["q"].strip(), "kind": x.get("kind"), "group": x.get("group")})
        print(f"[questions {route}] {sum(o['route'] == route for o in out)}", flush=True)
    path.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    which = sys.argv[1:] or ["all"]
    for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
    for name, fn in (("questions", questions), ("precision", precision), ("recall", recall)):
        if "all" in which or name in which: fn()
    unload(MODEL)
