"""Gate 2 proxy: do the top-5 vector hits for 10 queries contain answers that mention the topic?
Relevance is a keyword regex over the answer text, independent of extraction and of the embedder. This is a proxy written
without human labels (ADR-0013): it can under-count paraphrases and over-count incidental word matches."""
import json, re, sys, pathlib
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q

MIN_WORDS = int(sys.argv[1]) if len(sys.argv) > 1 else 0   # drop very short answers after retrieval
qs = json.loads((pathlib.Path(__file__).parent / "retrieval_queries.json").read_text())
hits = prec = 0
with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
    for x in qs:
        rows = Q.search_segments(d, x["q"], 5 if not MIN_WORDS else 20)
        full = {r["segment"]: r for r in Q._read(d, "MATCH (s:Segment) WHERE s.id IN $ids RETURN s.id AS segment, s.answer AS a", ids=[r["segment"] for r in rows])}
        rows = [r for r in rows if len(full[r["segment"]]["a"].split()) >= MIN_WORDS][:5]
        rel = [bool(re.search(x["re"], full[r["segment"]]["a"], re.I)) for r in rows]
        hits += any(rel); prec += sum(rel) / 5
        print(f"{'HIT ' if any(rel) else 'MISS'} p@5={sum(rel)}/5  {x['q']}")
print(f"queries with at least one relevant in top 5: {hits}/{len(qs)} = {hits/len(qs):.2f}; mean precision@5 = {prec/len(qs):.2f}  (min_words={MIN_WORDS})")
