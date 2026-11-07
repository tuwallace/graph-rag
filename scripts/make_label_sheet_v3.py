"""Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-ignored: contains transcript text).
Usage: PYTHONPATH=src uv run python scripts/make_label_sheet_v3.py"""
import csv, json, random, pandas as pd
from graphrag import config as C
from graphrag.parse import segments
from graphrag.ground import locate

OUT = C.ROOT / "data" / "labeling_v3"; OUT.mkdir(parents=True, exist_ok=True)
tx, grp = {}, {}
for s in C.SPLITS:
    d = pd.read_csv(C.RAW / f"{s}.csv")
    for t, x in zip(d.transcript_id, d.text): tx[t] = x; grp[t] = s
items = []
for l in open(C.ROOT / "data/artefacts/m2_v3.2.jsonl"):
    r = json.loads(l)
    for it in r["extraction"]["items"]: items.append((r["transcript_id"], it))
random.seed(3206); samp = random.sample(items, 100); random.shuffle(samp)
with open(OUT / "edges_to_label.csv", "w", newline="") as f, open(OUT / "edges_key.csv", "w", newline="") as g:
    w, k = csv.writer(f), csv.writer(g)
    w.writerow(["id", "interview", "kind", "name", "status", "polarity", "quote", "interviewer_question", "participant_answer", "label", "note"])
    k.writerow(["id", "interview", "group", "grounded_auto", "ground_score"])
    for i, (tid, it) in enumerate(samp, 1):
        segs = segments(tx[tid]); idx = it.get("segment_idx")
        if idx is None: idx, _ = locate(it["quote"], segs)
        sg = segs[idx] if idx is not None else {"question": "(not found)", "answer": "(quote not found in one answer)"}
        w.writerow([i, tid, it["kind"], it["name"].replace("_", " "), it["status"], it["polarity"], it["quote"], sg["question"][:400], sg["answer"][:900], "", ""])
        k.writerow([i, tid, grp[tid], it["grounded"], it["ground_score"]])
print("wrote", len(samp), "edges to", OUT)
