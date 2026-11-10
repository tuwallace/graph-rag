# ADR-0011: Retrieval for the transcript corpus

- Status: accepted 2026-11-10 by the project owner (earlier: proposed (supersedes [ADR-0003](0003-retrieval-strategy.md)))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Embeddings are recomputable; both options read the same segments.

## Context

ADR-0003 kept Qdrant because helpdesk-rag's retrieval was tuned and measured. This corpus has no such pipeline: it is about 14,500 segments with no existing index.
The data is small (about 14.5k vectors of 768 dimensions, roughly 45 MB as float32), and the graph traversal after retrieval is the point. Neo4j 5.11 and later has a native vector index.
Dependence on helpdesk-rag also disappears.

## Options

1. A. Neo4j vector index on `Segment.embedding` (one database)
2. B. Qdrant plus Neo4j (as in ADR-0003)
3. C. Neo4j vector index plus full-text index, fused (hybrid)

## Weighted decision matrix

| Criterion | Weight | A. Neo4j vectors | B. Qdrant + Neo4j | C. Neo4j hybrid |
|---|---|---|---|---|
| Fewest moving parts (8 GB Docker VM) | 30 | 5 | 2 | 5 |
| Vector search plus traversal in one query | 25 | 5 | 2 | 5 |
| Retrieval quality headroom | 20 | 3 | 4 | 4 |
| Effort | 15 | 4 | 2 | 3 |
| Reuse of existing code | 10 | 2 | 4 | 2 |
| **Weighted score (out of 5)** | 100 | 4.15 | 2.60 | 4.20 |

A and C are within noise (0.05). The full-text index is a Cypher one-liner, so tie-break on effort: start with A and add C only if a retrieval check shows lexical misses.

## Decision

Start with **A**: embed each segment (`question + answer`) with `nomic-embed-text` using `search_document:` and `search_query:` prefixes, and index it in Neo4j. No Qdrant, no Phoenix dependency
on helpdesk-rag. Add the full-text index (option C) if needed.

## Consequences

- Good: one store; one query for "nearest segments, then their concepts and quotes"; simpler compose file.
- Costs: no reranker and no tuned BM25 pipeline; quality is unmeasured until the eval exists.
- Risk: weak recall on short answers. Mitigation: embed question plus answer; check against hand-written queries before building more.

## Confirmation

Ten hand-written queries with known relevant segments (from your labelling session); recall at 5 reported before any answer-quality evaluation.

## Revisit when

Recall at 5 is under about 0.7: add the full-text index, then a cross-encoder reranker.
