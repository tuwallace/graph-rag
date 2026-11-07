# 04. Query routing and MCP tool surface (Interviewer corpus)

Design rule carried over from the helpdesk work: a small local model (qwen3:8b) mis-fills optional tool arguments, so a **decision model routes** ([ADR-0008](decisions/0008-decision-model-router.md))
and the typed queries do the retrieval. The orchestrator model writes the final answer from compact JSON; it does not write Cypher.

## Routes

| Route | Example question | What runs |
|---|---|---|
| `local_search` | "How do designers use AI for brainstorming?" | Embed query, vector search on `Segment`, expand to concepts and quotes |
| `concept_stats` | "How many creatives mention losing skills?" | Counts of segments or interviews per canonical concept, by group |
| `compare_groups` | "How do scientists and creatives differ on trust?" | Same concept across groups, with counts and 2 quotes each |
| `theme_overview` | "What are the main themes overall?" | Read pre-built `Theme` summaries (global question) |
| `evidence` | "Show quotes about AI hallucination" | Quotes for a canonical concept, with interview ids |
| `out_of_scope` | "What's 2+2?" | No query |

Router call (`/v1/systemone`; `criteria` must be an object of key to description):

```json
{"model": "nimble", "state": "<user question>",
 "questions": {"route": {"type": "choice", "instructions": "Pick the best route for this question about interview transcripts.",
   "criteria": {"local_search": "find what people said about a topic", "concept_stats": "count or rank concepts",
                "compare_groups": "compare workforce, creatives and scientists", "theme_overview": "overall themes or summary",
                "evidence": "quotes or examples", "out_of_scope": "unrelated to the interviews"}}}}
```

Enum arguments (the `group` for stats, the concept kind) are filled by further `choice` questions, never by qwen3. Concept names are resolved by embedding match to canonical nodes, then confirmed with the user if the match is weak.
Router confidence below a tuned threshold (start 0.6) returns a clarification request. The spike showed `nimble` attitude confidence below 0.6 on 37% of segments, so expect abstentions; routing questions are different from attitude questions and must be measured separately.

## Tool surface

One entry tool for the ollmcp demo, with the typed tools behind it (also available as a second profile for comparison):

| Tool | Arguments | Returns |
|---|---|---|
| `ask_interviews` | `question: str` | Routed answer payload (compact JSON, under about 1.5k tokens) |
| `search_segments` | `query: str` | Top 5 segments: id, group, short quote, concepts |
| `concept_stats` | `kind: enum(task, ai_use, concern)`, `group: enum(all, workforce, creatives, scientists)`, `limit: int = 10` | Ranked canonical concepts with counts and distinct interviews |
| `compare_groups` | `concept: str` | Per-group counts and quotes |
| `theme_summary` | `theme: str` | Summary and member concepts |
| `quotes` | `concept: str` | Up to 5 quotes with interview ids |

## Example Cypher (parameterised, read-only)

```cypher
// concept_stats: top concerns per group, counted by distinct interview
MATCH (g:Group)<-[:IN_GROUP]-(i:Interview)-[:HAS_SEGMENT]->(s:Segment)-[r:RAISES]->(c:Concern)
WHERE ($group = 'all' OR g.name = $group) AND r.status = 'current'
RETURN c.name AS concern, count(DISTINCT i) AS interviews
ORDER BY interviews DESC LIMIT $limit;

// local_search: nearest segments, then their concepts
CALL db.index.vector.queryNodes('segment_embedding', 5, $query_embedding) YIELD node AS s, score
MATCH (i:Interview)-[:HAS_SEGMENT]->(s)
OPTIONAL MATCH (s)-[r]->(x) WHERE type(r) IN ['DOES_TASK','USES_AI_FOR','RAISES']
RETURN i.transcript_id AS interview, s.id AS segment, score, left(s.answer, 300) AS excerpt,
       collect(DISTINCT x.name)[..5] AS concepts;
```

(`r.status` is the extraction `status` field from [ADR-0010](decisions/0010-extraction-pipeline.md); add it to the relationship properties in 03.)

## Answer rules (system prompt sketch)

```
Answer only from tool output. Cite interview ids. Quote at most one sentence per source.
Say these are findings from a sample of AI-led interviews, not facts about workers in general.
If a tool returns nothing or asks for clarification, say so; do not guess. No tool for greetings or unrelated questions.
```

## Global questions

"What are the main themes?" cannot be answered by nearest-neighbour retrieval. Pre-compute `Theme` nodes by community detection on canonical-concept co-occurrence and have `qwen2.5:32b`
summarise each one offline, each summary citing member concepts and counts. This is the GraphRAG-style feature the helpdesk data could not justify.

## Optional: gated text-to-Cypher

Off by default; same guards as before (read mode, `EXPLAIN`, write and `CALL` rejection, `LIMIT`, timeout, schema from [03](03-graph-schema.md) in the prompt, a drafting model other than the orchestrator).
Enable only if the eval shows questions the typed tools cannot answer.

## ollmcp wiring

```json
{"mcpServers": {"interview-graph": {"command": ".venv/bin/python", "args": ["-W", "ignore", "-m", "graphrag.mcp_server"],
  "env": {"PYTHONPATH": "src", "NEO4J_URI": "bolt://localhost:7687", "NEO4J_USER": "neo4j"}}}}
```

```bash
ollmcp --servers-json mcp.json --model qwen3:8b-16k
```

`NEO4J_PASSWORD` is read from `.env`. Nothing may print to stdout except MCP messages.
