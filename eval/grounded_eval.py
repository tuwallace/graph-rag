"""Re-measure groundedness with answer generation, through the grounded path (src/graphrag/grounded.py), router v2.
Questions: original 40 + 20 confirm questions. For each, scores the RAW model answer and the DELIVERED text with the independent
corpus-based checks from eval/score.py. Resumable: data/eval/grounded.jsonl. Run: PYTHONPATH=src:. uv run python eval/grounded_eval.py [run|score]
"""
import json, sys, time, pathlib
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, grounded
from graphrag.parse import user_text
from graphrag.pipeline import select
import eval.score as S

HERE = pathlib.Path(__file__).parent; OUT = C.ROOT / "data" / "eval" / "grounded.jsonl"
QS = json.loads((HERE / "questions.json").read_text()) + json.loads((HERE / "confirm_questions.json").read_text())

def run():
    done = {json.loads(l)["id"] for l in open(OUT)} if OUT.exists() else set()
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        ix = Q.ConceptIndex(d)
        for x in QS:
            if x["id"] in done: continue
            t0 = time.time(); r = grounded.grounded_answer(x["q"], d, ix)
            p = r["payload"]
            rec = {"id": x["id"], "route": x["route"], "got_route": p["route"], "status": p["status"], "source": r["source"], "issues": r["issues"], "raw": r["raw"], "text": r["text"],
                   "kind": p.get("kind"), "group": p.get("group"), "concept": p.get("concept"), "secs": round(time.time() - t0, 2)}
            with open(OUT, "a") as f: f.write(json.dumps(rec) + "\n")
            print(f"[{x['id']}] {rec['source']} {rec['secs']}s {r['issues'][:1]}", flush=True)

def quality(text, texts, ntexts):
    qs = S.quotes_in(text); cited = {c.split("#")[0] for c in S.IDRE.findall(text)}; ok = 0
    for q in qs:
        nq = S.norm(q)
        ok += any(nq in ntexts[c] or S.ground.is_grounded(q, texts[c]) for c in cited if c in texts)
    return len(qs), ok

def score():
    texts = {tid: user_text(t) for _, tid, t in select("demo")}; ntexts = {k: S.norm(v) for k, v in texts.items()}
    recs = [json.loads(l) for l in open(OUT)]
    out = {}
    for label, key in (("raw model answer (before validation)", "raw"), ("delivered text (after validation + fallback)", "text")):
        nq = nv = 0; bad_q = 0
        for r in recs:
            t = r[key]
            if t is None: continue
            n, v = quality(t, texts, ntexts); nq += n; nv += v; bad_q += n - v
        out[label] = (nv, nq)
    nllm = [r for r in recs if r["raw"] is not None]
    fb = [r for r in nllm if r["source"] == "rendered_fallback"]
    print(f"questions {len(recs)}; passed through the model {len(nllm)}; fell back to rendered facts {len(fb)} ({len(fb)/max(1,len(nllm)):.0%})")
    for k, (v, n) in out.items(): print(f"quotes found in the cited interview, {k}: {v}/{n}" + (f" ({v/n:.0%})" if n else ""))
    import collections
    print("fallback reasons:", dict(collections.Counter(i.split(":")[0] for r in fb for i in r["issues"])))
    print("routes that fell back:", dict(collections.Counter(r["route"] for r in fb)))
    print("statuses:", dict(collections.Counter(r["status"] for r in recs)))
    # figures in delivered text vs the rendered facts are checked by construction; here: independent check against the database for stats answers
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        ok = tot = 0
        for r in recs:
            if r["route"] == "concept_stats" and r["got_route"] == "concept_stats" and r["kind"] and r["status"] == "ok":
                g = Q.concept_stats(d, r["kind"], r["group"], 1)[0]; tot += 1
                ok += g["concept"].lower() in r["text"].lower() and str(g["interviews"]) in S.nums(r["text"], False)
        print(f"stats answers whose top concept and count match the database: {ok}/{tot}")
    print("median secs", sorted(r["secs"] for r in recs)[len(recs) // 2])

if __name__ == "__main__":
    (run if sys.argv[1:] == ["run"] else score)() if sys.argv[1:] in (["run"], ["score"]) else (run(), score())
