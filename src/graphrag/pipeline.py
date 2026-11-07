"""Stage-major build pipeline: extract (qwen) -> verify + attributes (nimble) -> normalise (embeddings) -> assemble graph input.
Each stage is resumable per transcript (see manifest.py) and unloads the previous model first so timings stay clean.
Usage: PYTHONPATH=src uv run python -m graphrag.pipeline --run-id demo1 --scope demo --stage all"""
import argparse, json, time
import pandas as pd, requests
from . import config as C
from .manifest import Stage
from .parse import segments
from . import extract as X, verify as V, attributes as A, normalise as N

VERIFY_MIN = 0.2          # calibrated on the LLM-labelled sheet: drops most unsupported items at a cost of ~18% of good ones (docs/07, M3)
SCOPES = {"demo": {"creatives": None, "scientists": None, "workforce": 250}, "tiny": {"workforce": 2, "creatives": 2, "scientists": 1}}

def select(scope: str) -> list[tuple[str, str, str]]:
    """(split, transcript_id, text). Deterministic: the same draw every run."""
    out = []
    for split, n in SCOPES[scope].items():
        d = pd.read_csv(C.RAW / f"{split}.csv")
        d = d if n is None else d.sample(n, random_state=7)
        out += [(split, r.transcript_id, r.text) for r in d.itertuples()]
    return out

def unload(model: str) -> None:
    try: requests.post(f"{C.OLLAMA_URL}/api/generate", json={"model": model, "keep_alive": 0}, timeout=30)
    except requests.RequestException: pass

def stage_extract(run: str, picks, extract_fn=X.extract) -> Stage:
    st = Stage(run, "extract")
    for i, (split, tid, text) in enumerate(picks, 1):
        if st.done(tid): continue
        rec = extract_fn(text); rec["items"] = rec.pop("extraction").get("items", []); rec["split"] = split
        rec["hygiene"] = X.hygiene_failures(rec["items"]); st.write(tid, rec)
        print(f"[extract {i}/{len(picks)}] {tid} {rec['secs']}s items={len(rec['items'])}", flush=True)
    return st

def stage_verify(run: str, verify_fn=V.verify_item) -> Stage:
    ex, st = Stage(run, "extract"), Stage(run, "verify")
    for i, r in enumerate(ex.records(), 1):
        if st.done(r["key"]): continue
        t0 = time.time(); st.write(r["key"], {"scores": [verify_fn(it) for it in r["items"]], "version": V.VERIFY_VERSION})
        print(f"[verify {i}/{len(ex.done_keys)}] {r['key']} {time.time()-t0:.0f}s", flush=True)
    return st

def stage_attributes(run: str, texts: dict[str, str], attr_fn=A.attributes) -> Stage:
    ex, st = Stage(run, "extract"), Stage(run, "attributes")
    for i, r in enumerate(ex.records(), 1):
        if st.done(r["key"]): continue
        t0 = time.time(); segs = segments(texts[r["key"]])
        st.write(r["key"], {"segments": [{"idx": s["idx"], **attr_fn(s)} for s in segs], "version": A.ATTR_VERSION})
        print(f"[attributes {i}/{len(ex.done_keys)}] {r['key']} {len(segs)} segs {time.time()-t0:.0f}s", flush=True)
    return st

def kept_items(extract_rec: dict, verify_rec: dict) -> list[dict]:
    out = []
    for it, sc in zip(extract_rec["items"], verify_rec["scores"]):
        out.append({**it, "verify": sc, "keep": bool(it["grounded"]) and V.keep(sc, VERIFY_MIN)})
    return out

def stage_normalise(run: str, embed_client=None) -> dict:
    ex, vr = Stage(run, "extract"), {r["key"]: r for r in Stage(run, "verify").records()}
    items = [it for r in ex.records() if r["key"] in vr for it in kept_items(r, vr[r["key"]]) if it["keep"]]
    table = N.canonicalise(items, client=embed_client)
    (ex.dir / "normalise.json").write_text(json.dumps(table))
    return table

def assemble(run: str, texts: dict[str, str]) -> dict:
    """Join everything into one record per interview: the input for the Neo4j loader (M5)."""
    ex = {r["key"]: r for r in Stage(run, "extract").records()}
    vr = {r["key"]: r for r in Stage(run, "verify").records()}
    at = {r["key"]: r for r in Stage(run, "attributes").records()}
    table = json.loads((Stage(run, "extract").dir / "normalise.json").read_text())
    path = Stage(run, "extract").dir / "graph_input.jsonl"; n_edges = n_kept = 0
    with open(path, "w") as f:
        for tid, r in ex.items():
            if tid not in vr or tid not in at: continue
            edges = []
            for it in kept_items(r, vr[tid]):
                raw = N.clean(it["name"]); canon = table["mapping"].get(it["kind"], {}).get(raw, raw)
                edges.append({"kind": it["kind"], "raw_name": it["name"], "canonical": canon, "status": it["status"], "polarity": it["polarity"],
                              "quote": it["quote"], "segment_idx": it.get("segment_idx"), "verify": it["verify"], "keep": it["keep"]})
            n_edges += len(edges); n_kept += sum(e["keep"] for e in edges)
            f.write(json.dumps({"transcript_id": tid, "group": r["split"], "segments": at[tid]["segments"], "edges": edges,
                                "model": r["model"], "prompt_version": r["prompt_version"]}) + "\n")
    return {"path": str(path), "interviews": len(ex), "edges": n_edges, "kept": n_kept}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--scope", default="demo", choices=list(SCOPES))
    ap.add_argument("--stage", default="all", choices=["all", "extract", "verify", "attributes", "normalise", "assemble"])
    a = ap.parse_args(); picks = select(a.scope); texts = {tid: text for _, tid, text in picks}
    run_all, s = a.stage == "all", a.stage
    if run_all or s == "extract": stage_extract(a.run_id, picks); unload(C.GEN_MODEL)
    if run_all or s == "verify": stage_verify(a.run_id)
    if run_all or s == "attributes": stage_attributes(a.run_id, texts); unload(C.ROUTER_MODEL)
    if run_all or s == "normalise": t = stage_normalise(a.run_id); print({k: len(v) for k, v in t["mapping"].items()})
    if run_all or s == "assemble": print(assemble(a.run_id, texts))

if __name__ == "__main__":
    main()
