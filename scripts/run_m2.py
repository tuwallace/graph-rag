"""M2: rerun extraction v3 on the same 20 transcripts as the spike. Usage: PYTHONPATH=src uv run python scripts/run_m2.py"""
import json, pathlib, pandas as pd
from graphrag import config as C
from graphrag.extract import extract, hygiene_failures, PROMPT_VERSION

OUT = C.ROOT / "data" / "artefacts"; OUT.mkdir(parents=True, exist_ok=True)
pick = []
for s, n in [("workforce", 10), ("creatives", 5), ("scientists", 5)]:      # identical sampling to spike/02_extract.py
    d = pd.read_csv(C.RAW / f"{s}.csv")
    pick += [(s, r.transcript_id, r.text) for r in d.sample(n, random_state=7).itertuples()]
path = OUT / f"m2_{PROMPT_VERSION}.jsonl"
done = {json.loads(l)["transcript_id"] for l in open(path)} if path.exists() else set()   # resumable
with open(path, "a") as f:
    for i, (split, tid, text) in enumerate(pick, 1):
        if tid in done: continue
        rec = {"split": split, "transcript_id": tid, **extract(text)}
        rec["hygiene"] = hygiene_failures(rec["extraction"].get("items", []))
        f.write(json.dumps(rec) + "\n"); f.flush()
        n = len(rec["extraction"].get("items", [])); g = sum(i_["grounded"] for i_ in rec["extraction"].get("items", []))
        print(f"{i}/20 {tid} {rec['secs']}s items={n} grounded={g} json={rec['valid_json']} truncated={rec['truncated']} hygiene={rec['hygiene']}", flush=True)
print("wrote", path)
