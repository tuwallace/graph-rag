"""Question router: a decision model (`nimble`, /v1/systemone) picks a route and fills enum arguments; typed queries answer.

The orchestrator (qwen3) never writes Cypher or fills arguments. Low router confidence returns a clarification request and runs
nothing (ADR-0008). Free-text concept names are resolved by embedding match to canonical nodes, not by an LLM.
"""
import time
from . import queries as Q
from .decision import decide

ROUTER_VERSION = "v3"   # v3: boundary examples in the route descriptions (2026-11-09). v2: threshold 0.5 (from dev half of the M7 set); longer concept span wins ties
MIN_CONFIDENCE = 0.5     # ADR-0008 started at 0.6; lowered to 0.5 from the dev half of the M7 set
MIN_CONCEPT_SIM = 0.8    # below this the match is too weak (0.786 matched "weather" to "climate change")

ROUTES = {
    "local_search": "find what people said about a topic or how a kind of person uses AI; an open question answered by reading a few answers. e.g. 'how do designers use AI day to day?'",
    "concept_stats": "count or rank things people mentioned: uses of AI, tasks, or concerns. e.g. 'what are the most common tasks?', 'top five worries among scientists'",
    "compare_groups": "compare workforce, creatives and scientists on one topic. e.g. 'do writers and researchers differ on trust?'",
    "theme_overview": "the big picture: the overall themes or a general summary of what the interviews say, about everyone or a whole group, with no single topic to look up. e.g. 'what are the main themes?', 'summarise what professionals say about AI', 'give me an overview of the concerns'",
    "evidence": "show quotes or examples about one specific thing. e.g. 'show me quotes about hallucinations'",
    "out_of_scope": "unrelated to the interviews: arithmetic, greetings, general knowledge",
}
ROUTE_Q = {"type": "choice", "instructions": "Pick the best route for this question about a set of AI interview transcripts.", "criteria": ROUTES}
KIND_Q = {"type": "choice", "instructions": "Which kind of thing is the question about?", "criteria": {
    "ai_use": "ways people use AI",
    "task": "work tasks or activities people do",
    "concern": "worries, fears, risks or problems with AI"}}
GROUP_Q = {"type": "choice", "instructions": "Which group of interviewees does the question restrict to?", "criteria": {
    "all": "no restriction, or several groups together",
    "workforce": "general workforce or professionals",
    "creatives": "creative professionals: artists, writers, designers, musicians",
    "scientists": "scientists and researchers"}}


def _pick(answer: dict) -> tuple[str, float]:
    return answer["choice"], round(float(answer["confidence"]), 3)


def clarify(reason: str, **extra) -> dict:
    return {"status": "clarify", "message": reason, **extra}


def route_question(question: str, decide_fn=decide) -> dict:
    a = decide_fn(question, {"route": ROUTE_Q})["route"]
    route, conf = _pick(a)
    return {"route": route, "confidence": conf, "probabilities": a.get("probabilities")}


def answer(question: str, driver, index: "Q.ConceptIndex", decide_fn=decide, k: int = 5) -> dict:
    """Route, gate, dispatch. Returns compact JSON-able payload with the routing decision attached."""
    t0 = time.time()
    r = route_question(question, decide_fn)
    meta = {"route": r["route"], "route_confidence": r["confidence"], "router_version": ROUTER_VERSION}

    def done(payload):
        return {**meta, **payload, "secs": round(time.time() - t0, 2)}

    if r["confidence"] < MIN_CONFIDENCE:
        return done(clarify("I am not sure what kind of question this is. Do you want quotes, counts, a group comparison or the main themes?"))
    route = r["route"]
    if route == "out_of_scope":
        return done({"status": "out_of_scope", "message": "This tool only answers questions about the AI interview transcripts."})
    if route == "local_search":
        return done({"status": "ok", "results": Q.search_segments(driver, question, k)})
    if route == "theme_overview":
        t = Q.theme_summary(driver)
        return done({"status": "ok", "themes": t} if t else {"status": "unavailable", "message": "Themes have not been built yet (milestone M8)."})
    if route == "concept_stats":
        extra = decide_fn(question, {"kind": KIND_Q, "group": GROUP_Q})
        kind, kc = _pick(extra["kind"]); group, gc = _pick(extra["group"])
        if min(kc, gc) < MIN_CONFIDENCE:
            return done(clarify("Which kind (AI uses, tasks or concerns) and which group (all, workforce, creatives, scientists)?", kind_guess=kind, group_guess=group))
        return done({"status": "ok", "kind": kind, "group": group, "group_size": Q.group_sizes(driver).get(group) if group != "all" else sum(Q.group_sizes(driver).values()),
                     "ranking": Q.concept_stats(driver, kind, group, 10)})
    # compare_groups and evidence need one concept
    m = index.match_question(question, 3)
    if not m or m[0]["similarity"] < MIN_CONCEPT_SIM:
        return done(clarify("I could not match that to a known concept. Which topic do you mean?", candidates=[x["name"] for x in m]))
    c = m[0]
    if route == "compare_groups":
        return done({"status": "ok", "concept": c["name"], "match_similarity": c["similarity"], "by_group": Q.compare_groups(driver, c["name"])})
    return done({"status": "ok", "concept": c["name"], "match_similarity": c["similarity"], "quotes": Q.quotes(driver, c["name"], 5)})
