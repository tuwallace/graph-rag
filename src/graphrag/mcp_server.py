"""MCP server over the interview graph. stdio transport: nothing may print to stdout except MCP messages.

Run: PYTHONPATH=src uv run python -m graphrag.mcp_server            (profile B: one routed tool + typed tools hidden)
     GRAPHRAG_PROFILE=typed ... (profile A: typed tools only, the model picks; for the M7 baseline)
"""
import os, sys, json
from fastmcp import FastMCP
from neo4j import GraphDatabase
from . import config as C, queries as Q, router, grounded

PROFILE = os.getenv("GRAPHRAG_PROFILE", "routed")   # routed | typed
mcp = FastMCP("interview-graph", instructions=(
    "Call ask_interviews once for every user message, including messages that look unrelated to the interviews: the tool decides and replies. Pass the user's message as `question` word for word; do not shorten or rephrase it. Never answer from your own knowledge or invent quotes. "
    "Then reply with the `answer` field exactly as given. Do not rewrite it and do not add anything: no summary, takeaways, interpretation, "
    "explanations of why, ratios or percentages that are not in it, and do not edit or bracket the quotes."))

_driver = None
_index = None

def driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF")
    return _driver

def index():
    global _index
    if _index is None:
        _index = Q.ConceptIndex(driver())
    return _index

def _resolve(concept: str):
    m = index().match(concept, 1)[0]
    return (m["name"], m["similarity"]) if m["similarity"] >= router.MIN_CONCEPT_SIM else (None, m["similarity"])

if PROFILE == "routed":
    @mcp.tool
    def ask_interviews(question: str) -> dict:
        """Answer any user message about the AI interview transcripts (a 500-interview sample of the 1,250 published; workforce, creatives and scientists). Call it for every message, including unrelated ones, passing the user's message word for word as `question`: it routes internally to search, counts, group comparison, themes or quotes, and refuses what it cannot answer. Relay the `answer` field to the user exactly as given, with nothing added."""
        p = router.answer(question, driver(), index())
        text = grounded.render(p)
        return {"route": p["route"], "route_confidence": p["route_confidence"], "status": p["status"], "answer": text,
                "instruction": "Reply with the answer field exactly as given. Add nothing."}
else:
    @mcp.tool
    def search_segments(query: str) -> list[dict]:
        """Top 5 interview answers semantically similar to the query, with group, excerpt and extracted concepts."""
        return Q.search_segments(driver(), query, 5)

    @mcp.tool
    def concept_stats(kind: str, group: str = "all", limit: int = 10) -> dict:
        """Rank concepts by number of interviews mentioning them. kind: task | ai_use | concern. group: all | workforce | creatives | scientists."""
        if kind not in Q.KINDS or group not in Q.GROUPS:
            return {"status": "error", "message": f"kind must be one of {list(Q.KINDS)}, group one of {list(Q.GROUPS)}"}
        return {"status": "ok", "ranking": Q.concept_stats(driver(), kind, group, max(1, min(limit, 25)))}

    @mcp.tool
    def compare_groups(concept: str) -> dict:
        """Per-group interview counts and two quotes for one concept (free text; matched to a canonical concept)."""
        name, sim = _resolve(concept)
        return {"status": "ok", "concept": name, "by_group": Q.compare_groups(driver(), name)} if name else {"status": "clarify", "message": "No matching concept."}

    @mcp.tool
    def quotes(concept: str) -> dict:
        """Up to 5 verbatim participant quotes with interview ids for one concept (free text; matched to a canonical concept)."""
        name, sim = _resolve(concept)
        return {"status": "ok", "concept": name, "quotes": Q.quotes(driver(), name, 5)} if name else {"status": "clarify", "message": "No matching concept."}

    @mcp.tool
    def theme_summary(theme: str = "") -> dict:
        """Pre-built theme summaries (available after milestone M8)."""
        t = Q.theme_summary(driver(), theme or None)
        return {"status": "ok", "themes": t} if t else {"status": "unavailable", "message": "Themes have not been built yet."}

if __name__ == "__main__":
    print(f"interview-graph profile={PROFILE}", file=sys.stderr)
    mcp.run(show_banner=False)
