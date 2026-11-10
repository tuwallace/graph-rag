# ADR-0008: Decision model (Jev-style) as the question router

- Status: accepted 2026-11-07 on accuracy and argument errors; the latency bound is amended to p95 under 2 s and was accepted by the project owner on 2026-11-07 (see "Confirmation result"). Earlier: proposed (amended 2026-11-05: routes, verification and attributes now target transcripts; see [spike 01](../spike-01-extraction.md) for measured latency)
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. The router is one function; the typed tools underneath do not change.

## Context

Ollama (server 0.40.14 here) serves a `/v1/systemone` endpoint for **decision models**: a small model takes a `state` (text) and named typed `questions`
(`choice`, `score`, and a yes/no type the blog calls `noul`) and returns an answer **with per-option probabilities and a confidence value**, typically with zero generated tokens.
Source: [Ollama blog post](https://ollama.com/blog/ollama-now-supports-jev-style-decision-models). The post describes `nimble` (9B) as the main model and says it averages about 91 ms per decision
on an M5 Max; I have not measured speed on your M2 Pro. `nimble:latest` (9.3 GB) is already installed.

Tested locally: a `choice` question with four routes sent four sample questions
("VPN drops every hour, any past fixes?", "Which problems get escalated most?", "Which team resolves network tickets fastest?", "whats 2+2") and got
`symptom_lookup`, `aggregate_ranking`, `agent_stats`, `out_of_scope`, all correct, with confidence 0.93 to 0.99. That is 4 questions, not an evaluation. The `noul` type was not tested.
Request note: `criteria` must be an object mapping option keys to descriptions (an array returns an error).

This matters because [ADR-0004](0004-query-interface.md) rests on one measured weakness: qwen3:8b over-fills optional arguments and mis-picks among tools. A decision model returns a
constrained choice with a probability, so it can **abstain** (low confidence) instead of guessing.

## Decision drivers

- Routing reliability, measured on the eval set
- Ability to abstain or ask for clarification when unsure
- Latency
- Memory (nimble is 9.3 GB beside qwen3 5.2 GB, on a host that also gives 8 GB to Docker)
- Complexity
- Transparency in ollmcp (seeing the model choose tools is part of the learning goal)

## Options

1. **A. Orchestrator picks among 5 tools** (current design)
2. **B. Decision model routes; one MCP tool `ask_helpdesk(question)`**; the server dispatches to the typed query; qwen3 only writes the answer
3. **C. Decision model as a pre-filter** (scope and route check) while all 5 tools stay visible to qwen3
4. D. Keyword/regex rules

## Weighted decision matrix

| Criterion | Weight | A. qwen3 picks | B. Router + 1 tool | C. Pre-filter + 5 tools | D. Rules |
|---|---|---|---|---|---|
| Routing reliability | 35 | 3 | 4 | 4 | 2 |
| Can abstain with calibrated confidence | 20 | 2 | 5 | 5 | 1 |
| Latency | 15 | 3 | 5 | 4 | 5 |
| Memory fit | 10 | 5 | 3 | 3 | 5 |
| Simplicity | 10 | 5 | 3 | 2 | 4 |
| Transparency in ollmcp | 10 | 5 | 3 | 4 | 4 |
| **Weighted score (out of 5)** | 100 | **3.40** | **4.05** | 3.90 | 2.95 |

The B and C gap (0.15) is within noise of my scoring. The reliability scores for A, B and C are not measured: B and C reflect the 4/4 trial above, A reflects the earlier measured argument-filling failure.

## Decision

Adopt a decision model as the router, in the shape of **B**, and keep **A** as an eval baseline (config A/B/C in 06 gain a router config).

- One MCP tool: `ask_helpdesk(question: str)`. Inside it: (1) `route` as a `choice` over `symptom_lookup | aggregate_ranking | agent_stats | related | profile | out_of_scope`;
  (2) for rankings, further `choice` questions fill the enums (`metric`, `group_by`), so the 8B model never fills arguments; (3) dispatch to the typed Cypher query; (4) return compact JSON.
- **Confidence gate**: if the top option's confidence is below a threshold (start at 0.6, tune on the eval set), return a clarification note and run nothing. Out-of-scope returns the existing "tell the user to open a ticket" note.
- The typed query tools from [04](../04-query-and-tools.md) stay as the internal layer, and stay exposed in a second `mcp.json` profile so config A (qwen3 picks among tools) can still be compared.
- Model: `nimble`. The experimental `tev1` models (4B, 0.8B) are worth testing as lighter routers; I did not test them.

## Consequences

- Good: constrained, typed, probabilistic routing; abstention for free; qwen3 no longer authors arguments; fewer tokens in the orchestrator's context.
- Costs: a second resident model (9.3 GB). Set `OLLAMA_MAX_LOADED_MODELS=2` or accept reload latency; check `docker stats` and `ollama ps`.
- The ollmcp demonstration of "model chooses among tools" is hidden inside one tool. Mitigation: config A keeps it visible; Phoenix spans show the route, probabilities and confidence.
- Risks: the endpoint is new (my ollama client is 0.35.1 against a 0.40.14 server, with a version-mismatch warning) and the model line is described as experimental in places. Mitigation: pin the Ollama version in docs; fall back to config A if the endpoint disappears.
- Routing gives probabilities, not guarantees. Phrases that mix intents ("which VPN problems escalate most and what was done?") need either two calls or a `compound` route; add such cases to the eval set.

## Confirmation

Route accuracy and abstention rate on the 40-question set (06), against config A. Required before this is accepted: router accuracy at least equal to config A on tool selection, with fewer wrong-argument calls, and p95 router latency under 1 s on this machine.

## Revisit when

Router accuracy is below config A, or the memory cost forces choosing between nimble and the orchestrator.

## M3 note (2026-11-06)

`nimble` is now used in the build for two things: item verification (yes/no, about 1.0 s per item) and segment attitude (one choice, about 1.7 s per segment). Topic and job-worry attributes were dropped (no value in 50 segments).
Cold latency is 1 to 2 s per call; identical requests repeated within seconds return in well under a second (prompt cache), so benchmark with fresh inputs. The router role for questions (above) is unchanged and still untested at scale.

## Confirmation result (2026-11-07)

Three tests were required: router accuracy at least equal to config A on tool selection; fewer wrong-argument calls; p95 router latency under 1 s. Evidence: the 40-question set (M7, dev/held-out halves) and 20 new questions written after the router changes below were chosen (`eval/confirm_questions.json`, run by `eval/confirm_adr0008.py`). Routing and arguments only; one run each; small n, so differences of one or two questions are noise.

Changes made after M7, justified by the dev half only: confidence threshold 0.6 to 0.5 (dev abstention 11% to 5% at the same accuracy when answering), and concept matching now prefers the longer span on ties (fixed "verification burden" resolving to "verification"). Router version `v2`.

| Test | Result | Verdict |
|---|---|---|
| Route accuracy, fresh 20 (18 in scope) | B 17/18 (94%), A 16/18 (89%) | Met (B at least A) |
| Route accuracy, original 40 (36 in scope), router v2 | B 33/36 (92%); A 31/36 (86%) from M7 | Met |
| Wrong-argument calls, fresh 20 (13 with arguments) | B 1, A 2 | Met, directionally |
| Wrong-argument calls, original 40 (24 with arguments) | B 1 (router v2), A 3 | Met, directionally (B was 3 under v1; two of those fixes were chosen after seeing these questions, so the fresh set is the cleaner evidence) |
| Abstentions on in-scope questions | fresh 20: 1 of 18; original 40: 2 of 36 | Fine |
| Out-of-scope questions | 6/6 handled, none leaked at any threshold | Met |
| p95 router latency, fresh text (n = 20) | p50 1.13 s, **p95 1.57 s** | Not met against 1 s; **met against the accepted 2 s bound** |

Latency: the decision call is a near-constant 1.13 s (fresh inputs; 18 of 20 within 1.12 to 1.22 s, two at 1.57 s), not dependent on question length. Shortening the route descriptions cuts it to about 0.88 s but costs accuracy: on the dev half, one-line descriptions gave 18/21 correct with 6 of 21 below the 0.5 confidence gate, and bare route names gave 15/21 with 14 below the gate (full descriptions: 19/21, 1 below). `tev1` models are not installed here and were not tested. I therefore keep the full descriptions and **amend the bound to p95 under 2 s on this machine**, with the reason that the router adds about 1.1 s to an answer that takes about 5 s end to end and the faster variants abstain more often. The amendment was proposed by me after seeing the result and was **accepted by the project owner on 2026-11-07**, so p95 under 2 s is now the bound of record (the measured p95 of 1.57 s meets it). Revisit it if a lighter router (`tev1`) becomes available.

**Owner decisions (2026-11-10):** keep router v3 with the p95 under 2 s bound; ADR accepted.

**Router v3 (2026-11-09).** Boundary examples were added to the route descriptions to fix `theme_overview` confusions. Accuracy edged up (original 40: 34/36; confirmation 20: 18/18; a fresh 48-question set written by `qwen2.5:32b`: 30/40 against 23/40 for config A). Latency rose to p50 1.68 s and p95 1.98 s (n = 20, max 4.21 s), inside the accepted 2 s bound by a thin margin. If p95 exceeds 2 s in use, shorten the examples first.

Remaining weaknesses: a one-in-three miss on questions that mix a concept with a group ("Which group uses AI for code generation the most?" was routed as `concept_stats` by both A and B), and an overview question phrased as "biggest themes in how people use AI" routed to `concept_stats` (confidence 0.56). Add such mixed questions to a future eval set rather than tuning on them.
