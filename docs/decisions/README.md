# Decision records

Format: **MADR-style** (status, context, decision drivers, options, outcome, consequences, confirmation), extended with a **weighted decision matrix**
and a **reversibility** rating so each choice shows how costly it is to undo.

> Note on "Jev-style decision models": that term turned out to mean Ollama's typed **decision models** (`/v1/systemone`, for example `nimble`), not a record format.
> They are now part of the design: see [ADR-0008](0008-decision-model-router.md). The ADRs themselves still use MADR plus weighted matrices.

## How to read the matrices

- Criteria weights sum to 100. Scores run 1 (poor) to 5 (excellent). Weighted score = sum(weight x score) / 100.
- **Scores are my judgment from the evidence in this repo and the cited docs, not benchmarks.** Where a score rests on something I did not measure, the record says so.
- Change a weight and recompute: if the winner flips, the decision is sensitive to that weight, and the record says where that happens.
- A matrix informs the decision; it does not make it. Close margins (under about 0.4) are called out and left to the stated tie-break.
- Reversibility: **Easy** (hours, no data migration), **Moderate** (a day, some rework), **Hard** (rewrite or data migration).

## Index

| ADR | Title | Outcome | Reversibility | Status |
|---|---|---|---|---|
| [0001](0001-graph-database.md) | Graph database | Neo4j Community 5.x | Moderate | accepted 2026-11-10 |
| [0002](0002-graph-construction.md) | Graph construction (helpdesk) | Deterministic from tables | Easy | superseded by 0010 |
| [0003](0003-retrieval-strategy.md) | Retrieval (helpdesk) | Keep Qdrant | Easy | superseded by 0011 |
| [0004](0004-query-interface.md) | Query interface | Typed Cypher tools | Easy | accepted 2026-11-10 |
| [0005](0005-local-llm-selection.md) | Local LLM selection | qwen3:8b-16k, 32b offline | Easy | accepted 2026-11-10 |
| [0006](0006-deployment-topology.md) | Deployment topology | Host Ollama and ollmcp, Neo4j in Docker | Easy | accepted 2026-11-10 |
| [0007](0007-privacy-and-access.md) | Privacy (helpdesk) | Public comments only | Moderate | superseded by 0012 |
| [0008](0008-decision-model-router.md) | Decision model as router | `nimble` routes | Easy | accepted 2026-11-10 (p95 under 2 s; router v3) |
| [0009](0009-corpus-anthropic-interviewer.md) | Corpus | Anthropic Interviewer | Moderate | **accepted** |
| [0010](0010-extraction-pipeline.md) | Extraction pipeline | Per-transcript extract, ground, verify, normalise | Easy | accepted 2026-11-10 |
| [0011](0011-retrieval-in-neo4j.md) | Retrieval | Neo4j vector index | Easy | accepted 2026-11-10 |
| [0012](0012-privacy-for-transcripts.md) | Privacy and licensing | Never commit data; attribution | Moderate | accepted 2026-11-10 |
| [0013](0013-waive-human-labels.md) | Human labels | Waived for the demo; Gate 1 waived, not passed | Easy | accepted |

Process: new decisions get the next number; a changed decision gets a **new** record that marks the old one `superseded by ADR-XXXX`. Do not edit accepted records
except to fix typos. Use [0000-template.md](0000-template.md).

## Open questions for you

1. (Resolved: human labels waived, [ADR-0013](0013-waive-human-labels.md).)
2. (Resolved 2026-11-10: 500 transcripts, all creatives and scientists plus 250 workforce, is the final scope.)
