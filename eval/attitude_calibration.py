"""Attitude labels vs a larger model, and confidence calibration (final graph). Model-judged: this measures agreement of the `nimble` per-segment attitude
(positive / negative / mixed / none, with a confidence) with qwen2.5:32b run alone on the same criteria, not agreement with a human.
Sample: 160 segments, 40 per predicted attitude (negative has 293 in the graph). Output data/eval/final/attitude.json.
Run: PYTHONPATH=src:. uv run python eval/attitude_calibration.py
"""
import json, random, collections
import ollama
from graphrag import config as C
from graphrag.parse import segments as parse_segments
from graphrag.pipeline import select, unload
from graphrag.attributes import ATTITUDE

MODEL = "qwen2.5:32b-instruct-q4_K_M"; RUN = C.ROOT / "data" / "artefacts" / "demo1"; OUT = C.ROOT / "data" / "eval" / "final"; OUT.mkdir(parents=True, exist_ok=True)
for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
texts = {tid: t for _, tid, t in select("demo")}
pool = collections.defaultdict(list)
for l in open(RUN / "graph_input.jsonl"):
    r = json.loads(l)
    for s in r["segments"]: pool[s["attitude"]].append((r["transcript_id"], s))
rnd = random.Random(9); sample = [(a, tid, s) for a in ("positive", "negative", "mixed", "none") for tid, s in rnd.sample(pool[a], 40)]
client = ollama.Client(host=C.OLLAMA_URL, timeout=900); crit = "\n".join(f'- "{k}": {v}' for k, v in ATTITUDE["criteria"].items()); rows = []
for j, (a, tid, s) in enumerate(sample, 1):
    seg = {x["idx"]: x for x in parse_segments(texts[tid])}[s["idx"]]
    p = (f"Interviewer: {seg['question'][:600]}\nParticipant: {seg['answer'][:1800]}\n\n{ATTITUDE['instructions']}\nChoose exactly one:\n{crit}\n"
         'Return JSON {"attitude": "positive|negative|mixed|none"}.')
    r = client.chat(model=MODEL, messages=[{"role": "user", "content": p}], format="json", options={"temperature": 0, "num_predict": 40, "num_ctx": 6144, "seed": 1})
    try: lab = json.loads(r.message.content).get("attitude")
    except json.JSONDecodeError: lab = None
    rows.append({"key": f"{tid}#{s['idx']}", "pred": a, "conf": s["attitude_conf"], "judge": lab}); print(j, a, s["attitude_conf"], lab, flush=True)
n = len(rows); acc = sum(r["pred"] == r["judge"] for r in rows) / n
conf = collections.Counter((r["pred"], r["judge"]) for r in rows)
per = {a: round(sum(r["judge"] == a for r in rows if r["pred"] == a) / 40, 3) for a in ("positive", "negative", "mixed", "none")}
bins = [(0, 0.6), (0.6, 0.8), (0.8, 0.95), (0.95, 1.01)]; cal = []
for lo, hi in bins:
    b = [r for r in rows if lo <= r["conf"] < hi]
    if b: cal.append({"conf_range": f"{lo}-{min(hi,1.0)}", "n": len(b), "mean_conf": round(sum(r["conf"] for r in b) / len(b), 3), "agreement": round(sum(r["pred"] == r["judge"] for r in b) / len(b), 3)})
ece = sum(c["n"] * abs(c["mean_conf"] - c["agreement"]) for c in cal) / n
out = {"n": n, "agreement": round(acc, 3), "per_predicted_class_agreement": per, "confusion_pred_judge": {f"{a}->{b}": v for (a, b), v in sorted(conf.items(), key=lambda kv: -kv[1])},
       "calibration": cal, "ece": round(ece, 3), "graph_distribution": {a: len(v) for a, v in pool.items()}}
json.dump({"summary": out, "rows": rows}, open(OUT / "attitude.json", "w"), indent=1); print(json.dumps(out, indent=1)); unload(MODEL)
