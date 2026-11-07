# Graph Report - graph-rag  (2026-11-07)

## Corpus Check
- 86 files · ~46,842 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 637 nodes · 1083 edges · 47 communities (44 shown, 3 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0283b433`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- extract.py
- mcp_server.py
- decision.py
- 07. Implementation roadmap
- queries.py
- docs/README.md
- run_eval.py
- pipeline.py
- themes.py
- pathlib
- score.py
- 03. Graph schema
- score_labels_v3.py
- json
- ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets
- load.py
- 04. Query routing and MCP tool surface
- ADR-NNNN: Title (the decision, as a short noun phrase)
- ADR-0010: Extraction pipeline for the transcripts
- grounded.py
- test_router.py
- calibrate_verify.py
- ADR-0001: Graph database
- ADR-0002: How the graph is built
- ADR-0003: Vector retrieval and graph expansion
- ADR-0004: Query interface the LLM uses
- ADR-0006: Deployment topology
- ADR-0007: Privacy and access control
- Spike 01: can local models build the graph from the transcripts?
- __init__.py
- 08. Evaluation results (M7)
- ADR-0005: Local LLM selection
- ADR-0011: Retrieval for the transcript corpus
- prepush_check.py
- Labelling guide (v3.2 sheets, about 2 hours)
- test_load.py
- 02. Architecture
- ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus
- ADR-0013: Proceed without human labels for the demo
- interview-graph
- test_themes.py
- 01. Data analysis: Anthropic Interviewer transcripts
- 05_make_label_sheets.py
- pre-push
- graph-rag
- confirm_adr0008.py

## God Nodes (most connected - your core abstractions)
1. `07. Implementation roadmap` - 20 edges
2. `ask_interviews()` - 14 edges
3. `Stage` - 12 edges
4. `segments()` - 11 edges
5. `ADR-0008: Decision model (Jev-style) as the question router` - 11 edges
6. `ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets` - 11 edges
7. `ADR-0010: Extraction pipeline for the transcripts` - 10 edges
8. `decide()` - 9 edges
9. `score()` - 9 edges
10. `answer()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Milestones` --references--> `ask_interviews()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/mcp_server.py
- `Nodes` --references--> `answer()`  [INFERRED]
  docs/03-graph-schema.md → src/graphrag/router.py
- `Decision-model attributes on `Segment` (properties, not nodes)` --references--> `attributes()`  [INFERRED]
  docs/03-graph-schema.md → src/graphrag/attributes.py
- `Throughput reality (measured, one machine)` --references--> `attributes()`  [INFERRED]
  docs/05-components.md → src/graphrag/attributes.py
- `Groundedness: what was needed (written 2026-11-07; built and measured below)` --references--> `is_grounded()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/ground.py

## Import Cycles
- None detected.

## Communities (47 total, 3 thin omitted)

### Community 0 - "extract.py"
Cohesion: 0.06
Nodes (49): difflib, Groundedness: what was needed (written 2026-11-07; built and measured below), ADR-0008: Decision model (Jev-style) as the question router, Confirmation, Confirmation result (2026-11-07), Consequences, Context, Decision (+41 more)

### Community 1 - "mcp_server.py"
Cohesion: 0.06
Nodes (42): 04. Query routing and MCP tool surface (Interviewer corpus), Answer rules (system prompt sketch), Example Cypher (parameterised, read-only), Global questions, ollmcp wiring, Optional: gated text-to-Cypher, Routes, Tool surface (+34 more)

### Community 2 - "decision.py"
Cohesion: 0.09
Nodes (26): 03. Graph schema (Interviewer corpus), Constraints and indexes, Decision-model attributes on `Segment` (properties, not nodes), Model, Nodes, Pipeline, Provenance rule, Relationships (all carry provenance) (+18 more)

### Community 3 - "07. Implementation roadmap"
Cohesion: 0.09
Nodes (21): 07. Implementation roadmap, ADR-0008 confirmation (2026-11-07), Caveats carried forward, Critical path and parallel work, Decision points and fallbacks, Finding: the run was interrupted once, 2026-11-06 19:44:41, First three actions, Gate 2: retrieval check (proxy, no human labels) (+13 more)

### Community 4 - "queries.py"
Cohesion: 0.08
Nodes (26): ndarray, numpy, canonicalise(), clean(), cluster(), embed(), Client, Merge near-duplicate extracted names into canonical concepts using embeddings… (+18 more)

### Community 5 - "docs/README.md"
Cohesion: 0.23
Nodes (5): Archived: helpdesk-tickets design, Decision records, How to read the matrices, Index, Open questions for you

### Community 6 - "run_eval.py"
Cohesion: 0.31
Nodes (8): chat(), config_A(), config_B(), config_C(), final_answer(), M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble…, Same behaviour as the typed MCP profile., run_tool()

### Community 7 - "pipeline.py"
Cohesion: 0.13
Nodes (18): quality(), Re-measure groundedness with answer generation, through the grounded path…, score(), Path, Resumable stage bookkeeping: each stage appends one JSON line per finished key;…, Stage, assemble(), kept_items() (+10 more)

### Community 8 - "themes.py"
Cohesion: 0.21
Nodes (15): M8 outcome (done 2026-11-07), itertools, networkx, unload(), build_graph(), detect(), fetch(), main() (+7 more)

### Community 9 - "pathlib"
Cohesion: 0.17
Nodes (8): asyncio, fastmcp, fastmcp_client_transports, pathlib, Start the MCP server over stdio and call it like a client would. Usage:…, fake_extract(), test_stages_resume_and_assemble(), ext()

### Community 10 - "score.py"
Cohesion: 0.18
Nodes (14): f(), context_numbers(), evaluate(), load(), norm(), nums(), p95(), pct() (+6 more)

### Community 11 - "03. Graph schema"
Cohesion: 0.14
Nodes (12): 01. Data analysis: what a graph can honestly add, Findings that drive the design, Tables, What this means, 03. Graph schema, Constraints and indexes (Cypher), Derived (materialized) edges and properties, Evolution path (+4 more)

### Community 12 - "score_labels_v3.py"
Cohesion: 0.24
Nodes (7): math, fmt(), Score the v3.2 labelling sheets. Usage: uv run --with pandas python…, wilson(), fmt(), Score filled-in labelling sheets. Usage: python spike/06_score_labels.py…, wilson()

### Community 13 - "json"
Cohesion: 0.19
Nodes (9): json, ollama, pandas, random, re, requests, Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-…, M2: rerun extraction v3 on the same 20 transcripts as the spike. Usage:… (+1 more)

### Community 14 - "ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets"
Cohesion: 0.17
Nodes (12): ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets, Confirmation, Consequences, Context, Decision drivers, Decision (recommended, pending your confirmation), Impact on the existing design, Options (+4 more)

### Community 15 - "load.py"
Cohesion: 0.11
Nodes (24): argparse, dotenv, hashlib, os, Settings from environment / .env. No secrets in code., build(), checks(), chunks() (+16 more)

### Community 16 - "04. Query routing and MCP tool surface"
Cohesion: 0.20
Nodes (9): 04. Query routing and MCP tool surface, Design rule from the existing project, Example expansion query (used by `find_similar_problems`), ollmcp wiring, Optional: gated text-to-Cypher (phase 3, off by default), Question types and routes, Response shaping for a small model, System prompt additions (sketch) (+1 more)

### Community 17 - "ADR-NNNN: Title (the decision, as a short noun phrase)"
Cohesion: 0.20
Nodes (9): ADR-NNNN: Title (the decision, as a short noun phrase), Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 18 - "ADR-0010: Extraction pipeline for the transcripts"
Cohesion: 0.20
Nodes (10): ADR-0010: Extraction pipeline for the transcripts, Confirmation, Consequences, Context, Decision, Decision drivers, M3 amendments (2026-11-06), Options (+2 more)

### Community 19 - "grounded.py"
Cohesion: 0.15
Nodes (17): Groundedness: built and measured (2026-11-07), allowed_numbers(), grounded_answer(), items(), numbers(), quotes_in(), Grounded answers: the server renders facts as text, a model may only add…, Route, render, frame with the LLM, validate, fall back to the rendered facts on… (+9 more)

### Community 20 - "test_router.py"
Cohesion: 0.31
Nodes (6): fake(), FakeIndex, test_concept_stats_low_enum_confidence_clarifies(), test_low_confidence_clarifies_and_runs_nothing(), test_out_of_scope_calls_no_query(), test_weak_concept_match_clarifies()

### Community 21 - "calibrate_verify.py"
Cohesion: 0.20
Nodes (7): csv, Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration,…, match(), Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels).…, Download the Anthropic/AnthropicInterviewer transcripts into…, statistics, urllib_request

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

### Community 29 - "__init__.py"
Cohesion: 0.20
Nodes (4): collections, Gate 2 proxy: do the top-5 vector hits for 10 queries contain answers that…, Routing accuracy on questions written by a different model (qwen2.5:32b) from…, neo4j

### Community 30 - "08. Evaluation results (M7)"
Cohesion: 0.25
Nodes (8): 08. Evaluation results (M7), All 40, Dev half (tuning allowed), Held-out half, Per-route latency (median s), Router abstention by threshold (All 40, route confidence only), Router abstention by threshold (Dev half (tuning allowed), route confidence only), Router abstention by threshold (Held-out half, route confidence only)

### Community 31 - "ADR-0005: Local LLM selection"
Cohesion: 0.25
Nodes (8): ADR-0005: Local LLM selection, Confirmation, Consequences, Context, Decision, Revisit when, Roles, Weighted decision matrix: orchestrator

### Community 32 - "ADR-0011: Retrieval for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0011: Retrieval for the transcript corpus, Confirmation, Consequences, Context, Decision, Options, Revisit when, Weighted decision matrix

### Community 33 - "prepush_check.py"
Cohesion: 0.32
Nodes (7): main(), Path, Pre-push check (ADR-0012). Fails when a tracked file could expose the…, shingles(), tracked(), shutil, subprocess

### Community 35 - "Labelling guide (v3.2 sheets, about 2 hours)"
Cohesion: 0.29
Nodes (7): Files, How to fill in the CSV, Labelling guide (v3.2 sheets, about 2 hours), Reading the result, Score it, Sheet 1: edges, Sheet 2: attitude (30 rows)

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

### Community 41 - "test_themes.py"
Cohesion: 0.47
Nodes (3): _by(), test_detect_separates_clusters_and_is_deterministic(), test_rare_concepts_excluded()

### Community 42 - "01. Data analysis: Anthropic Interviewer transcripts"
Cohesion: 0.40
Nodes (5): 01. Data analysis: Anthropic Interviewer transcripts, Risks specific to this corpus, Shape, Structure, What a graph can add here

### Community 43 - "05_make_label_sheets.py"
Cohesion: 0.60
Nodes (4): best_pair(), norm(), pairs(), Build blind labelling sheets under data/labeling/ (git-ignored: they contain…

### Community 46 - "confirm_adr0008.py"
Cohesion: 0.40
Nodes (3): b_row(), ADR-0008 confirmation on questions written after the router changes were chosen…, timed_decide()

## Knowledge Gaps
- **203 isolated node(s):** `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI`, `NEO4J_USER`, `graph-rag` (+198 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 334 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ask_interviews()` connect `mcp_server.py` to `07. Implementation roadmap`, `grounded.py`?**
  _High betweenness centrality (0.221) - this node is a cross-community bridge._
- **Why does `07. Implementation roadmap` connect `07. Implementation roadmap` to `extract.py`, `themes.py`, `grounded.py`, `docs/README.md`?**
  _High betweenness centrality (0.169) - this node is a cross-community bridge._
- **Why does `Graph RAG demo: Anthropic Interviewer transcripts` connect `mcp_server.py` to `docs/README.md`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ask_interviews()` (e.g. with `Tool surface` and `Metrics`) actually correct?**
  _`ask_interviews()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI` to the rest of the system?**
  _203 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `extract.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05764411027568922 - nodes in this community are weakly interconnected._
- **Should `mcp_server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.06423034330011074 - nodes in this community are weakly interconnected._