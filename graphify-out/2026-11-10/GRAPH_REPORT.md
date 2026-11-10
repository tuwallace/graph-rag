# Graph Report - graph-rag  (2026-11-10)

## Corpus Check
- 98 files · ~59,218 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 720 nodes · 1275 edges · 54 communities (51 shown, 3 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 50 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f315826a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- extract.py
- mcp_server.py
- router.py
- 07. Implementation roadmap
- queries.py
- docs/README.md
- pathlib
- pipeline.py
- themes.py
- load.py
- score.py
- 03. Graph schema
- test_themes.py
- 05_make_label_sheets.py
- ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets
- json
- 04. Query routing and MCP tool surface
- ADR-NNNN: Title (the decision, as a short noun phrase)
- ADR-0010: Extraction pipeline for the transcripts
- run_eval.py
- test_router.py
- sys
- ADR-0001: Graph database
- ADR-0002: How the graph is built
- ADR-0003: Vector retrieval and graph expansion
- ADR-0004: Query interface the LLM uses
- ADR-0006: Deployment topology
- ADR-0007: Privacy and access control
- Spike 01: can local models build the graph from the transcripts?
- grounded_eval.py
- Label confirmation
- ADR-0005: Local LLM selection
- ADR-0011: Retrieval for the transcript corpus
- ground.py
- 09. Completion status (2026-11-10, final update: all planned tests run)
- test_load.py
- 02. Architecture
- ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus
- ADR-0013: Proceed without human labels for the demo
- interview-graph
- judge32b.py
- 08. Evaluation results (M7)
- ask_interviews
- pre-push
- graph-rag
- __init__.py
- concern_merge.py
- 04. Query routing and MCP tool surface (Interviewer corpus)
- Labelling guide (v3.2 sheets, about 2 hours)
- Concern pass applied to all 500 interviews (2026-11-09)
- 06. Evaluation and roadmap
- M4 outcome (done; finished 2026-11-06 22:51 local)
- Graph RAG demo: Anthropic Interviewer transcripts

## God Nodes (most connected - your core abstractions)
1. `07. Implementation roadmap` - 23 edges
2. `ask_interviews()` - 17 edges
3. `Stage` - 13 edges
4. `select()` - 12 edges
5. `segments()` - 11 edges
6. `answer()` - 11 edges
7. `ADR-0008: Decision model (Jev-style) as the question router` - 11 edges
8. `ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets` - 11 edges
9. `ADR-0010: Extraction pipeline for the transcripts` - 11 edges
10. `score()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Tool surface` --references--> `ask_interviews()`  [INFERRED]
  docs/04-query-and-tools.md → src/graphrag/mcp_server.py
- `Metrics` --references--> `ask_interviews()`  [INFERRED]
  docs/06-evaluation-and-roadmap.md → src/graphrag/mcp_server.py
- `What changed against the first run (all 40)` --references--> `ask_interviews()`  [INFERRED]
  docs/08-evaluation-results.md → src/graphrag/mcp_server.py
- `Decisions at a glance` --references--> `ask_interviews()`  [INFERRED]
  docs/README.md → src/graphrag/mcp_server.py
- `What was built` --references--> `ask_interviews()`  [INFERRED]
  README.md → src/graphrag/mcp_server.py

## Import Cycles
- None detected.

## Communities (54 total, 3 thin omitted)

### Community 0 - "extract.py"
Cohesion: 0.13
Nodes (18): build_prompt(), extract(), hygiene_failures(), Client, Extraction v3: one list of typed items per transcript, each with status,…, Names among the most frequent that appear verbatim in the prompt (a sign the…, locate(), Best participant answer for a quote: (segment idx, score). (+10 more)

### Community 1 - "mcp_server.py"
Cohesion: 0.11
Nodes (26): dotenv, cov(), os, Settings from environment / .env. No secrets in code., allowed_numbers(), items(), numbers(), quotes_in() (+18 more)

### Community 2 - "router.py"
Cohesion: 0.06
Nodes (39): 03. Graph schema (Interviewer corpus), Constraints and indexes, Decision-model attributes on `Segment` (properties, not nodes), Model, Nodes, Pipeline, Provenance rule, Relationships (all carry provenance) (+31 more)

### Community 3 - "07. Implementation roadmap"
Cohesion: 0.12
Nodes (16): 07. Implementation roadmap, ADR-0008 confirmation (2026-11-07), Critical path and parallel work, Decision points and fallbacks, First three actions, M1 outcome (2026-11-05), M2 outcome (2026-11-05), M3 outcome (2026-11-06) (+8 more)

### Community 4 - "queries.py"
Cohesion: 0.10
Nodes (26): hashlib, ndarray, canonicalise(), clean(), cluster(), embed(), Client, Merge near-duplicate extracted names into canonical concepts using embeddings… (+18 more)

### Community 5 - "docs/README.md"
Cohesion: 0.17
Nodes (10): 01. Data analysis: Anthropic Interviewer transcripts, Risks specific to this corpus, Shape, Structure, What a graph can add here, Archived: helpdesk-tickets design, Decision records, How to read the matrices (+2 more)

### Community 6 - "pathlib"
Cohesion: 0.09
Nodes (19): asyncio, fastmcp, fastmcp_client_transports, pathlib, Start the MCP server over stdio and call it like a client would. Usage:…, main(), participant_text(), PII residual checks from ADR-0012: phone formats, first names on their own,… (+11 more)

### Community 7 - "pipeline.py"
Cohesion: 0.10
Nodes (27): extract(), ids(), jl(), judge(), new_edges(), Second extraction pass for concerns with a looser prompt, on the 10 transcripts…, The 10 recall transcripts first; with CONCERN_SCOPE=all, then every other…, Kept new concern edges whose quote is not already the quote of an original kept… (+19 more)

### Community 8 - "themes.py"
Cohesion: 0.12
Nodes (21): M8 outcome (done 2026-11-07), itertools, math, networkx, fmt(), Score the v3.2 labelling sheets. Usage: uv run --with pandas python…, wilson(), fmt() (+13 more)

### Community 9 - "load.py"
Cohesion: 0.15
Nodes (19): build(), checks(), chunks(), counts(), edge_id(), embed_segments(), main(), M5: load an assembled run (graph_input.jsonl) into Neo4j. Idempotent (MERGE… (+11 more)

### Community 10 - "score.py"
Cohesion: 0.15
Nodes (16): f(), context_numbers(), evaluate(), load(), norm(), nums(), p95(), pct() (+8 more)

### Community 11 - "03. Graph schema"
Cohesion: 0.14
Nodes (12): 01. Data analysis: what a graph can honestly add, Findings that drive the design, Tables, What this means, 03. Graph schema, Constraints and indexes (Cypher), Derived (materialized) edges and properties, Evolution path (+4 more)

### Community 12 - "test_themes.py"
Cohesion: 0.47
Nodes (3): _by(), test_detect_separates_clusters_and_is_deterministic(), test_rare_concepts_excluded()

### Community 13 - "05_make_label_sheets.py"
Cohesion: 0.60
Nodes (4): best_pair(), norm(), pairs(), Build blind labelling sheets under data/labeling/ (git-ignored: they contain…

### Community 14 - "ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets"
Cohesion: 0.17
Nodes (12): ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets, Confirmation, Consequences, Context, Decision drivers, Decision (recommended, pending your confirmation), Impact on the existing design, Options (+4 more)

### Community 15 - "json"
Cohesion: 0.16
Nodes (9): collections, Attitude labels vs a larger model, and confidence calibration (final graph).…, Graph-wide precision check of the concern edges added by the all-500 concern…, Sampled check of entity normalisation (final graph), judged by qwen2.5:32b run…, Re-measure recall on the 10 transcripts of eval/judge32b.py recall, against the…, Run-to-run stability (final graph). Model-dependent steps are repeated with…, json, ollama (+1 more)

### Community 16 - "04. Query routing and MCP tool surface"
Cohesion: 0.20
Nodes (9): 04. Query routing and MCP tool surface, Design rule from the existing project, Example expansion query (used by `find_similar_problems`), ollmcp wiring, Optional: gated text-to-Cypher (phase 3, off by default), Question types and routes, Response shaping for a small model, System prompt additions (sketch) (+1 more)

### Community 17 - "ADR-NNNN: Title (the decision, as a short noun phrase)"
Cohesion: 0.20
Nodes (9): ADR-NNNN: Title (the decision, as a short noun phrase), Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 18 - "ADR-0010: Extraction pipeline for the transcripts"
Cohesion: 0.18
Nodes (11): ADR-0010: Extraction pipeline for the transcripts, Confirmation, Consequences, Context, Decision, Decision drivers, M3 amendments (2026-11-06), Options (+3 more)

### Community 19 - "run_eval.py"
Cohesion: 0.14
Nodes (13): b_row(), ADR-0008 confirmation on questions written after the router changes were chosen…, timed_decide(), Routing accuracy on questions written by a different model (qwen2.5:32b) from…, chat(), config_A(), config_B(), config_C() (+5 more)

### Community 20 - "test_router.py"
Cohesion: 0.31
Nodes (6): fake(), FakeIndex, test_concept_stats_low_enum_confidence_clarifies(), test_low_confidence_clarifies_and_runs_nothing(), test_out_of_scope_calls_no_query(), test_weak_concept_match_clarifies()

### Community 21 - "sys"
Cohesion: 0.16
Nodes (9): Gate 2 proxy: do the top-5 vector hits for 10 queries contain answers that…, pandas, pexpect, re, Drive a live ollmcp session (qwen3:8b-16k, routed profile, mcp.json) through a…, M2: rerun extraction v3 on the same 20 transcripts as the spike. Usage:…, statistics, sys (+1 more)

### Community 22 - "ADR-0001: Graph database"
Cohesion: 0.22
Nodes (9): ADR-0001: Graph database, Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 23 - "ADR-0002: How the graph is built"
Cohesion: 0.22
Nodes (9): ADR-0002: How the graph is built, Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 24 - "ADR-0003: Vector retrieval and graph expansion"
Cohesion: 0.22
Nodes (9): ADR-0003: Vector retrieval and graph expansion, Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 25 - "ADR-0004: Query interface the LLM uses"
Cohesion: 0.22
Nodes (9): ADR-0004: Query interface the LLM uses, Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 26 - "ADR-0006: Deployment topology"
Cohesion: 0.22
Nodes (9): ADR-0006: Deployment topology, Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 27 - "ADR-0007: Privacy and access control"
Cohesion: 0.22
Nodes (9): ADR-0007: Privacy and access control, Confirmation, Consequences, Context, Decision, Decision drivers, Options for internal comments, Revisit when (+1 more)

### Community 28 - "Spike 01: can local models build the graph from the transcripts?"
Cohesion: 0.22
Nodes (9): Addendum 2: v3.2 labels by Claude (2026-11-06), not a human result, Addendum: provisional labels by Claude (2026-11-05), not a human result, Against the ADR-0009 thresholds, Limits of this spike, Results, Setup, Spike 01: can local models build the graph from the transcripts?, Verdict (+1 more)

### Community 29 - "grounded_eval.py"
Cohesion: 0.50
Nodes (3): quality(), Re-measure groundedness with answer generation, through the grounded path…, score()

### Community 30 - "Label confirmation"
Cohesion: 0.25
Nodes (8): All 40, Dev half (tuning allowed), Held-out half, Label confirmation, Per-route latency (median s), Router abstention by threshold (All 40, route confidence only), Router abstention by threshold (Dev half (tuning allowed), route confidence only), Router abstention by threshold (Held-out half, route confidence only)

### Community 31 - "ADR-0005: Local LLM selection"
Cohesion: 0.25
Nodes (8): ADR-0005: Local LLM selection, Confirmation, Consequences, Context, Decision, Revisit when, Roles, Weighted decision matrix: orchestrator

### Community 32 - "ADR-0011: Retrieval for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0011: Retrieval for the transcript corpus, Confirmation, Consequences, Context, Decision, Options, Revisit when, Weighted decision matrix

### Community 33 - "ground.py"
Cohesion: 0.21
Nodes (11): difflib, Groundedness: what was needed (written 2026-11-07; built and measured below), match(), Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels).…, is_grounded(), Check that an extracted quote really comes from the participant (User turns),…, Fraction of quote tokens covered by in-order matching blocks of the haystack…, score() (+3 more)

### Community 35 - "09. Completion status (2026-11-10, final update: all planned tests run)"
Cohesion: 0.29
Nodes (7): 09. Completion status (2026-11-10, final update: all planned tests run), Decided by the owner (2026-11-10), Done, Housekeeping, Open: needs your decision (superseded by the section above; kept for the record), Targets in 06 against the evidence, Tests: all run (2026-11-10)

### Community 36 - "test_load.py"
Cohesion: 0.38
Nodes (4): E(), _run(), test_build_keeps_grounded_only(), test_embed_cache_reused()

### Community 37 - "02. Architecture"
Cohesion: 0.33
Nodes (6): 02. Architecture, Components, Failure handling, Resource budget, Routes (decided by `nimble`, see [04](04-query-and-tools.md)), Two flows

### Community 38 - "ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus, Confirmation, Consequences, Context, Decision, PII pass record (2026-11-07, before the first public commit), PII residual pass (2026-11-10), Revisit when

### Community 39 - "ADR-0013: Proceed without human labels for the demo"
Cohesion: 0.33
Nodes (6): ADR-0013: Proceed without human labels for the demo, Confirmation, Consequences, Context, Decision, Revisit when

### Community 40 - "interview-graph"
Cohesion: 0.33
Nodes (5): NEO4J_URI, NEO4J_USER, PYTHONPATH, .venv/bin/python, interview-graph

### Community 41 - "judge32b.py"
Cohesion: 0.15
Nodes (18): ADR-0008: Decision model (Jev-style) as the question router, Confirmation, Confirmation result (2026-11-07), Consequences, Context, Decision, Decision drivers, M3 note (2026-11-06) (+10 more)

### Community 42 - "08. Evaluation results (M7)"
Cohesion: 0.20
Nodes (10): 08. Evaluation results (M7), All 40, final graph, Attitude labels and calibration, Groundedness on the final graph (60 questions, `eval/grounded_eval.py`, router v3), Normalisation (merges and missed merges), Per-route end-to-end latency (median s), final graph, Re-run on the final graph (2026-11-10), Remaining tests (2026-11-10): stability, normalisation, attitude (+2 more)

### Community 43 - "ask_interviews"
Cohesion: 0.22
Nodes (11): Gate 2: retrieval check (proxy, no human labels), Groundedness: built and measured (2026-11-07), M6 outcome (done 2026-11-07) and Gate 2, Milestones, Fix attempt and re-test (2026-11-10), Live `ollmcp` session on the final graph (2026-11-10), grounded_answer(), Route, render, frame with the LLM, validate, fall back to the rendered facts on… (+3 more)

### Community 46 - "__init__.py"
Cohesion: 0.15
Nodes (4): csv, Consistency checks on the model-judged label files (data/eval/judge/,…, Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration,…, Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-…

### Community 47 - "concern_merge.py"
Cohesion: 0.09
Nodes (15): argparse, numpy, assign(), main(), new_items(), Merge the looser concern pass (eval/concern_pass.py) into an assembled run…, Map each new cleaned name to an existing canonical name (cos >= threshold) or…, dedupe() (+7 more)

### Community 48 - "04. Query routing and MCP tool surface (Interviewer corpus)"
Cohesion: 0.25
Nodes (8): 04. Query routing and MCP tool surface (Interviewer corpus), Answer rules (system prompt sketch), Example Cypher (parameterised, read-only), Global questions, ollmcp wiring, Optional: gated text-to-Cypher, Routes, Tool surface

### Community 49 - "Labelling guide (v3.2 sheets, about 2 hours)"
Cohesion: 0.29
Nodes (8): Files, How to fill in the CSV, Labelling guide (v3.2 sheets, about 2 hours), Reading the result, Score it, Sheet 1: edges, Sheet 2: attitude (30 rows), label()

### Community 50 - "Concern pass applied to all 500 interviews (2026-11-09)"
Cohesion: 0.50
Nodes (4): Concern pass applied to all 500 interviews (2026-11-09), Filter at verify 0.6 (2026-11-10, owner decision), Graph-wide check of the new concern edges (2026-11-10), Recall re-measured after the filter (2026-11-10)

### Community 51 - "06. Evaluation and roadmap"
Cohesion: 0.33
Nodes (6): 06. Evaluation and roadmap, Labelling plan (as run: model labels, confirmed by the owner; see [ADR-0013](decisions/0013-waive-human-labels.md) and [09](09-completion-status.md)), Metrics, Phases (all done; see [07](07-implementation-roadmap.md) for dates and outcomes), Risks, The honest problem

### Community 52 - "M4 outcome (done; finished 2026-11-06 22:51 local)"
Cohesion: 0.67
Nodes (3): Caveats carried forward, Finding: the run was interrupted once, 2026-11-06 19:44:41, M4 outcome (done; finished 2026-11-06 22:51 local)

### Community 53 - "Graph RAG demo: Anthropic Interviewer transcripts"
Cohesion: 0.40
Nodes (5): Decisions at a glance, Graph RAG demo: Anthropic Interviewer transcripts, Read in this order, What I need from you, What the spike found (20 transcripts, one machine)

## Knowledge Gaps
- **219 isolated node(s):** `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI`, `NEO4J_USER`, `graph-rag` (+214 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 372 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ask_interviews()` connect `ask_interviews` to `mcp_server.py`, `router.py`, `08. Evaluation results (M7)`, `04. Query routing and MCP tool surface (Interviewer corpus)`, `06. Evaluation and roadmap`, `Graph RAG demo: Anthropic Interviewer transcripts`?**
  _High betweenness centrality (0.227) - this node is a cross-community bridge._
- **Why does `07. Implementation roadmap` connect `07. Implementation roadmap` to `ground.py`, `docs/README.md`, `themes.py`, `ask_interviews`, `Concern pass applied to all 500 interviews (2026-11-09)`, `M4 outcome (done; finished 2026-11-06 22:51 local)`?**
  _High betweenness centrality (0.146) - this node is a cross-community bridge._
- **Why does `Graph RAG demo: Anthropic Interviewer transcripts` connect `Graph RAG demo: Anthropic Interviewer transcripts` to `docs/README.md`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ask_interviews()` (e.g. with `Tool surface` and `Metrics`) actually correct?**
  _`ask_interviews()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI` to the rest of the system?**
  _219 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `extract.py` be split into smaller, more focused modules?**
  _Cohesion score 0.13405797101449277 - nodes in this community are weakly interconnected._
- **Should `mcp_server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11264367816091954 - nodes in this community are weakly interconnected._