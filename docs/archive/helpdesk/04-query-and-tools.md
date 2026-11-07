# 04. Query routing and MCP tool surface

## Design rule from the existing project

In helpdesk-rag, qwen3:8b filled an optional `priority` argument on **every** call and correct results fell from 16/19 to 6/19 until the argument was removed.
So this design treats the 8B model as a **router with a small menu**, not as a query author:

- 5 tools, no more. Small models degrade as the tool list grows.
- Required arguments are short strings or enums. No optional filters.
- Tool names and docstrings say *when not to use them*.
- Cypher lives in code, parameterized and read-only. The model never writes Cypher in the default path ([ADR-0004](decisions/0004-query-interface.md)).

> **Update (ADR-0008):** routing is done by a decision model (`nimble`, via `/v1/systemone`), not by qwen3. The tools below are the internal layer behind a single
> `ask_helpdesk(question)` MCP tool, and are also available as a second ollmcp profile for A/B comparison. Sketch of the router call:
>
> ```json
> {"model": "nimble", "state": "<user question>", "questions": {"route": {"type": "choice",
>   "instructions": "Pick the best tool for this help-desk question.",
>   "criteria": {"symptom_lookup": "user describes an IT problem and wants similar past tickets",
>                "aggregate_ranking": "ranking or counting problems across tickets",
>                "agent_stats": "questions about agents or teams", "out_of_scope": "not about IT help-desk history"}}}}
> ```
>
> Returns `choice`, `probabilities` and `confidence`; below the confidence threshold the tool asks for clarification instead of running a query. `criteria` must be an object of key to description.

## Question types and routes

| Question type | Example | Route |
|---|---|---|
| Symptom lookup | "VPN drops every hour, seen before?" | `find_similar_problems` (Qdrant, then graph expand) |
| Problem deep-dive | "What was done for 'Outlook keeps prompting for password on Mac'?" | `problem_profile` |
| Ranking / aggregate | "Which problems get escalated most?" | `top_problems` |
| Agent / team | "Who resolves network tickets fastest?" | `agent_stats` |
| Relationship | "What problems are related to BitLocker prompts?" | `related_problems` |
| Out of scope | "What's 2+2" | No tool call |

## Tools (`helpdesk-graph` MCP server)

| Tool | Arguments | Returns | Backed by |
|---|---|---|---|
| `find_similar_problems` | `symptom: str` | Up to 3 problems: `problem`, `tickets_with_this_problem`, `relevance`, `top_actions[3]`, `median_hours_to_resolve`, `escalation_rate`, `example_ticket_ids[3]` | Existing `retrieve_docs` then one expansion query |
| `problem_profile` | `problem: str` (exact summary from a prior result) | Full profile: actions with counts, priority mix, channel mix, resolve-time p50/p90, SLA breaches, related problems | One Cypher query |
| `top_problems` | `metric: enum(tickets, escalated, slowest, sla_breaches)`, `limit: int = 5` | Ranked list with the metric value and ticket count | Four fixed Cypher templates |
| `agent_stats` | `group_by: enum(agent, team)`, `metric: enum(median_resolve_hours, tickets, escalation_rate)` | Ranked rows | Two fixed templates |
| `related_problems` | `problem: str` | Up to 5 neighbours with the shared actions that connect them | `CO_OCCURS` traversal |

`limit` is the only optional argument and is clamped to 1-10. It is a number, not a categorical filter, so it does not trigger the "fill every field" failure.

The existing `search_tickets` stays registered in the separate `helpdesk-rag` server for parity and A/B comparison. When both servers are loaded the total is 6 tools.
For the graph experiment, load only `helpdesk-graph` so the model cannot take the old path by default.

### Example expansion query (used by `find_similar_problems`)

```cypher
// Stats per problem (one row)
MATCH (p:Problem {key: $key})-[:HAS_TICKET]->(t:Ticket)
RETURN p.summary AS problem,
       count(t) AS tickets,
       percentileCont(t.hours_to_resolve, 0.5) AS median_hours,   // nulls (open tickets) are ignored
       avg(CASE WHEN t.escalated THEN 1.0 ELSE 0.0 END) AS escalation_rate,
       collect(t.ticket_id)[..3] AS example_ticket_ids;

// Top actions per problem (second query, same tool call)
MATCH (:Problem {key: $key})-[c:COMMONLY_DONE]->(a:Action)
RETURN a.text AS action, c.n AS tickets, c.share AS share
ORDER BY c.n DESC LIMIT 3;
```

Every number comes from the database, never from the LLM. Two small queries are easier to test than one clever one.

### Response shaping for a small model

- Return **compact JSON under about 1.5k tokens**. The 16k context is shared with chat history and the system prompt.
- Always include `example_ticket_ids` so the answer can cite evidence.
- Include a plain-language `note` on empty results, as `search_tickets` does today: "No matching problems. Do not guess; tell the user to open a new ticket."
- Round numbers in the tool, not in the model.
- Never return `Reported by <name>` text or internal-only data.

## System prompt additions (sketch)

```
You answer questions about IT help-desk history using the tools provided.
Use find_similar_problems for a symptom. Use top_problems or agent_stats for rankings.
Use only numbers returned by tools; if a tool returns nothing, say so and suggest opening a ticket.
Cite ticket IDs. Do not claim a fix worked: actions show what was tried, not what resolved the issue.
Do not call a tool for greetings or non-IT questions.
```

The last-but-one rule matters: `Action` nodes are comments such as "Customer contacted and asked to retry after cache clear", which is a step taken, not proof of a resolution.

## Optional: gated text-to-Cypher (phase 3, off by default)

If typed tools prove too narrow, add one tool `ask_graph(question: str)` with these guards:

1. A Neo4j **read-only** user and `READ` access mode on the session.
2. The schema (section 03) injected as the prompt; few-shot examples drawn from the eval set.
3. Generation by `qwen2.5-coder:7b-instruct-q8_0` (already installed) or `qwen2.5:32b` if latency allows, **not** the orchestrator model.
4. `EXPLAIN` the query first; reject anything with writes, `CALL` outside an allowlist, or unbounded variable-length paths; enforce `LIMIT 50` and a 5 s timeout.
5. Log every generated query to Phoenix. Promote repeated good queries into typed tools.

Gate it behind the evaluation in [06](06-evaluation-and-roadmap.md): enable only if it beats the typed set on the questions the typed set cannot answer.

## ollmcp wiring

```json
{
  "mcpServers": {
    "helpdesk-graph": {
      "command": ".venv/bin/python",
      "args": ["-W", "ignore", "-m", "graphrag.mcp_server"],
      "env": {
        "PYTHONPATH": "src:../helpdesk-rag/src",
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "reader",
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

```bash
ollmcp --servers-json mcp.json --model qwen3:8b-16k
```

Notes:

- Run from the project root (relative paths), as with helpdesk-rag. Nothing may print to stdout except MCP protocol (stdio transport).
- The password is not in `mcp.json`; the server reads `NEO4J_PASSWORD` from `.env`.
- `qwen3:8b-16k` is already pulled; plain `qwen3:8b` is the project default and works too, but its 4k-ish default context is tight once tool results are in play. This is a recommendation to verify, not a measured result.
