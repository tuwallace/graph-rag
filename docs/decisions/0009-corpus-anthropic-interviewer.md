# ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets

- Status: accepted by twallace on 2026-11-05; spike completed, verdict go with scope and prompt changes (see [spike 01](../spike-01-extraction.md))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Moderate. The Neo4j, MCP and ollmcp plumbing carries over; the schema, loader and eval set do not.

## Context

The repo ([tuwallace/graph-rag](https://github.com/tuwallace/graph-rag)) is **public** and this is a **demo**. At the time of checking it held only `LICENSE` (MIT) and a README title; the docs in this directory exist locally only.

The helpdesk data ([01](../01-data-analysis.md)) is relational and templated: 56 distinct problems, 24 distinct comment bodies, random category per problem, 101 of 1,249 SLA rows matching. [ADR-0002](0002-graph-construction.md)
concluded that LLM extraction adds nothing there, which means the demo would show a graph database, not graph RAG.

Candidate: [Anthropic/AnthropicInterviewer](https://huggingface.co/datasets/Anthropic/AnthropicInterviewer) (from the dataset page and one sampled row; I did not download the dataset):

| Property | Value |
|---|---|
| Content | Transcripts of AI-led interviews with professionals about using AI at work |
| Splits | `workforce` 1,000, `creatives` 125, `scientists` 125 (1,250 total) |
| Schema | `transcript_id` (e.g. `work_0000`), `text` (4.84k to 26.8k characters) |
| Size | 11.4 MB CSV |
| License | Data CC-BY, code MIT; page says participants consented to public release |
| Sampled transcript | 27 turns, about 650 words; speaker labels vary within one transcript ("Assistant:", "AI:", "User:"); interviewer follows a fixed guide (workflow, triggers, interaction pattern, a critical incident, skills, future); no names or employers seen in that one row |

Not known: whether any transcript contains identifying details (the page describes no anonymization), how long the others are in turns, and what the associated paper's own coding of themes is (I have not read it).

## Decision drivers

- Does the data make a graph worth building (relationships live in prose, not in columns)?
- Is the data real and the questions meaningful?
- License fit for a public repo
- Feasible on one Mac with 8B-class local models
- Can answers be checked?
- Reuse of work already done

## Options

1. A. Helpdesk tickets only (current design)
2. **B. Anthropic Interviewer only**
3. C. Both corpora

## Weighted decision matrix

| Criterion | Weight | A. Helpdesk | B. Interviewer | C. Both |
|---|---|---|---|---|
| Demonstrates what graph RAG adds | 30 | 2 | 5 | 5 |
| Real data, meaningful questions | 15 | 2 | 5 | 4 |
| License fit for a public repo | 15 | 2 | 5 | 4 |
| Feasible locally | 15 | 5 | 3 | 2 |
| Evaluable (ground truth) | 15 | 4 | 2 | 3 |
| Reuse of existing design | 10 | 5 | 2 | 4 |
| **Weighted score (out of 5)** | 100 | **3.05** | **3.95** | 3.85 |

B and C are within 0.10. Tie-break: scope. Two corpora means two schemas, two loaders and two eval sets for a demo. Helpdesk stays in the repo history as the tabular variant.
License note for A: CC-BY-NC-4.0 is allowed in a public repo, but its non-commercial term constrains anyone who reuses the demo.

The weak spots in B are real: no structured side tables, no labelled answers, and extraction runs on local models that this project has seen struggle (ADR-0002 evidence).

## Decision (recommended, pending your confirmation)

Make **Anthropic Interviewer the primary corpus**. Keep helpdesk as a documented secondary variant, not maintained in step.

## Impact on the existing design

| Area | Change |
|---|---|
| ADR-0002 (graph build) | **Reversed for this corpus.** Extraction is now the point. Use a hybrid: decision model (`nimble`) for typed per-segment attributes, `qwen3:8b-16k` for open entities; every extracted node keeps `transcript_id` and turn provenance. |
| ADR-0003 (retrieval) | The corpus is text, so chunk retrieval is the entry point. A Neo4j vector index on `Segment` becomes attractive (one store, one query for vector then traversal); Qdrant is no longer required. Re-run the matrix. |
| ADR-0004 (query interface) | Typed tools still apply for aggregates ("how many creatives report job anxiety?"). Add a **global** route that answers from community/theme summaries, the GraphRAG feature helpdesk could not justify. |
| ADR-0005 (models) | Extraction dominates cost: estimate hours of `qwen3:8b` time for 1,250 transcripts (**unmeasured; time 20 transcripts first**). Run the 125-row `creatives` and `scientists` splits before `workforce`. `qwen2.5:32b` is too slow to extract with at this size; use it as offline judge on a sample. |
| ADR-0007 (privacy) | Public repo: **never commit the dataset or extracted graph dumps**; fetch at setup like helpdesk-rag does. Add CC-BY attribution. Add a scan for names, emails, employers before anything is shown or logged. |
| ADR-0008 (decision model) | Becomes more useful: `choice`/`score`/yes-no questions per segment (for example attitude toward AI, task category, mentions of job displacement) give typed, calibrated attributes with confidence. Test whether `nimble`'s context fits a segment; chunk by interviewer-participant turn pairs. |
| Schema ([03](../03-graph-schema.md)) | Replace the ticket model, sketched below. |
| Eval ([06](../06-evaluation-and-roadmap.md)) | Hardest part. Ground truth must be built: hand-label 30 to 50 segments, compute counts from those labels, score extraction precision and recall against them, and judge global answers with the offline model. No computed-by-SQL truth as with helpdesk. |

### Sketch of the new schema

```
(:Group {name})                      workforce | creatives | scientists
(:Interview {transcript_id})-[:IN_GROUP]->(:Group)
(:Interview)-[:HAS_SEGMENT]->(:Segment {idx, text, speaker_turns})   // 2-4 turns each, with embedding
(:Segment)-[:MENTIONS]->(:Task {name})            // what the person does or delegates
(:Segment)-[:MENTIONS]->(:AIUse {name})           // how AI is used (draft, search, code, brainstorm)
(:Segment)-[:EXPRESSES]->(:Attitude {kind, valence, confidence})   // decision-model output
(:Segment)-[:RAISES]->(:Concern {name})           // skills loss, trust, job security, ethics
(:Interview)-[:WORKS_AS]->(:Role {name})          // implied, normalised; often absent
(:Task|:Concern|:AIUse)-[:IN_THEME]->(:Theme)     // community detection, summarised for global questions
```

Provenance on every edge to `Segment`. Entity normalisation (merging "writing emails" and "drafting email") is the main quality risk; plan an embedding-based merge with a review sample.

## Consequences

- Good: a genuine graph RAG demo; real prose; permissive license; a single-database design; the decision-model router has more to do.
- Costs: extraction runtime and quality are the project's main risk; evaluation needs hand labels; more design to rewrite than a swap suggests.
- Risks: personal details in raw transcripts despite consent (mitigated by scanning and not republishing); misreading survey-like answers as facts about the population (state sample and interviewer limitations); entity duplicates inflating counts.

## Confirmation

Before committing to B: a 2-hour spike on 20 transcripts, measuring (1) extraction time per transcript with `qwen3:8b-16k`, (2) hand-checked precision on 100 extracted edges, (3) `nimble` attribute agreement with your own labels on 30 segments. If precision is under about 0.7, fall back to A or reduce extraction to the decision model's typed attributes only.

## Revisit when

The spike misses its thresholds, or a labelled slice of the paper's themes becomes available for ground truth.

## Outcome (added 2026-11-05)

Accepted: the Interviewer corpus replaces the helpdesk tickets. [Spike 01](../spike-01-extraction.md) ran the confirmation test: 31 s per transcript (about 10.8 h for all), roughly 0.87 strict and 0.70 lenient
precision on 30 items from one rater, `nimble` at p50 2.4 s per three-question call. Two thresholds above remain open (100-edge precision and `nimble` agreement with your labels) because no human labels exist yet.
Follow-on decisions: [0010](0010-extraction-pipeline.md), [0011](0011-retrieval-in-neo4j.md), [0012](0012-privacy-for-transcripts.md).
