"""Re-measure recall on the 10 transcripts of eval/judge32b.py recall, against the original graph input (graph_input.v1.jsonl) and the current one,
with the same coverage prompt, judged twice by qwen2.5:32b (run alone) so judge variation is controlled. Items are the ones the judge listed earlier
(data/eval/judge/recall.jsonl). Model-judged. Output: data/eval/recall_remeasure.json.
Run: PYTHONPATH=src:. uv run python eval/recall_remeasure.py
"""
import json, collections
import ollama
from graphrag import config as C
from graphrag.pipeline import unload

MODEL = "qwen2.5:32b-instruct-q4_K_M"; RUN = C.ROOT / "data" / "artefacts" / "demo1"
client = ollama.Client(host=C.OLLAMA_URL, timeout=900)


def cover(concepts, items):
    if not items or not concepts: return [False] * len(items)
    p = ("An extraction system produced this list of concepts for an interview:\n" + "\n".join(f"- {k}" for k in concepts) +
         "\n\nFor each item below, say whether one of the extracted concepts means essentially the same thing (a near-synonym or a slightly broader or narrower version counts). "
         'Return JSON {"results": [{"item": "<item>", "covered": true|false}]} in the same order.\n\nItems:\n' + "\n".join(f"- {v}" for v in items))
    r = client.chat(model=MODEL, messages=[{"role": "user", "content": p}], format="json", options={"temperature": 0, "num_predict": 900, "num_ctx": 6144, "seed": 1})
    try: res = [bool(x.get("covered")) for x in json.loads(r.message.content).get("results", []) if isinstance(x, dict)]
    except json.JSONDecodeError: res = []
    return (res + [False] * len(items))[:len(items)]


def kept(path):
    return {json.loads(l)["transcript_id"]: sorted({e["canonical"] for e in json.loads(l)["edges"] if e["keep"]}) for l in open(path)}


if __name__ == "__main__":
    for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
    old, new = kept(RUN / "graph_input.v1.jsonl"), kept(RUN / "graph_input.jsonl")
    rec = [json.loads(l) for l in open(C.ROOT / "data" / "eval" / "judge" / "recall.jsonl")]
    tot = collections.Counter(); rows = []
    for j, r in enumerate(rec, 1):
        kinds = [k for k, _ in r["items"]]; items = [v for _, v in r["items"]]
        a, b = cover(old[r["key"]], items), cover(new[r["key"]], items)
        for k, x, y in zip(kinds, a, b):
            tot[(k, "n")] += 1; tot[(k, "old")] += x; tot[(k, "new")] += y; tot[("all", "n")] += 1; tot[("all", "old")] += x; tot[("all", "new")] += y
        rows.append({"key": r["key"], "group": r["group"], "n": len(items), "old": sum(a), "new": sum(b), "kept_old": len(old[r["key"]]), "kept_new": len(new[r["key"]])})
        print(f"[{j}/10] items {len(items)} old {sum(a)} new {sum(b)}", flush=True)
    out = {"rows": rows, "totals": {f"{k}|{s}": v for (k, s), v in tot.items()}}
    json.dump(out, open(C.ROOT / "data" / "eval" / "recall_remeasure.json", "w"), indent=1)
    for k in ("all", "ai_uses", "tasks", "concerns"):
        n = tot[(k, "n")]; print(f"{k}: n {n} old {tot[(k,'old')]} ({tot[(k,'old')]/n:.0%}) new {tot[(k,'new')]} ({tot[(k,'new')]/n:.0%})")
    unload(MODEL)
