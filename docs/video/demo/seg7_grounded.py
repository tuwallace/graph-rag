"""Segment 7 replay source. Part 1 runs the grounded answer path live. Part 2 shows a stored case from the 60-question run (data/eval/grounded.jsonl)
where the model invented quotes and figures and the validator replaced its text with the plain facts. Output is trimmed to a few lines per answer."""
import json
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, grounded

def show(label, q, source, issues, text, n=5):
    print(f"question: {q}")
    print(f"  source={source}  issues={len(issues)}")
    for i in issues[:3]: print(f"    issue: {i[:100]}")
    print("  delivered text (first lines):")
    for l in [x for x in text.splitlines() if x.strip()][:n]: print("    " + (l if len(l) <= 108 else l[:105] + "..."))
    print()

QS = {x["id"]: x["q"] for f in ("questions.json", "confirm_questions.json") for x in json.load(open(C.ROOT / "eval" / f))}
with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
    ix = Q.ConceptIndex(d)
    q = "Top concerns among scientists?"
    r = grounded.grounded_answer(q, d, ix)
    print("--- live run ---"); show("live", q, r["source"], r["issues"], r["text"], 4)
stored = {json.loads(l)["id"]: json.loads(l) for l in open(C.ROOT / "data" / "eval" / "grounded.jsonl")}["c07"]
print("--- stored case from the 60-question run ---")
show("stored", QS["c07"], stored["source"], stored["issues"], stored["text"], 3)
