"""M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble router + one tool), C (plain vector RAG).
Resumable: results go to data/eval/<config>.jsonl and finished question ids are skipped.
Run: PYTHONPATH=src:. uv run python eval/run_eval.py [A B C]
"""
import json, sys, time, pathlib
import ollama
from neo4j import GraphDatabase
from graphrag import config as C, queries as Q, router

OUT = C.ROOT / "data" / "eval"; OUT.mkdir(parents=True, exist_ok=True)
QUESTIONS = json.loads((pathlib.Path(__file__).parent / "questions.json").read_text())
CLIENT = ollama.Client(host=C.OLLAMA_URL, timeout=600)
MAXCTX = 7000   # characters of tool output shown to the answer model

SYSTEM = ("Answer only from the tool output or context provided. Cite interview ids. Quote at most one sentence per source, in double quotes. "
          "Say these are findings from a sample of AI-led interviews, not facts about workers in general. If the tool output says clarify, "
          "unavailable or out_of_scope, or there is nothing relevant, say so; do not guess. Do not use outside knowledge.")

TOOLS = [
 {"type": "function", "function": {"name": "search_segments", "description": "Top 5 interview answers semantically similar to the query, with group, excerpt and extracted concepts.",
   "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
 {"type": "function", "function": {"name": "concept_stats", "description": "Rank concepts by number of interviews mentioning them. kind: task | ai_use | concern. group: all | workforce | creatives | scientists.",
   "parameters": {"type": "object", "properties": {"kind": {"type": "string", "enum": list(Q.KINDS)}, "group": {"type": "string", "enum": list(Q.GROUPS)}, "limit": {"type": "integer"}}, "required": ["kind"]}}},
 {"type": "function", "function": {"name": "compare_groups", "description": "Per-group interview counts and two quotes for one concept (free text; matched to a canonical concept).",
   "parameters": {"type": "object", "properties": {"concept": {"type": "string"}}, "required": ["concept"]}}},
 {"type": "function", "function": {"name": "quotes", "description": "Up to 5 verbatim participant quotes with interview ids for one concept (free text; matched to a canonical concept).",
   "parameters": {"type": "object", "properties": {"concept": {"type": "string"}}, "required": ["concept"]}}},
 {"type": "function", "function": {"name": "theme_summary", "description": "Pre-built theme summaries.",
   "parameters": {"type": "object", "properties": {"theme": {"type": "string"}}, "required": []}}},
]


def chat(messages, tools=None):
    return CLIENT.chat(model=C.GEN_MODEL, messages=messages, tools=tools, think=False, options={"temperature": 0, "num_predict": 700})


def run_tool(driver, index, name, args):
    """Same behaviour as the typed MCP profile."""
    def res(c):
        m = index.match(c, 1)[0]
        return (m["name"], m["similarity"]) if m["similarity"] >= router.MIN_CONCEPT_SIM else (None, m["similarity"])
    try:
        if name == "search_segments":
            return Q.search_segments(driver, str(args["query"]), 5)
        if name == "concept_stats":
            if args.get("kind") not in Q.KINDS or args.get("group", "all") not in Q.GROUPS:
                return {"status": "error", "message": f"kind must be one of {list(Q.KINDS)}, group one of {list(Q.GROUPS)}"}
            return {"status": "ok", "ranking": Q.concept_stats(driver, args["kind"], args.get("group", "all"), max(1, min(int(args.get("limit", 10)), 25)))}
        if name in ("compare_groups", "quotes"):
            n, _ = res(str(args["concept"]))
            if not n:
                return {"status": "clarify", "message": "No matching concept."}
            return {"status": "ok", "concept": n, "by_group": Q.compare_groups(driver, n)} if name == "compare_groups" else {"status": "ok", "concept": n, "quotes": Q.quotes(driver, n, 5)}
        if name == "theme_summary":
            t = Q.theme_summary(driver, args.get("theme") or None)
            return {"status": "ok", "themes": t} if t else {"status": "unavailable", "message": "Themes have not been built yet."}
        return {"status": "error", "message": f"unknown tool {name}"}
    except Exception as e:   # bad arguments from the model are data, not a crash
        return {"status": "error", "message": f"{type(e).__name__}: {e}"}


def final_answer(question, context):
    r = chat([{"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Question: {question}\n\nTool output / context:\n{context[:MAXCTX]}"}])
    return r.message.content or ""


def config_A(x, driver, index):
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": x["q"]}]
    calls, ctx = [], []
    r = chat(msgs, TOOLS)
    for _ in range(3):
        tcs = r.message.tool_calls or []
        if not tcs:
            break
        msgs.append(r.message)
        for tc in tcs:
            args = dict(tc.function.arguments or {}); out = run_tool(driver, index, tc.function.name, args)
            calls.append({"name": tc.function.name, "args": args}); s = json.dumps(out, default=str); ctx.append(s)
            msgs.append({"role": "tool", "tool_name": tc.function.name, "content": s[:MAXCTX]})
        r = chat(msgs, TOOLS)
    return {"calls": calls, "context": "\n".join(ctx), "answer": r.message.content or ""}


def config_B(x, driver, index):
    p = router.answer(x["q"], driver, index)
    ctx = json.dumps(p, default=str)
    return {"payload": {k: v for k, v in p.items() if k not in ("results", "ranking", "by_group", "quotes", "themes")}, "context": ctx,
            "answer": final_answer(x["q"], ctx)}


def config_C(x, driver, index):
    ctx = json.dumps(Q.search_segments(driver, x["q"], 5), default=str)
    return {"context": ctx, "answer": final_answer(x["q"], ctx)}


FUNCS = {"A": config_A, "B": config_B, "C": config_C}

if __name__ == "__main__":
    which = sys.argv[1:] or ["B", "C", "A"]
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        index = Q.ConceptIndex(d)
        for cfg in which:
            path = OUT / f"{cfg}.jsonl"
            done = {json.loads(l)["id"] for l in open(path)} if path.exists() else set()
            for x in QUESTIONS:
                if x["id"] in done:
                    continue
                t0 = time.time()
                try:
                    rec = FUNCS[cfg](x, d, index)
                except Exception as e:
                    rec = {"error": f"{type(e).__name__}: {e}", "context": "", "answer": ""}
                rec.update(id=x["id"], config=cfg, secs=round(time.time() - t0, 2))
                with open(path, "a") as f:
                    f.write(json.dumps(rec, default=str) + "\n")
                print(f"[{cfg} {x['id']}] {rec['secs']}s", flush=True)
