# ADR-0003: Vector retrieval and graph expansion

- Status: superseded by [ADR-0011](0011-retrieval-in-neo4j.md) (Qdrant is dropped; there is no tuned pipeline to preserve)
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Both stores can coexist; the choice is which one the tool calls first.

## Context

helpdesk-rag's retrieval is tuned and measured: dense + BM25 with RRF, candidates grouped by problem (pool recall 0.74 to 0.95), rerank on the summary (0.95 vs 0.89 on full text),
relative cutoff and answer floor. Fine-tuning and embedder swaps gave no gain. Neo4j (5.11 and later) has a native vector index, so a single-database design is possible, but
it has no BM25-plus-RRF pipeline of the same shape and none of the tuning above would carry over for free.

## Decision drivers

- No regression on a retrieval path that already works
- Number of moving parts
- Ability to express "vector search then traversal" in one query
- Memory in the 8 GB Docker VM
- Ability to attribute a change in quality to the graph and nothing else

## Options

1. **Qdrant retrieval, then graph expansion by problem key** (graph tool calls the existing `retrieve_docs`)
2. Neo4j vector index only; drop Qdrant
3. Both vector stores kept in sync (dual write)
4. Graph-only retrieval (full-text/keyword in Neo4j)

## Weighted decision matrix

| Criterion | Weight | 1. Qdrant + expand | 2. Neo4j vectors only | 3. Dual | 4. Graph-only |
|---|---|---|---|---|---|
| No regression risk | 30 | 5 | 2 | 4 | 1 |
| Fewest moving parts | 20 | 3 | 5 | 2 | 5 |
| Single-query hybrid expressiveness | 20 | 3 | 5 | 4 | 2 |
| Memory in Docker | 15 | 4 | 5 | 3 | 5 |
| Clean attribution in the eval | 15 | 5 | 3 | 4 | 3 |
| **Weighted score (out of 5)** | 100 | **4.05** | 3.80 | 3.45 | 2.90 |

The top two are close (0.25). Tie-break: prefer the option that cannot make symptom recall worse, because the whole evaluation depends on a clean baseline.

## Decision

Keep **Qdrant** as the semantic entry point. The graph tool resolves hits to `Problem` nodes by the shared problem key, then expands with Cypher.
Do not add a Neo4j vector index in phase 1 or 2.

## Consequences

- Good: zero retrieval regression; the existing eval still applies; the graph's contribution is isolated.
- Costs: two stores; a key-join that must stay consistent (shared normalizer plus a test).
- Cannot do "vector search and traversal in a single Cypher statement" yet.

## Confirmation

Phase 1 join test: every distinct Qdrant summary maps to exactly one `Problem`. Phase 3: symptom hit@5 for config B within noise of the baseline 0.95.

## Revisit when

After the phase 3 eval, run one experiment: add a vector index on `Problem.embedding` (56 vectors) and compare the two paths on the control questions. If equal, consider
consolidating to simplify operations, as a new ADR that supersedes this one.
