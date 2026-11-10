# Graph Report - graph-rag  (2026-11-10)

## Corpus Check
- 93 files · ~54,408 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 690 nodes · 1203 edges · 47 communities (43 shown, 4 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 40 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `64db036c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ground.py
- mcp_server.py
- router.py
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
- confirm_adr0008.py
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
- judge32b.py
- 09. Completion status (2026-11-10, updated after the owner's decisions and Test 1)
- sys
- pre-push
- graph-rag

## God Nodes (most connected - your core abstractions)
1. `07. Implementation roadmap` - 23 edges
2. `ask_interviews()` - 15 edges
3. `Stage` - 13 edges
4. `segments()` - 11 edges
5. `select()` - 11 edges
6. `ADR-0008: Decision model (Jev-style) as the question router` - 11 edges
7. `ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets` - 11 edges
8. `ADR-0010: Extraction pipeline for the transcripts` - 11 edges
9. `score()` - 10 edges
10. `decide()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Milestones` --references--> `ask_interviews()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/mcp_server.py
- `What changed against the first run (all 40)` --references--> `ask_interviews()`  [INFERRED]
  docs/08-evaluation-results.md → src/graphrag/mcp_server.py
- `Decision-model attributes on `Segment` (properties, not nodes)` --references--> `attributes()`  [INFERRED]
  docs/03-graph-schema.md → src/graphrag/attributes.py
- `Throughput reality (measured, one machine)` --references--> `attributes()`  [INFERRED]
  docs/05-components.md → src/graphrag/attributes.py
- `Groundedness: what was needed (written 2026-11-07; built and measured below)` --references--> `is_grounded()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/ground.py

## Import Cycles
- None detected.

## Communities (47 total, 4 thin omitted)

### Community 0 - "ground.py"
Cohesion: 0.10
Nodes (21): difflib, Groundedness: what was needed (written 2026-11-07; built and measured below), match(), dedupe(), hygiene_failures(), Names among the most frequent that appear verbatim in the prompt (a sign the…, Drop repeats of the same quote, or of the same (kind, name); keep the first.…, is_grounded() (+13 more)

### Community 1 - "mcp_server.py"
Cohesion: 0.05
Nodes (46): asyncio, 04. Query routing and MCP tool surface (Interviewer corpus), Answer rules (system prompt sketch), Example Cypher (parameterised, read-only), Global questions, ollmcp wiring, Optional: gated text-to-Cypher, Routes (+38 more)

### Community 2 - "router.py"
Cohesion: 0.06
Nodes (41): 03. Graph schema (Interviewer corpus), Constraints and indexes, Decision-model attributes on `Segment` (properties, not nodes), Model, Nodes, Pipeline, Provenance rule, Relationships (all carry provenance) (+33 more)

### Community 3 - "07. Implementation roadmap"
Cohesion: 0.07
Nodes (27): 07. Implementation roadmap, ADR-0008 confirmation (2026-11-07), Caveats carried forward, Concern pass applied to all 500 interviews (2026-11-09), Critical path and parallel work, Decision points and fallbacks, Filter at verify 0.6 (2026-11-10, owner decision), Finding: the run was interrupted once, 2026-11-06 19:44:41 (+19 more)

### Community 4 - "queries.py"
Cohesion: 0.07
Nodes (30): hashlib, ndarray, numpy, canonicalise(), clean(), cluster(), embed(), Client (+22 more)

### Community 5 - "docs/README.md"
Cohesion: 0.17
Nodes (10): 01. Data analysis: Anthropic Interviewer transcripts, Risks specific to this corpus, Shape, Structure, What a graph can add here, Archived: helpdesk-tickets design, Decision records, How to read the matrices (+2 more)

### Community 6 - "prepush_check.py"
Cohesion: 0.32
Nodes (7): main(), Path, Pre-push check (ADR-0012). Fails when a tracked file could expose the…, shingles(), tracked(), shutil, subprocess

### Community 7 - "pipeline.py"
Cohesion: 0.08
Nodes (34): argparse, dotenv, extract(), ids(), jl(), judge(), new_edges(), Second extraction pass for concerns with a looser prompt, on the 10 transcripts… (+26 more)

### Community 8 - "themes.py"
Cohesion: 0.14
Nodes (18): M8 outcome (done 2026-11-07), itertools, math, networkx, fmt(), Score the v3.2 labelling sheets. Usage: uv run --with pandas python…, wilson(), build_graph() (+10 more)

### Community 9 - "load.py"
Cohesion: 0.15
Nodes (19): build(), checks(), chunks(), counts(), edge_id(), embed_segments(), main(), M5: load an assembled run (graph_input.jsonl) into Neo4j. Idempotent (MERGE… (+11 more)

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
Cohesion: 0.28
Nodes (7): csv, Download the Anthropic/AnthropicInterviewer transcripts into…, best_pair(), norm(), pairs(), Build blind labelling sheets under data/labeling/ (git-ignored: they contain…, urllib_request

### Community 14 - "ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets"
Cohesion: 0.17
Nodes (12): ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets, Confirmation, Consequences, Context, Decision drivers, Decision (recommended, pending your confirmation), Impact on the existing design, Options (+4 more)

### Community 15 - "__init__.py"
Cohesion: 0.16
Nodes (7): collections, Consistency checks on the model-judged label files (data/eval/judge/,…, Re-measure recall on the 10 transcripts of eval/judge32b.py recall, against the…, Routing accuracy on questions written by a different model (qwen2.5:32b) from…, json, Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels).…, Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-…

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

### Community 21 - "confirm_adr0008.py"
Cohesion: 0.18
Nodes (6): b_row(), ADR-0008 confirmation on questions written after the router changes were chosen…, timed_decide(), Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration,…, statistics, time

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
Cohesion: 0.14
Nodes (14): 08. Evaluation results (M7), All 40, All 40, final graph, Dev half (tuning allowed), Groundedness on the final graph (60 questions, `eval/grounded_eval.py`, router v3), Held-out half, Label confirmation, Per-route end-to-end latency (median s), final graph (+6 more)

### Community 31 - "ADR-0005: Local LLM selection"
Cohesion: 0.25
Nodes (8): ADR-0005: Local LLM selection, Confirmation, Consequences, Context, Decision, Revisit when, Roles, Weighted decision matrix: orchestrator

### Community 32 - "ADR-0011: Retrieval for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0011: Retrieval for the transcript corpus, Confirmation, Consequences, Context, Decision, Options, Revisit when, Weighted decision matrix

### Community 33 - "extract.py"
Cohesion: 0.21
Nodes (13): Graph-wide precision check of the concern edges added by the all-500 concern…, ollama, re, build_prompt(), extract(), Client, Extraction v3: one list of typed items per transcript, each with status,…, parse_turns() (+5 more)

### Community 35 - "grounded.py"
Cohesion: 0.22
Nodes (12): Groundedness: built and measured (2026-11-07), cov(), allowed_numbers(), grounded_answer(), items(), numbers(), quotes_in(), Grounded answers: the server renders facts as text, a model may only add… (+4 more)

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

### Community 41 - "judge32b.py"
Cohesion: 0.15
Nodes (18): ADR-0008: Decision model (Jev-style) as the question router, Confirmation, Confirmation result (2026-11-07), Consequences, Context, Decision, Decision drivers, M3 note (2026-11-06) (+10 more)

### Community 42 - "09. Completion status (2026-11-10, updated after the owner's decisions and Test 1)"
Cohesion: 0.29
Nodes (7): 09. Completion status (2026-11-10, updated after the owner's decisions and Test 1), Decided by the owner (2026-11-10), Done, Housekeeping, Open: needs your decision (superseded by the section above; kept for the record), Open: tests not yet run (after Test 1), Targets in 06 against the evidence

### Community 43 - "sys"
Cohesion: 0.20
Nodes (7): pandas, random, M2: rerun extraction v3 on the same 20 transcripts as the spike. Usage:…, fmt(), Score filled-in labelling sheets. Usage: python spike/06_score_labels.py…, wilson(), sys

## Knowledge Gaps
- **216 isolated node(s):** `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI`, `NEO4J_USER`, `graph-rag` (+211 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 358 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ask_interviews()` connect `mcp_server.py` to `07. Implementation roadmap`, `router.py`, `grounded.py`, `Label confirmation`?**
  _High betweenness centrality (0.228) - this node is a cross-community bridge._
- **Why does `07. Implementation roadmap` connect `07. Implementation roadmap` to `ground.py`, `themes.py`, `grounded.py`, `docs/README.md`?**
  _High betweenness centrality (0.154) - this node is a cross-community bridge._
- **Why does `Graph RAG demo: Anthropic Interviewer transcripts` connect `mcp_server.py` to `docs/README.md`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `ask_interviews()` (e.g. with `Tool surface` and `Metrics`) actually correct?**
  _`ask_interviews()` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI` to the rest of the system?**
  _216 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ground.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09846153846153846 - nodes in this community are weakly interconnected._
- **Should `mcp_server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05442176870748299 - nodes in this community are weakly interconnected._