"""Sampled check of entity normalisation (final graph), judged by qwen2.5:32b run alone. Model-judged.
  merges  : 80 raw-name -> canonical merges (20 each from ai_use, work_task, concern from the original pass, concern from the loose pass), judged same / related / different.
  missed  : 40 pairs of distinct canonical names of the same kind with cosine 0.75 to 0.85 (just under the 0.85 merge threshold), judged same / related / different.
Output data/eval/final/normalisation.json. Run: PYTHONPATH=src:. uv run python eval/normalisation_check.py [prepare|judge]   (prepare needs the small embedding model; judge needs the 32b alone)
"""
import json, random, sys, collections
import numpy as np
from graphrag import config as C, normalise as N
from graphrag.pipeline import unload

RUN = C.ROOT / "data" / "artefacts" / "demo1"; OUT = C.ROOT / "data" / "eval" / "final"; OUT.mkdir(parents=True, exist_ok=True)
MODEL = "qwen2.5:32b-instruct-q4_K_M"


def prepare():
    table = json.load(open(RUN / "normalise.json"))["mapping"]
    new_raw = set()
    canon = {"ai_use": set(), "work_task": set(), "concern": set()}
    for l in open(RUN / "graph_input.jsonl"):
        for e in json.loads(l)["edges"]:
            if e["keep"]:
                canon[e["kind"]].add(e["canonical"])
                if e.get("prompt_version") == "concern-loose-v1": new_raw.add(N.clean(e["raw_name"]))
    rnd = random.Random(5); merges = []
    for kind, tag in (("ai_use", "ai_use"), ("work_task", "work_task"), ("concern", "concern_original"), ("concern", "concern_loose")):
        pool = [(r, c) for r, c in table[kind].items() if r != c and c in canon[kind] and ((r in new_raw) == (tag == "concern_loose"))]
        merges += [{"stratum": tag, "kind": kind, "raw": r, "canonical": c} for r, c in rnd.sample(pool, min(20, len(pool)))]
    pairs = []
    for kind, names in canon.items():
        names = sorted(names); v = N.embed(names); sims = v @ v.T; iu = np.triu_indices(len(names), 1)
        mask = (sims[iu] >= 0.75) & (sims[iu] < 0.85)
        idx = np.flatnonzero(mask)
        pairs += [{"kind": kind, "a": names[iu[0][k]], "b": names[iu[1][k]], "sim": round(float(sims[iu][k]), 3), "pool": int(mask.sum())} for k in idx]
    by = collections.defaultdict(list)
    for p in pairs: by[p["kind"]].append(p)
    pools = {k: len(v) for k, v in by.items()}
    tot = sum(pools.values()); sample = []
    for k, v in by.items(): sample += rnd.sample(v, min(len(v), max(1, round(40 * len(v) / tot))))
    json.dump({"merges": merges, "pairs": sample, "near_miss_pool": pools}, open(OUT / "normalisation_sample.json", "w"), indent=1)
    print(len(merges), "merges;", len(sample), "near-miss pairs; pool sizes", pools)


def judge():
    import ollama
    for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)
    s = json.load(open(OUT / "normalisation_sample.json")); client = ollama.Client(host=C.OLLAMA_URL, timeout=900)

    def ask(a, b):
        p = (f'Two short phrases come from interviews about how people use AI at work.\nPhrase A: "{a}"\nPhrase B: "{b}"\n\n'
             'Label: "same" = a reader would treat them as the same idea (a rewording, plural or near-synonym); "related" = clearly connected but one is broader, narrower or a different aspect; '
             '"different" = different ideas. Return JSON {"label": "same|related|different"}.')
        r = client.chat(model=MODEL, messages=[{"role": "user", "content": p}], format="json", options={"temperature": 0, "num_predict": 40, "num_ctx": 2048, "seed": 1})
        try: return json.loads(r.message.content).get("label")
        except json.JSONDecodeError: return None
    for m in s["merges"]: m["label"] = ask(m["raw"], m["canonical"]); print("merge", m["stratum"], m["label"], flush=True)
    for p in s["pairs"]: p["label"] = ask(p["a"], p["b"]); print("pair", p["kind"], p["label"], flush=True)
    summ = {"merges": {}, "near_miss": {}}
    for st in sorted({m["stratum"] for m in s["merges"]}):
        c = collections.Counter(m["label"] for m in s["merges"] if m["stratum"] == st); summ["merges"][st] = dict(c)
    c = collections.Counter(m["label"] for m in s["merges"]); summ["merges"]["all"] = dict(c)
    for k in sorted({p["kind"] for p in s["pairs"]}):
        summ["near_miss"][k] = dict(collections.Counter(p["label"] for p in s["pairs"] if p["kind"] == k))
    summ["near_miss"]["all"] = dict(collections.Counter(p["label"] for p in s["pairs"])); summ["near_miss_pool"] = s["near_miss_pool"]
    json.dump({"sample": s, "summary": summ}, open(OUT / "normalisation.json", "w"), indent=1); print(json.dumps(summ, indent=1))
    unload(MODEL)


if __name__ == "__main__":
    for st in (sys.argv[1:] or ["prepare", "judge"]): {"prepare": prepare, "judge": judge}[st]()
