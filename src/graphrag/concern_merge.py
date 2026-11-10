"""Merge the looser concern pass (eval/concern_pass.py) into an assembled run (graph_input.jsonl + normalise.json).

New concern edges are those that are grounded, pass the same verify threshold, and whose quote is not already the quote of any existing
edge in that interview. Their names join an existing canonical concern when cosine >= the normalise threshold, otherwise they cluster among
themselves. Existing canonical names and edges are never changed. Originals are backed up as *.v1.* the first time. Idempotent.
Run: PYTHONPATH=src:. uv run python -m graphrag.concern_merge --run-id demo1
"""
import argparse, json, shutil
import numpy as np
from . import config as C, normalise as N, verify as V
from .extract import _nq
from .manifest import Stage

PASS_VERSION = "concern-loose-v1"
VERIFY_MIN = 0.2


def new_items(extract_rows: list[dict], verify_rows: dict, existing_quotes: dict[str, set]) -> dict[str, list[dict]]:
    out = {}
    for r in extract_rows:
        v = verify_rows.get(r["key"])
        if v is None: continue
        used, rows = set(existing_quotes.get(r["key"], set())), []
        for it, sc in zip(r["items"], v["scores"]):
            q = _nq(it["quote"])
            if it.get("kind") == "concern" and it["grounded"] and it.get("segment_idx") is not None and V.keep(sc, VERIFY_MIN) and q not in used:
                used.add(q); rows.append({**it, "verify": sc})
        out[r["key"]] = rows
    return out


def assign(new_counts: dict[str, int], canon_names: list[str], embed_fn, threshold: float = N.DEFAULT_THRESHOLD) -> dict[str, str]:
    """Map each new cleaned name to an existing canonical name (cos >= threshold) or to a new canonical chosen by greedy clustering."""
    names = list(new_counts)
    if not names: return {}
    nv, cv = embed_fn(names), embed_fn(canon_names)
    sims = nv @ cv.T
    mapping, rest = {}, []
    for i, n in enumerate(names):
        j = int(np.argmax(sims[i]))
        if sims[i, j] >= threshold: mapping[n] = canon_names[j]
        else: rest.append(i)
    if rest:
        sub = N.cluster([names[i] for i in rest], nv[rest], new_counts, threshold)
        mapping.update(sub)
    return mapping


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--concern-dir", default=str(C.ROOT / "data" / "eval" / "concern_pass"))
    a = ap.parse_args(); run = C.ROOT / "data" / "artefacts" / a.run_id; cdir = C.ROOT / "data" / "eval" / "concern_pass" if not a.concern_dir else __import__("pathlib").Path(a.concern_dir)
    gi, nt = run / "graph_input.jsonl", run / "normalise.json"
    for p in (gi, nt):
        b = p.with_name(p.stem + ".v1" + p.suffix)
        if not b.exists(): shutil.copy(p, b)
    recs = [json.loads(l) for l in open(run / "graph_input.v1.jsonl")]       # always merge from the untouched originals
    table = json.load(open(run / "normalise.v1.json"))
    ex = [json.loads(l) for l in open(cdir / "extract.jsonl")]; vr = {r["key"]: r for r in (json.loads(l) for l in open(cdir / "verify.jsonl"))}
    existing = {r["transcript_id"]: {_nq(e["quote"]) for e in r["edges"]} for r in recs}
    new = new_items(ex, vr, existing)
    counts: dict[str, int] = {}
    for rows in new.values():
        for it in rows: n = N.clean(it["name"]); counts[n] = counts.get(n, 0) + 1
    old_map = table["mapping"]["concern"]
    canon = sorted(set(old_map.values()))
    mapping = assign({n: c for n, c in counts.items() if n not in old_map}, canon, N.embed)
    table["mapping"]["concern"] = {**old_map, **mapping}
    al = table["aliases"].setdefault("concern", {})
    for raw, c in mapping.items(): al.setdefault(c, []).append(raw)
    added = 0
    with open(gi, "w") as f:
        for r in recs:
            for it in new.get(r["transcript_id"], []):
                raw = N.clean(it["name"]); canon_name = table["mapping"]["concern"].get(raw, raw)
                r["edges"].append({"kind": "concern", "raw_name": it["name"], "canonical": canon_name, "status": it["status"], "polarity": it["polarity"],
                                   "quote": it["quote"], "segment_idx": it["segment_idx"], "verify": it["verify"], "keep": True, "prompt_version": PASS_VERSION})
                added += 1
            f.write(json.dumps(r) + "\n")
    nt.write_text(json.dumps(table))
    n_new_canon = len(set(mapping.values()) - set(canon))
    print(json.dumps({"transcripts_with_new": sum(bool(v) for v in new.values()), "edges_added": added, "new_names": len(mapping), "new_canonical_concerns": n_new_canon,
                      "joined_existing": sum(1 for v in mapping.values() if v in set(canon))}))


if __name__ == "__main__":
    main()
