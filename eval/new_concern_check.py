"""Graph-wide precision check of the concern edges added by the all-500 concern pass (prompt_version concern-loose-v1).
Random sample (seed 21) of 120 of the new edges, labelled by qwen2.5:32b (run alone) with the same prompt as eval/judge32b.py precision.
Model-judged; the owner has not labelled these. Output: data/eval/concern_pass/new_edges_precision.jsonl. Resumable.
Run: PYTHONPATH=src:. uv run python eval/new_concern_check.py
"""
import json, random, collections
import ollama
from graphrag import config as C
from graphrag.parse import segments as parse_segments
from graphrag.pipeline import select, unload

MODEL = "qwen2.5:32b-instruct-q4_K_M"; N = 120
OUT = C.ROOT / "data" / "eval" / "concern_pass" / "new_edges_precision.jsonl"
client = ollama.Client(host=C.OLLAMA_URL, timeout=900)
CLAIM = "The participant is worried, frustrated or distrustful about AI because of: {n}."


def label(p):
    r = client.chat(model=MODEL, messages=[{"role": "user", "content": p}], format="json", options={"temperature": 0, "num_predict": 200, "num_ctx": 6144, "seed": 1})
    try: return json.loads(r.message.content)
    except json.JSONDecodeError: return {}


if __name__ == "__main__":
    for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
    texts = {tid: (sp, t) for sp, tid, t in select("demo")}
    pool = []
    for l in open(C.ROOT / "data" / "artefacts" / "demo1" / "graph_input.jsonl"):
        r = json.loads(l)
        for i, e in enumerate(r["edges"]):
            if e.get("prompt_version") == "concern-loose-v1": pool.append((r["transcript_id"], r["group"], i, e))
    sample = random.Random(21).sample(pool, N)
    done = {json.loads(l)["key"] for l in open(OUT)} if OUT.exists() else set()
    print(f"pool {len(pool)}, sample {len(sample)}, done {len(done)}", flush=True)
    for j, (tid, grp, i, e) in enumerate(sample, 1):
        key = f"{tid}:{i}"
        if key in done: continue
        s = {x["idx"]: x for x in parse_segments(texts[tid][1])}[e["segment_idx"]]
        p = (f"You are a strict annotator checking one fact extracted from an interview.\n\nInterviewer: {s['question'][:600]}\nParticipant: {s['answer'][:1800]}\n\n"
             f"Extracted claim: {CLAIM.format(n=e['canonical'])}\nEvidence quote: \"{e['quote']}\"\n\n"
             'Label the claim: "correct" = the participant says this about themselves as something they do, use, avoid or feel now or recently; '
             '"hypothetical" = it is only a wish, prediction, "if", something about other people, or something they stopped doing; '
             '"wrong" = the answer does not say this (a different idea, the opposite, or a stretch). '
             'Return JSON {"label": "correct|hypothetical|wrong", "reason": "<one short sentence>"}.')
        a = label(p)
        open(OUT, "a").write(json.dumps({"key": key, "group": grp, "status": e["status"], "polarity": e["polarity"], "supports": e["verify"]["supports"], "label": a.get("label"), "reason": a.get("reason")}) + "\n")
        print(f"[{j}/{N}] {a.get('label')}", flush=True)
    unload(MODEL)
