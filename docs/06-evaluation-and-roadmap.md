# 06. Evaluation and roadmap

## The honest problem

There are no labels. Evaluation is the hardest part of this project and the part most likely to be skipped. Ground truth must be built by hand.

## Labelling plan (as run: model labels, confirmed by the owner; see [ADR-0013](decisions/0013-waive-human-labels.md) and [09](09-completion-status.md))

The project ran with model labels instead of hand labels: `qwen3` and `nimble` during the build, and `qwen2.5:32b` for the independent precision, recall and question checks (precision 78% strict, 90% counting hypothetical; the owner confirmed the labels and reviewed the generated questions). The table below is what a full human check would cover; it is not planned.

| Set | Size | Task | Closes |
|---|---|---|---|
| Edge precision | 100 extracted edges (sampled across groups) | Mark each: correct, wrong, or hypothetical-as-fact | [ADR-0010](decisions/0010-extraction-pipeline.md) precision threshold |
| Attitude labels | 30 segments | positive / negative / mixed / none | `nimble` agreement (unfinished in [spike 01](spike-01-extraction.md)) |
| Recall check | 10 transcripts | List concepts you would extract; compare with what was extracted | Missing recall, not measured so far |
| Router set | 40 questions | Write questions, assign the route | Router accuracy and abstention |
| Retrieval set | 10 queries | Mark relevant segment ids | [ADR-0011](decisions/0011-retrieval-in-neo4j.md) recall at 5 |

Hold half of the questions back until the end. Review files can be generated from `data/spike_review_sample.json`-style dumps (git-ignored; they contain transcript text).

## Metrics

| Layer | Metric | Target |
|---|---|---|
| Extraction | Precision on hand labels, with and without the verify step | at least 0.80 with verify (ADR-0010) |
| Extraction | Fuzzy grounding rate | at least 90% |
| Extraction | Prompt-hygiene check | zero failures |
| Normalisation | Canonical nodes per 100 raw names; sampled merge errors | report; no target yet |
| Attributes | `nimble` vs your labels; confidence calibration | report agreement and calibration curve |
| Routing | Route accuracy and abstention rate at thresholds 0.5, 0.6, 0.7 | baseline first |
| Retrieval | recall at 5 | at least 0.7 |
| Answers | Every quote exists and belongs to the cited interview; counts equal the database | 100% |
| Answers | Groundedness of numbers (regex), then judge on a sample with `qwen2.5:32b` | 100% on numbers |
| Latency | End-to-end p50 and p95 per route | report |

Configurations: **A** qwen3 picks among the typed tools (6 tools visible), **B** `nimble` routes and one `ask_interviews` tool, **C** plain vector RAG with no graph (segments only, same answer model).
The graph earns its place only if B beats C on the count, comparison and global questions. Symptom-style local questions may not improve; say so if they do not.

## Phases (all done; see [07](07-implementation-roadmap.md) for dates and outcomes)

| Phase | Deliverable | Exit criteria |
|---|---|---|
| 0. Spike | [spike 01](spike-01-extraction.md) | Done: go with scope and prompt changes |
| 1. Setup | uv project, compose with Neo4j, `.env`, `.gitignore`, constraints | `RETURN 1` over Bolt; ports on localhost |
| 2. Extraction v2 | Fixed prompt, grounding, verify, rerun the same 20 | Your labels show precision at least 0.80 |
| 3. Build | 500 transcripts through all stages, normalisation, load | Counts consistent; every edge has a grounded quote |
| 4. Tools | `interview-graph` MCP server, router, typed queries | ollmcp lists the tools; smoke tests pass |
| 5. Eval | Label sets and configurations A, B, C | Results table, including where the graph did not help |
| 6. Themes | Community detection and offline summaries for global questions | Summaries cite member concepts |
| 7. Publish | README, attribution, PII pass, pre-push check | No data or quotes beyond short excerpts in git |

## Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Precision stays near 0.7 | Medium | Verify step; reduce to typed attributes only ([ADR-0010](decisions/0010-extraction-pipeline.md) fallback) |
| Run time overruns | High | 500-transcript scope, resumable stages, overnight runs, slim `nimble` calls |
| Normalisation merges distinct ideas or leaves duplicates | High | Sample review; keep aliases; report both error types |
| Router abstains too often | Medium | Measure on routing questions, tune threshold, test `tev1` |
| Accidentally committing transcripts or quotes | Medium | `.gitignore`, pre-push check ([ADR-0012](decisions/0012-privacy-for-transcripts.md)) |
| Over-claiming from a self-selected, AI-interviewed sample | Medium | Answer rules say so; report n and limits |
| Docker VM memory (8 GB shared) | Medium | Heap caps; stop other stacks |
