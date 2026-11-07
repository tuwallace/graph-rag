# ADR-0002: How the graph is built

- Status: superseded by [ADR-0010](0010-extraction-pipeline.md) (written for the helpdesk tables; extraction is now justified)
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. The graph is derived and rebuildable from the CSVs in seconds.

## Context

"GraphRAG" usually means LLM-extracted entities and relations from unstructured text, then community summaries (Microsoft GraphRAG, LightRAG, `neo4j-graphrag` pipelines).
This dataset is different ([01](../01-data-analysis.md)): five relational tables, 56 distinct problems, 24 distinct comment bodies. The structure is already explicit in foreign keys.

Evidence on local extraction quality from this project: graphify, using a local 7B model, extracted almost nothing from one generated document
(`live-recording-guide.md` stayed a single edge-less node even after a retry; see `Session_Logs.md`, 2026-10-21 entry). That is a different task (code and docs, not tickets) but it is
direct evidence of how a local 7B model behaves as an extractor.

## Decision drivers

- Fidelity: do not invent edges the data does not contain
- Reproducibility: same input gives the same graph
- Cost and latency on a local 8B model
- Added signal over what the columns already give
- Implementation effort

## Options

1. **Deterministic mapping from tables** (pandas to Cypher `MERGE`)
2. LLM extraction per ticket (`neo4j-graphrag`, LightRAG style)
3. Microsoft GraphRAG: extraction plus community detection plus summaries
4. Hybrid: deterministic core now, LLM extraction added later for free-text fields

## Weighted decision matrix

| Criterion | Weight | 1. Deterministic | 2. LLM per ticket | 3. MS GraphRAG | 4. Hybrid |
|---|---|---|---|---|---|
| Fidelity to the data | 30 | 5 | 2 | 1 | 4 |
| Cost / latency on local 8B | 20 | 5 | 2 | 1 | 4 |
| Reproducibility | 20 | 5 | 2 | 2 | 4 |
| Added signal over the columns | 20 | 3 | 3 | 2 | 4 |
| Implementation effort | 10 | 5 | 3 | 1 | 3 |
| **Weighted score (out of 5)** | 100 | **4.60** | 2.30 | 1.40 | 3.90 |

Option 4 scores lower today because most of its extra cost buys nothing yet. It becomes the right answer once the data has real free text (see Revisit).

## Decision

Build the graph **deterministically** from the tables. Use an LLM at **query time only** (routing and answering), never at load time. Derive `COMMONLY_DONE` and `CO_OCCURS` with
plain Cypher aggregation, with scores stored on the edges.

## Consequences

- Good: fast, exact, testable (row counts must match); no GPU contention at load time; no hallucinated edges.
- Costs: no discovery of structure that is only in prose. Not a loss on this data.
- Community summaries (the headline GraphRAG feature for "global" questions) are not built. Global questions are answered by aggregate Cypher instead.
- Risk: someone reads "GraphRAG" and expects entity extraction. Mitigation: the README states this decision up front.

## Confirmation

Load test: node and edge counts equal the CSV-derived expectations; reloading twice changes nothing (idempotent `MERGE`).

## Revisit when

A dataset arrives with real free-text resolution notes or knowledge-base articles. Then add LLM extraction of `Symptom`, `RootCause` and `Fix` nodes with source
ticket IDs as provenance, using the 32b model offline, and re-evaluate. Supersede this record, do not edit it.
