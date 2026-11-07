# Graph RAG demo: Anthropic Interviewer transcripts

Status: **built and evaluated as a demo** (milestones M1 to M8 done; M9 publish in progress, 2026-11-07). Public demo repository ([tuwallace/graph-rag](https://github.com/tuwallace/graph-rag)).

The corpus is [Anthropic/AnthropicInterviewer](https://huggingface.co/datasets/Anthropic/AnthropicInterviewer): 1,250 transcripts of AI-led interviews about using AI at work
(CC-BY per the dataset card body; the card's front matter says `mit`; attribute Anthropic). It replaced the earlier synthetic helpdesk-ticket data ([archive](archive/helpdesk/README.md)).
Stack: Ollama (qwen3, `nimble` decision model, nomic-embed-text), ollmcp, Docker (Neo4j Community).

## Read in this order

| Doc | Purpose |
|---|---|
| [01-data-analysis.md](01-data-analysis.md) | What the corpus is and its risks |
| [spike-01-extraction.md](spike-01-extraction.md) | **Measured**: can local models build the graph? Results and verdict |
| [labeling-guide.md](labeling-guide.md) | Optional human labelling (waived for the demo) |
| [02-architecture.md](02-architecture.md) | Components, flows, resource budget |
| [03-graph-schema.md](03-graph-schema.md) | Nodes, edges, provenance, pipeline |
| [04-query-and-tools.md](04-query-and-tools.md) | Routing with `nimble`, MCP tools, Cypher |
| [05-components.md](05-components.md) | Component choices, compose file, throughput |
| [06-evaluation-and-roadmap.md](06-evaluation-and-roadmap.md) | Labelling plan, metrics, phases, risks |
| [07-implementation-roadmap.md](07-implementation-roadmap.md) | **Build order**, gates, fallbacks, first three actions |
| [08-evaluation-results.md](08-evaluation-results.md) | M7 results: configs A, B, C on 40 questions |
| [decisions/](decisions/README.md) | Decision records with weighted matrices |

## What the spike found (20 transcripts, one machine)

- Extraction with `qwen3:8b-16k` is **valid and auditable but slow**: 31 s per transcript, about 10.8 h for everything; demo scope is 500 transcripts (about 4.3 h).
- Precision on a 30-item read was about 0.87 strict and 0.70 lenient (one rater, me); the main errors are wishes and predictions extracted as facts.
- A prompt example leaked into the data until I removed it; counts would have been silently wrong.
- Names almost never repeat (115 distinct of 123 task items), so **normalisation is required** before any counting.
- `nimble` worked on all 208 segments but at 2.4 s per call (3 questions), not the 91 ms in the blog post, and agrees with qwen3 on overall attitude for 15 of 20 transcripts.

## Decisions at a glance

| ADR | Decision | Status |
|---|---|---|
| [0009](decisions/0009-corpus-anthropic-interviewer.md) | Corpus: Interviewer instead of helpdesk | accepted by you; spike done |
| [0010](decisions/0010-extraction-pipeline.md) | Extraction, grounding, `nimble` verification, normalisation; 500-transcript scope | proposed |
| [0011](decisions/0011-retrieval-in-neo4j.md) | Neo4j vector index; Qdrant dropped | proposed |
| [0012](decisions/0012-privacy-for-transcripts.md) | Never commit data; attribution; PII pass | proposed |
| [0013](decisions/0013-waive-human-labels.md) | Proceed without human labels (Gate 1 waived, not passed) | accepted |
| [0008](decisions/0008-decision-model-router.md) | `nimble` routes; one `ask_interviews` tool | proposed |
| [0001](decisions/0001-graph-database.md), [0005](decisions/0005-local-llm-selection.md), [0006](decisions/0006-deployment-topology.md) | Neo4j Community; model roles; topology | proposed, amended |
| [0002](decisions/0002-graph-construction.md), [0003](decisions/0003-retrieval-strategy.md), [0007](decisions/0007-privacy-and-access.md) | Helpdesk-era decisions | superseded by 0010, 0011, 0012 |
| [0004](decisions/0004-query-interface.md) | Typed tools over text-to-Cypher | proposed, still holds |

## What I need from you

Nothing is required. Human labelling is **waived for the demo** ([ADR-0013](decisions/0013-waive-human-labels.md)); precision (0.74) and `nimble` agreement (0.63) are LLM-estimated. If you ever want a human check, see the [labelling guide](labeling-guide.md).
