"""Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration, not a validation: labels are one LLM rater's; see ADR-0013).
Usage: PYTHONPATH=src uv run python scripts/calibrate_verify.py"""
import csv, json, time, statistics as st
from graphrag import config as C
from graphrag.verify import verify_item

rows = list(csv.DictReader(open(C.ROOT / "data/labeling_v3/edges_to_label.csv")))
out = C.ROOT / "data/artefacts/verify_calibration.jsonl"; res = []
t0 = time.time()
for r in rows:
    v = verify_item({"kind": r["kind"], "name": r["name"], "quote": r["quote"]})
    res.append({"id": int(r["id"]), "label": r["label"], "status": r["status"], "kind": r["kind"], **v})
    print(r["id"], r["label"], v, flush=True)
json.dump(res, open(out, "w"))
secs = time.time() - t0; print(f"\n{len(res)} items in {secs:.0f}s = {secs/len(res):.2f}s per item")
ok = [x for x in res if x["label"] == "ok"]; bad = [x for x in res if x["label"] != "ok"]
def auc(key):
    pairs = [(a[key], b[key]) for a in ok for b in bad]
    return sum((1.0 if a > b else 0.5 if a == b else 0.0) for a, b in pairs) / len(pairs)
print(f"base precision {len(ok)}/{len(res)} = {len(ok)/len(res):.2f}")
print(f"AUC (ok vs not ok): supports {auc('supports'):.2f}  own_current {auc('own_current'):.2f}")
print("\nthreshold on 'supports' (alone):")
for t in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    kept = [x for x in res if x["supports"] >= t]; k_ok = sum(x["label"] == "ok" for x in kept)
    print(f"  >= {t:.1f}: kept {len(kept):3}  precision {k_ok/max(1,len(kept)):.2f}  recall of ok {k_ok/len(ok):.2f}")
print("\nsupports >= t AND own_current >= u:")
for t in [0.3, 0.5, 0.7]:
    for u in [0.3, 0.5, 0.7]:
        kept = [x for x in res if x["supports"] >= t and x["own_current"] >= u]; k_ok = sum(x["label"] == "ok" for x in kept)
        print(f"  s>={t} c>={u}: kept {len(kept):3}  precision {k_ok/max(1,len(kept)):.2f}  recall {k_ok/len(ok):.2f}")
print("\nmean 'supports' by label:", {l: round(st.mean(x['supports'] for x in res if x['label']==l), 2) for l in sorted({x['label'] for x in res})})
