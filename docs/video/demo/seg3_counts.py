"""Segment 3 replay source: the same question answered by the graph tool and by plain vector search. Prints only counts, ids, scores and concept names (no transcript text)."""
import sys
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, router, grounded

QUESTION = "What are the top concerns among scientists?"
with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
    ix = Q.ConceptIndex(d)
    if "plain" in sys.argv:
        print(f"plain vector search: {QUESTION}")
        for r in Q.search_segments(d, QUESTION, 5):
            print(f"  {r['interview']:<14} {r['group']:<10} score {r['score']:.3f}")
        print("  -> 5 similar answers. No counts, no ranking of concerns.")
    else:
        p = router.answer(QUESTION, d, ix)
        print(f"route={p['route']} confidence={p['route_confidence']}")
        print(grounded.render(p))
