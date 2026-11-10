# Graph Report - graph-rag  (2026-11-10)

## Corpus Check
- 94 files · ~55,639 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 696 nodes · 1217 edges · 54 communities (49 shown, 5 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0f96bae2`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ground.py
- mcp_server.py
- decision.py
- 07. Implementation roadmap
- queries.py
- docs/README.md
- prepush_check.py
- pipeline.py
- themes.py
- load.py
- score.py
- 03. Graph schema
- test_themes.py
- 05_make_label_sheets.py
- ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets
- __init__.py
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
- pathlib
- Label confirmation
- ADR-0005: Local LLM selection
- ADR-0011: Retrieval for the transcript corpus
- extract.py
- grounded.py
- test_load.py
- 02. Architecture
- ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus
- ADR-0013: Proceed without human labels for the demo
- interview-graph
- ADR-0008: Decision model (Jev-style) as the question router
- ask_interviews
- 06_score_labels.py
- pre-push
- graph-rag
- test_m3_modules.py
- 04. Query routing and MCP tool surface (Interviewer corpus)
- judge32b.py
- mcp_smoke.py
- 06. Evaluation and roadmap
- confirm_adr0008.py
- Graph RAG demo: Anthropic Interviewer transcripts

## God Nodes (most connected - your core abstractions)
1. `07. Implementation roadmap` - 23 edges
2. `ask_interviews()` - 17 edges
3. `Stage` - 13 edges
4. `answer()` - 12 edges
5. `segments()` - 11 edges
6. `select()` - 11 edges
7. `ADR-0008: Decision model (Jev-style) as the question router` - 11 edges
8. `ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets` - 11 edges
9. `ADR-0010: Extraction pipeline for the transcripts` - 11 edges
10. `score()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Tool surface` --references--> `ask_interviews()`  [INFERRED]
  docs/04-query-and-tools.md → src/graphrag/mcp_server.py
- `Metrics` --references--> `ask_interviews()`  [INFERRED]
  docs/06-evaluation-and-roadmap.md → src/graphrag/mcp_server.py
- `Decisions at a glance` --references--> `ask_interviews()`  [INFERRED]
  docs/README.md → src/graphrag/mcp_server.py
- `What was built` --references--> `ask_interviews()`  [INFERRED]
  README.md → src/graphrag/mcp_server.py
- `Context` --references--> `questions()`  [INFERRED]
  docs/decisions/0008-decision-model-router.md → eval/judge32b.py

## Import Cycles
- None detected.

## Communities (54 total, 5 thin omitted)

### Community 0 - "ground.py"
Cohesion: 0.10
Nodes (21): difflib, Groundedness: what was needed (written 2026-11-07; built and measured below), match(), dedupe(), hygiene_failures(), Names among the most frequent that appear verbatim in the prompt (a sign the…, Drop repeats of the same quote, or of the same (kind, name); keep the first.…, is_grounded() (+13 more)

### Community 1 - "mcp_server.py"
Cohesion: 0.23
Nodes (15): compare_groups(), concept_stats(), driver(), index(), quotes(), MCP server over the interview graph. stdio transport: nothing may print to…, Top 5 interview answers semantically similar to the query, with group, excerpt…, Rank concepts by number of interviews mentioning them. kind: task | ai_use |… (+7 more)

### Community 2 - "decision.py"
Cohesion: 0.07
Nodes (35): 03. Graph schema (Interviewer corpus), Constraints and indexes, Decision-model attributes on `Segment` (properties, not nodes), Model, Nodes, Pipeline, Provenance rule, Relationships (all carry provenance) (+27 more)

### Community 3 - "07. Implementation roadmap"
Cohesion: 0.07
Nodes (26): 07. Implementation roadmap, ADR-0008 confirmation (2026-11-07), Caveats carried forward, Concern pass applied to all 500 interviews (2026-11-09), Critical path and parallel work, Decision points and fallbacks, Filter at verify 0.6 (2026-11-10, owner decision), Finding: the run was interrupted once, 2026-11-06 19:44:41 (+18 more)

### Community 4 - "queries.py"
Cohesion: 0.08
Nodes (33): ndarray, numpy, assign(), main(), new_items(), Merge the looser concern pass (eval/concern_pass.py) into an assembled run…, Map each new cleaned name to an existing canonical name (cos >= threshold) or…, _nq() (+25 more)

### Community 5 - "docs/README.md"
Cohesion: 0.17
Nodes (10): 01. Data analysis: Anthropic Interviewer transcripts, Risks specific to this corpus, Shape, Structure, What a graph can add here, Archived: helpdesk-tickets design, Decision records, How to read the matrices (+2 more)

### Community 6 - "prepush_check.py"
Cohesion: 0.32
Nodes (7): main(), Path, Pre-push check (ADR-0012). Fails when a tracked file could expose the…, shingles(), tracked(), shutil, subprocess

### Community 7 - "pipeline.py"
Cohesion: 0.10
Nodes (27): dotenv, extract(), ids(), jl(), judge(), new_edges(), Second extraction pass for concerns with a looser prompt, on the 10 transcripts…, The 10 recall transcripts first; with CONCERN_SCOPE=all, then every other… (+19 more)

### Community 8 - "themes.py"
Cohesion: 0.13
Nodes (19): argparse, M8 outcome (done 2026-11-07), itertools, math, networkx, fmt(), Score the v3.2 labelling sheets. Usage: uv run --with pandas python…, wilson() (+11 more)

### Community 9 - "load.py"
Cohesion: 0.14
Nodes (20): hashlib, build(), checks(), chunks(), counts(), edge_id(), embed_segments(), main() (+12 more)

### Community 10 - "score.py"
Cohesion: 0.18
Nodes (14): f(), context_numbers(), evaluate(), load(), norm(), nums(), p95(), pct() (+6 more)

### Community 11 - "03. Graph schema"
Cohesion: 0.14
Nodes (12): 01. Data analysis: what a graph can honestly add, Findings that drive the design, Tables, What this means, 03. Graph schema, Constraints and indexes (Cypher), Derived (materialized) edges and properties, Evolution path (+4 more)

### Community 12 - "test_themes.py"
Cohesion: 0.47
Nodes (3): _by(), test_detect_separates_clusters_and_is_deterministic(), test_rare_concepts_excluded()

### Community 13 - "05_make_label_sheets.py"
Cohesion: 0.21
Nodes (9): csv, random, Download the Anthropic/AnthropicInterviewer transcripts into…, Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-…, best_pair(), norm(), pairs(), Build blind labelling sheets under data/labeling/ (git-ignored: they contain… (+1 more)

### Community 14 - "ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets"
Cohesion: 0.17
Nodes (12): ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets, Confirmation, Consequences, Context, Decision drivers, Decision (recommended, pending your confirmation), Impact on the existing design, Options (+4 more)

### Community 15 - "__init__.py"
Cohesion: 0.17
Nodes (6): collections, Consistency checks on the model-judged label files (data/eval/judge/,…, Re-measure recall on the 10 transcripts of eval/judge32b.py recall, against the…, Routing accuracy on questions written by a different model (qwen2.5:32b) from…, json, Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels).…

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
Cohesion: 0.31
Nodes (8): chat(), config_A(), config_B(), config_C(), final_answer(), M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble…, Same behaviour as the typed MCP profile., run_tool()

### Community 20 - "test_router.py"
Cohesion: 0.31
Nodes (6): fake(), FakeIndex, test_concept_stats_low_enum_confidence_clarifies(), test_low_confidence_clarifies_and_runs_nothing(), test_out_of_scope_calls_no_query(), test_weak_concept_match_clarifies()

### Community 21 - "sys"
Cohesion: 0.15
Nodes (9): pandas, pexpect, re, Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration,…, Drive a live ollmcp session (qwen3:8b-16k, routed profile, mcp.json) through a…, M2: rerun extraction v3 on the same 20 transcripts as the spike. Usage:…, statistics, sys (+1 more)

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

### Community 29 - "pathlib"
Cohesion: 0.16
Nodes (9): Gate 2 proxy: do the top-5 vector hits for 10 queries contain answers that…, quality(), Re-measure groundedness with answer generation, through the grounded path…, score(), neo4j, pathlib, fake_extract(), test_stages_resume_and_assemble() (+1 more)

### Community 30 - "Label confirmation"
Cohesion: 0.25
Nodes (8): All 40, Dev half (tuning allowed), Held-out half, Label confirmation, Per-route latency (median s), Router abstention by threshold (All 40, route confidence only), Router abstention by threshold (Dev half (tuning allowed), route confidence only), Router abstention by threshold (Held-out half, route confidence only)

### Community 31 - "ADR-0005: Local LLM selection"
Cohesion: 0.25
Nodes (8): ADR-0005: Local LLM selection, Confirmation, Consequences, Context, Decision, Revisit when, Roles, Weighted decision matrix: orchestrator

### Community 32 - "ADR-0011: Retrieval for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0011: Retrieval for the transcript corpus, Confirmation, Consequences, Context, Decision, Options, Revisit when, Weighted decision matrix

### Community 33 - "extract.py"
Cohesion: 0.22
Nodes (12): Graph-wide precision check of the concern edges added by the all-500 concern…, ollama, build_prompt(), extract(), Client, Extraction v3: one list of typed items per transcript, each with status,…, parse_turns(), Split a transcript into turns and question/answer segments. (+4 more)

### Community 35 - "grounded.py"
Cohesion: 0.08
Nodes (31): Groundedness: built and measured (2026-11-07), 09. Completion status (2026-11-10, updated after the owner's decisions and Test 1), Decided by the owner (2026-11-10), Done, Housekeeping, Open: needs your decision (superseded by the section above; kept for the record), Open: tests not yet run (after Test 1), Targets in 06 against the evidence (+23 more)

### Community 36 - "test_load.py"
Cohesion: 0.38
Nodes (4): E(), _run(), test_build_keeps_grounded_only(), test_embed_cache_reused()

### Community 37 - "02. Architecture"
Cohesion: 0.33
Nodes (6): 02. Architecture, Components, Failure handling, Resource budget, Routes (decided by `nimble`, see [04](04-query-and-tools.md)), Two flows

### Community 38 - "ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus"
Cohesion: 0.29
Nodes (7): ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus, Confirmation, Consequences, Context, Decision, PII pass record (2026-11-07, before the first public commit), Revisit when

### Community 39 - "ADR-0013: Proceed without human labels for the demo"
Cohesion: 0.33
Nodes (6): ADR-0013: Proceed without human labels for the demo, Confirmation, Consequences, Context, Decision, Revisit when

### Community 40 - "interview-graph"
Cohesion: 0.33
Nodes (5): NEO4J_URI, NEO4J_USER, PYTHONPATH, .venv/bin/python, interview-graph

### Community 41 - "ADR-0008: Decision model (Jev-style) as the question router"
Cohesion: 0.18
Nodes (11): ADR-0008: Decision model (Jev-style) as the question router, Confirmation, Confirmation result (2026-11-07), Consequences, Context, Decision, Decision drivers, M3 note (2026-11-06) (+3 more)

### Community 42 - "ask_interviews"
Cohesion: 0.22
Nodes (11): Milestones, 08. Evaluation results (M7), All 40, final graph, Fix attempt and re-test (2026-11-10), Groundedness on the final graph (60 questions, `eval/grounded_eval.py`, router v3), Live `ollmcp` session on the final graph (2026-11-10), Per-route end-to-end latency (median s), final graph, Re-run on the final graph (2026-11-10) (+3 more)

### Community 43 - "06_score_labels.py"
Cohesion: 0.67
Nodes (3): fmt(), Score filled-in labelling sheets. Usage: python spike/06_score_labels.py…, wilson()

### Community 48 - "04. Query routing and MCP tool surface (Interviewer corpus)"
Cohesion: 0.25
Nodes (8): 04. Query routing and MCP tool surface (Interviewer corpus), Answer rules (system prompt sketch), Example Cypher (parameterised, read-only), Global questions, ollmcp wiring, Optional: gated text-to-Cypher, Routes, Tool surface

### Community 49 - "judge32b.py"
Cohesion: 0.50
Nodes (7): ask(), done_ids(), load_records(), precision(), questions(), Independent checks by a larger model (qwen2.5:32b, run alone), so the 8B…, recall()

### Community 50 - "mcp_smoke.py"
Cohesion: 0.33
Nodes (4): asyncio, fastmcp, fastmcp_client_transports, Start the MCP server over stdio and call it like a client would. Usage:…

### Community 51 - "06. Evaluation and roadmap"
Cohesion: 0.33
Nodes (6): 06. Evaluation and roadmap, Labelling plan (as run: model labels, confirmed by the owner; see [ADR-0013](decisions/0013-waive-human-labels.md) and [09](09-completion-status.md)), Metrics, Phases (all done; see [07](07-implementation-roadmap.md) for dates and outcomes), Risks, The honest problem

### Community 52 - "confirm_adr0008.py"
Cohesion: 0.40
Nodes (3): b_row(), ADR-0008 confirmation on questions written after the router changes were chosen…, timed_decide()

### Community 53 - "Graph RAG demo: Anthropic Interviewer transcripts"
Cohesion: 0.40
Nodes (5): Decisions at a glance, Graph RAG demo: Anthropic Interviewer transcripts, Read in this order, What I need from you, What the spike found (20 transcripts, one machine)

## Knowledge Gaps
- **214 isolated node(s):** `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI`, `NEO4J_USER`, `graph-rag` (+209 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 359 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ask_interviews()` connect `ask_interviews` to `mcp_server.py`, `grounded.py`, `07. Implementation roadmap`, `04. Query routing and MCP tool surface (Interviewer corpus)`, `06. Evaluation and roadmap`, `Graph RAG demo: Anthropic Interviewer transcripts`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Why does `07. Implementation roadmap` connect `07. Implementation roadmap` to `ground.py`, `grounded.py`, `docs/README.md`, `themes.py`, `ask_interviews`?**
  _High betweenness centrality (0.147) - this node is a cross-community bridge._
- **Why does `Graph RAG demo: Anthropic Interviewer transcripts` connect `Graph RAG demo: Anthropic Interviewer transcripts` to `docs/README.md`?**
  _High betweenness centrality (0.089) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `ask_interviews()` (e.g. with `Tool surface` and `Metrics`) actually correct?**
  _`ask_interviews()` has 10 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI` to the rest of the system?**
  _214 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ground.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09846153846153846 - nodes in this community are weakly interconnected._
- **Should `decision.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06685633001422475 - nodes in this community are weakly interconnected._