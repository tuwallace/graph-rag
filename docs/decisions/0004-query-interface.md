# ADR-0004: Query interface the LLM uses

- Status: accepted 2026-11-10 by the project owner (earlier: proposed (amended 2026-11-05: still holds; tools and routes are in [04](../04-query-and-tools.md) for the Interviewer corpus))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Tools are thin wrappers over Cypher in code.

## Context

The model is a local 8B (`qwen3:8b-16k`) driven through ollmcp. Measured in this project: when the MCP tool had an optional `priority` argument, qwen3:8b filled it on every call,
and correct results dropped from 16/19 to 6/19; removing the argument fixed it. Text-to-Cypher asks the same model to author a whole query, a much larger surface for the same
failure (wrong labels, invented properties, wrong direction, missing `LIMIT`).

Options for exposing Neo4j to the model include the official Neo4j MCP Cypher server, which gives the model a read-query tool and a schema tool. I recall it also having a write tool
and a read-only mode; verify against the version you would install before relying on that.

## Decision drivers

- Reliability with an 8B model
- Safety: no writes, bounded cost, no injection
- Coverage of the question types in [04](../04-query-and-tools.md)
- Debuggability: can a failure be traced to one query?
- Effort

## Options

1. **Typed tools**: fixed parameterized Cypher, enum arguments
2. Free text-to-Cypher by the orchestrator model
3. Official `mcp-neo4j-cypher` server exposed directly
4. Typed tools, plus a **gated text-to-Cypher fallback** (separate drafting model, validation)

## Weighted decision matrix

| Criterion | Weight | 1. Typed | 2. Free T2C | 3. Official MCP | 4. Typed + gated T2C |
|---|---|---|---|---|---|
| Reliability on an 8B model | 35 | 5 | 2 | 2 | 4 |
| Safety (read-only, bounded) | 20 | 5 | 2 | 2 | 4 |
| Question coverage | 20 | 3 | 5 | 5 | 4 |
| Debuggability | 15 | 5 | 2 | 3 | 4 |
| Implementation effort | 10 | 3 | 5 | 5 | 2 |
| **Weighted score (out of 5)** | 100 | **4.40** | 2.90 | 3.05 | 3.80 |

Sensitivity: options 2 and 3 only close the gap if question coverage is weighted far above reliability and safety, which does not fit a model with the measured failure above.

## Decision

(Updated by [ADR-0008](0008-decision-model-router.md): a decision model routes and fills enum arguments, and the typed queries below become the internal layer behind one `ask_helpdesk` tool. The reasoning here still holds.)

Ship **typed tools only** (five of them) in phases 1 to 3. Hold option 4 as a conditional phase 4 addition, enabled only if the evaluation shows questions the typed set cannot answer
and the gated path beats "no answer" on them.

## Consequences

- Good: predictable, testable, safe; each tool has one query to profile; Cypher injection is structurally avoided (parameters only).
- Costs: new question shapes need a new tool or template; coverage is bounded by what was written.
- Mitigation: log unanswered question types and review them; promote recurring ones into tools.

## Confirmation

The eval's tool-selection accuracy and correctness (config B vs C) in [06](../06-evaluation-and-roadmap.md); a count of questions where the model said "I cannot answer that".

## Revisit when

More than about 15 percent of reasonable held-out questions have no matching tool, or the orchestrator changes to a model that handles open tool arguments reliably.
