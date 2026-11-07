"""Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels). Usage: PYTHONPATH=src uv run python scripts/compare_m2.py"""
import json, csv, collections, statistics as st
from graphrag import config as C
from graphrag.ground import score

V3 = [json.loads(l) for l in open(C.ROOT / "data/artefacts/m2_v3.2.jsonl")]
V2 = [json.loads(l) for l in open(C.ROOT / "data/spike_extract_v2.jsonl")]
items = [(r["transcript_id"], it) for r in V3 for it in r["extraction"].get("items", [])]

print("== v3 summary ==")
n = len(items); g = sum(i["grounded"] for _, i in items)
print(f"valid json {sum(r['valid_json'] for r in V3)}/{len(V3)}; items {n} ({n/len(V3):.1f}/transcript); grounded(fuzzy, User turns) {g}/{n} = {100*g/n:.1f}%")
secs = [r["secs"] for r in V3]; print(f"secs mean {st.mean(secs):.1f} median {st.median(secs):.1f} max {max(secs):.1f}; projected 500: {500*st.mean(secs)/3600:.1f} h, 1250: {1250*st.mean(secs)/3600:.1f} h")
print("kind", dict(collections.Counter(i["kind"] for _, i in items)))
print("status", dict(collections.Counter(i["status"] for _, i in items)))
print("polarity", dict(collections.Counter(i["polarity"] for _, i in items)))
print("hygiene failures", [(r["transcript_id"], r["hygiene"]) for r in V3 if r["hygiene"]] or "none")
names = collections.Counter(i["name"].strip().lower() for _, i in items)
print(f"distinct names {len(names)} of {n}; top {names.most_common(4)}")
v2n = sum(len(r["extraction"].get(k, [])) for r in V2 for k in ("tasks", "ai_uses", "concerns"))
print(f"(v2 had {v2n} items)")

print("\n== known v2 errors (my labels) vs v3 ==")
KIND_ERR = {1, 30, 59, 75, 80, 83, 87, 89, 97, 99}
rows = list(csv.DictReader(open(C.ROOT / "data/labeling_claude/edges_to_label.csv")))
KMAP = {"task": "work_task", "ai_use": "ai_use", "concern": "concern"}
def match(row):
    best, bs = None, 0.0
    for tid, it in items:
        if tid != row["interview"]: continue
        s = score(row["quote"], it["quote"])
        if s > bs: best, bs = it, s
    return (best, bs) if bs >= 0.8 else (None, bs)
tally = collections.Counter()
for r in rows:
    lab = r["label"]; it, s = match(r); i = int(r["id"])
    if lab == "ok":
        if it is None: tally["ok:dropped"] += 1
        elif it["status"] == "current" and it["polarity"] == "affirmed": tally["ok:kept"] += 1
        else: tally["ok:now-flagged"] += 1; print(f"  REGRESSION? #{i} ok -> v3 {it['kind']}/{it['status']}/{it['polarity']} '{it['name']}'")
        continue
    why = "kind" if i in KIND_ERR else ("hypo" if lab == "hypo" else "other-wrong")
    if it is None:
        tally[f"{why}:dropped"] += 1; res = "DROPPED"
    else:
        res = f"{it['kind']}/{it['status']}/{it['polarity']} '{it['name']}'"
        flagged = it["status"] != "current" or it["polarity"] == "negated"
        if why == "kind": tally[f"{why}:{'same-kind' if it['kind'] == KMAP[r['kind']] else 'kind-changed'}"] += 1
        else: tally[f"{why}:{'flagged' if flagged else 'unchanged'}"] += 1
    print(f"  #{i:>3} {lab:5} [{why}] v2 {r['kind']} '{r['extracted_name']}'  ->  {res}")
print("\n", dict(sorted(tally.items())))
