"""M5: load an assembled run (graph_input.jsonl) into Neo4j. Idempotent (MERGE everywhere).

Run: PYTHONPATH=src uv run python -m graphrag.load --run-id demo1 [--scope demo]

Only edges with keep=true are loaded. Every edge is re-grounded against the segment's participant answer at load
time; failures are dropped and counted (03-graph-schema, provenance rule).
"""
import argparse, hashlib, json
import ollama
from neo4j import GraphDatabase
from . import config as C, ground, schema
from .parse import segments as parse_segments, parse_turns
from .pipeline import select

LABEL = {"work_task": ("Task", "DOES_TASK"), "ai_use": ("AIUse", "USES_AI_FOR"), "concern": ("Concern", "RAISES")}
EMBED_CHARS = 6000   # nomic-embed-text context guard
BATCH = 500


def seg_id(tid: str, idx: int) -> str:
    return f"{tid}#{idx}"


def edge_id(sid: str, kind: str, canonical: str, quote: str) -> str:
    return hashlib.sha1(f"{sid}|{kind}|{canonical}|{quote}".encode()).hexdigest()[:16]


def build(run_dir, texts: dict[str, str]):
    """Return (interviews, segments, edges_by_kind, stats) ready for UNWIND. Pure: no database, no embedding."""
    interviews, segs, edges = [], [], {k: [] for k in LABEL}
    stats = {"edges_in": 0, "edges_kept": 0, "ungrounded": 0, "no_segment": 0}
    for line in open(run_dir / "graph_input.jsonl"):
        rec = json.loads(line)
        tid = rec["transcript_id"]; text = texts[tid]
        parsed = {s["idx"]: s for s in parse_segments(text)}
        interviews.append({"tid": tid, "group": rec["group"], "n_turns": len(parse_turns(text)), "chars": len(text)})
        for a in rec["segments"]:
            p = parsed.get(a["idx"])
            if p:
                segs.append({"id": seg_id(tid, a["idx"]), "tid": tid, "idx": a["idx"], "question": p["question"], "answer": p["answer"],
                             "attitude": a["attitude"], "attitude_conf": a["attitude_conf"]})
        for e in rec["edges"]:
            stats["edges_in"] += 1
            if not e["keep"]:
                continue
            stats["edges_kept"] += 1
            p = parsed.get(e["segment_idx"])
            if p is None:
                stats["no_segment"] += 1; continue
            if not ground.is_grounded(e["quote"], p["answer"]):
                stats["ungrounded"] += 1; continue
            sid = seg_id(tid, e["segment_idx"])
            edges[e["kind"]].append({"sid": sid, "key": e["canonical"], "eid": edge_id(sid, e["kind"], e["canonical"], e["quote"]),
                                     "raw_name": e["raw_name"], "quote": e["quote"], "status": e["status"], "polarity": e["polarity"],
                                     "supports": e["verify"]["supports"], "own_current": e["verify"].get("own_current"),
                                     "model": rec["model"], "prompt_version": e.get("prompt_version", rec["prompt_version"])})
    return interviews, segs, edges, stats


def embed_segments(segs: list[dict], cache_path, client=None, batch: int = 32) -> dict[str, list[float]]:
    """Embed question+answer per segment; cached on disk so a reload or crash does not recompute."""
    cache = {}
    if cache_path.exists():
        for line in open(cache_path):
            try:
                r = json.loads(line); cache[r["id"]] = r["v"]
            except json.JSONDecodeError:
                pass   # half-written last line
    todo = [s for s in segs if s["id"] not in cache]
    client = client or ollama.Client(host=C.OLLAMA_URL)
    with open(cache_path, "a") as f:
        for i in range(0, len(todo), batch):
            chunk = todo[i:i + batch]
            docs = [("search_document: " + s["question"] + "\n" + s["answer"])[:EMBED_CHARS] for s in chunk]
            for s, v in zip(chunk, client.embed(model=C.EMBED_MODEL, input=docs)["embeddings"]):
                cache[s["id"]] = v; f.write(json.dumps({"id": s["id"], "v": v}) + "\n")
            f.flush()
            if (i // batch) % 20 == 0:
                print(f"[embed {min(i + batch, len(todo))}/{len(todo)}]", flush=True)
    return cache


def chunks(rows, n=BATCH):
    for i in range(0, len(rows), n):
        yield rows[i:i + n]


def write(driver, interviews, segs, edges, vectors, run_id):
    with driver.session() as s:
        for g in sorted({i["group"] for i in interviews}):
            s.run("MERGE (:Group {name:$g})", g=g).consume()
        for ch in chunks(interviews):
            s.run("""UNWIND $rows AS r MERGE (i:Interview {transcript_id:r.tid}) SET i.n_turns=r.n_turns, i.chars=r.chars
                     WITH i, r MATCH (g:Group {name:r.group}) MERGE (i)-[:IN_GROUP]->(g)""", rows=ch).consume()
        for ch in chunks(segs):
            rows = [{**x, "embedding": vectors[x["id"]]} for x in ch]
            s.run("""UNWIND $rows AS r MERGE (s:Segment {id:r.id})
                     SET s.idx=r.idx, s.question=r.question, s.answer=r.answer, s.attitude=r.attitude, s.attitude_conf=r.attitude_conf,
                         s.attr_version='v2'
                     WITH s, r CALL db.create.setNodeVectorProperty(s, 'embedding', r.embedding)
                     WITH s, r MATCH (i:Interview {transcript_id:r.tid}) MERGE (i)-[:HAS_SEGMENT]->(s)""", rows=rows).consume()
        for kind, (label, rel) in LABEL.items():
            for ch in chunks(edges[kind]):
                s.run(f"""UNWIND $rows AS r MATCH (s:Segment {{id:r.sid}})
                          MERGE (n:{label} {{key:r.key}}) ON CREATE SET n.name=r.key
                          MERGE (s)-[e:{rel} {{eid:r.eid}}]->(n)
                          SET e.quote=r.quote, e.status=r.status, e.polarity=r.polarity, e.raw_name=r.raw_name, e.supports=r.supports,
                              e.own_current=r.own_current, e.model=r.model, e.prompt_version=r.prompt_version, e.run_id=$run""",
                      rows=ch, run=run_id).consume()
            # derived: aliases (distinct raw names) and mentions (edge count)
            s.run(f"""MATCH (n:{label})<-[e:{rel}]-() WITH n, collect(DISTINCT e.raw_name) AS al, count(e) AS m
                      SET n.aliases=al, n.mentions=m""").consume()


def checks(driver, interviews, segs, edges, stats) -> dict:
    """Post-load invariants. Returns {name: (ok, detail)}."""
    out = {}
    with driver.session() as s:
        q = lambda c: s.run(c).single()[0]
        out["interviews"] = (q("MATCH (n:Interview) RETURN count(n)") == len(interviews), f"{q('MATCH (n:Interview) RETURN count(n)')} vs {len(interviews)}")
        out["segments"] = (q("MATCH (n:Segment) RETURN count(n)") == len(segs), f"{q('MATCH (n:Segment) RETURN count(n)')} vs {len(segs)}")
        out["embedded"] = (q("MATCH (n:Segment) WHERE n.embedding IS NOT NULL RETURN count(n)") == len(segs), "all segments have a vector")
        for kind, (label, rel) in LABEL.items():
            got, want = q(f"MATCH ()-[e:{rel}]->() RETURN count(e)"), len(edges[kind])
            out[f"edges {rel}"] = (got == want, f"{got} vs {want}")
            nodes_want = len({e["key"] for e in edges[kind]})
            got_n = q(f"MATCH (n:{label}) RETURN count(n)")
            out[f"nodes {label}"] = (got_n == nodes_want, f"{got_n} vs {nodes_want}")
        out["every edge has a quote"] = (q("MATCH ()-[e:DOES_TASK|USES_AI_FOR|RAISES]->() WHERE e.quote IS NULL OR e.quote = '' RETURN count(e)") == 0, "no edge without quote")
        out["every edge from a segment"] = (q("MATCH (n:Task|AIUse|Concern) WHERE NOT (n)<--(:Segment) RETURN count(n)") == 0, "no orphan concept")
        out["vector index online"] = (q("SHOW INDEXES YIELD name, state WHERE name='segment_embedding' AND state='ONLINE' RETURN count(*)") == 1, "segment_embedding ONLINE")
    out["grounding at load"] = (True, f"dropped {stats['ungrounded']} ungrounded, {stats['no_segment']} without segment, of {stats['edges_kept']} kept")
    return out


def counts(driver) -> dict:
    with driver.session() as s:
        return {"nodes": s.run("MATCH (n) RETURN count(n)").single()[0], "rels": s.run("MATCH ()-[r]->() RETURN count(r)").single()[0]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--scope", default="demo")
    a = ap.parse_args()
    run_dir = C.ROOT / "data" / "artefacts" / a.run_id
    texts = {tid: text for _, tid, text in select(a.scope)}
    interviews, segs, edges, stats = build(run_dir, texts)
    print(f"built: {len(interviews)} interviews, {len(segs)} segments, edges {({k: len(v) for k, v in edges.items()})}, {stats}", flush=True)
    vectors = embed_segments(segs, run_dir / "segment_embeddings.jsonl")
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD)) as d:
        d.verify_connectivity()
        schema.apply(d, dim=len(next(iter(vectors.values()))))
        before = counts(d)
        write(d, interviews, segs, edges, vectors, a.run_id)
        after = counts(d)
        print("counts before:", before, "after:", after, flush=True)
        res = checks(d, interviews, segs, edges, stats)
    for k, (ok, detail) in res.items():
        print(("PASS " if ok else "FAIL ") + k + ": " + detail)
    raise SystemExit(0 if all(ok for ok, _ in res.values()) else 1)


if __name__ == "__main__":
    main()
