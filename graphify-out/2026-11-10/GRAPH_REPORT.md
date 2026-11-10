# Graph Report - graph-rag  (2026-11-10)

## Corpus Check
- 91 files · ~51,983 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 2, .example 1, .lock 1)

## Summary
- 671 nodes · 1176 edges · 44 communities (40 shown, 4 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `26827a03`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- load.py
- mcp_server.py
- router.py
- 07. Implementation roadmap
- queries.py
- docs/README.md
- concern_merge.py
- pipeline.py
- themes.py
- pathlib
- score.py
- 03. Graph schema
- test_themes.py
- 05_make_label_sheets.py
- ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets
- check_labels.py
- 04. Query routing and MCP tool surface
- ADR-NNNN: Title (the decision, as a short noun phrase)
- ADR-0010: Extraction pipeline for the transcripts
- run_eval.py
- test_router.py
- collections
- ADR-0001: Graph database
- ADR-0002: How the graph is built
- ADR-0003: Vector retrieval and graph expansion
- ADR-0004: Query interface the LLM uses
- ADR-0006: Deployment topology
- ADR-0007: Privacy and access control
- Spike 01: can local models build the graph from the transcripts?
- __init__.py
- Label confirmation
- ADR-0005: Local LLM selection
- ADR-0011: Retrieval for the transcript corpus
- test_load.py
- 02. Architecture
- ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus
- ADR-0013: Proceed without human labels for the demo
- interview-graph
- judge32b.py
- json
- pre-push
- graph-rag
- sys

## God Nodes (most connected - your core abstractions)
1. `07. Implementation roadmap` - 23 edges
2. `ask_interviews()` - 14 edges
3. `Stage` - 13 edges
4. `segments()` - 11 edges
5. `select()` - 11 edges
6. `ADR-0008: Decision model (Jev-style) as the question router` - 11 edges
7. `ADR-0009: Corpus: Anthropic Interviewer transcripts vs helpdesk tickets` - 11 edges
8. `score()` - 10 edges
9. `ADR-0010: Extraction pipeline for the transcripts` - 10 edges
10. `decide()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Milestones` --references--> `ask_interviews()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/mcp_server.py
- `Decision-model attributes on `Segment` (properties, not nodes)` --references--> `attributes()`  [INFERRED]
  docs/03-graph-schema.md → src/graphrag/attributes.py
- `Throughput reality (measured, one machine)` --references--> `attributes()`  [INFERRED]
  docs/05-components.md → src/graphrag/attributes.py
- `Groundedness: what was needed (written 2026-11-07; built and measured below)` --references--> `is_grounded()`  [INFERRED]
  docs/07-implementation-roadmap.md → src/graphrag/ground.py
- `Tool surface` --references--> `ask_interviews()`  [INFERRED]
  docs/04-query-and-tools.md → src/graphrag/mcp_server.py

## Import Cycles
- None detected.

## Communities (44 total, 4 thin omitted)

### Community 0 - "load.py"
Cohesion: 0.07
Nodes (43): difflib, Groundedness: what was needed (written 2026-11-07; built and measured below), build_prompt(), dedupe(), extract(), hygiene_failures(), Client, Extraction v3: one list of typed items per transcript, each with status,… (+35 more)

### Community 1 - "mcp_server.py"
Cohesion: 0.05
Nodes (54): 04. Query routing and MCP tool surface (Interviewer corpus), Answer rules (system prompt sketch), Example Cypher (parameterised, read-only), Global questions, ollmcp wiring, Optional: gated text-to-Cypher, Routes, Tool surface (+46 more)

### Community 2 - "router.py"
Cohesion: 0.06
Nodes (40): 03. Graph schema (Interviewer corpus), Constraints and indexes, Decision-model attributes on `Segment` (properties, not nodes), Model, Nodes, Pipeline, Provenance rule, Relationships (all carry provenance) (+32 more)

### Community 3 - "07. Implementation roadmap"
Cohesion: 0.07
Nodes (26): 07. Implementation roadmap, ADR-0008 confirmation (2026-11-07), Caveats carried forward, Concern pass applied to all 500 interviews (2026-11-09), Critical path and parallel work, Decision points and fallbacks, Filter at verify 0.6 (2026-11-10, owner decision), Finding: the run was interrupted once, 2026-11-06 19:44:41 (+18 more)

### Community 4 - "queries.py"
Cohesion: 0.08
Nodes (33): dotenv, hashlib, ndarray, Settings from environment / .env. No secrets in code., canonicalise(), clean(), cluster(), embed() (+25 more)

### Community 5 - "docs/README.md"
Cohesion: 0.18
Nodes (10): 01. Data analysis: Anthropic Interviewer transcripts, Risks specific to this corpus, Shape, Structure, What a graph can add here, Archived: helpdesk-tickets design, Decision records, How to read the matrices (+2 more)

### Community 6 - "concern_merge.py"
Cohesion: 0.08
Nodes (18): numpy, main(), Path, Pre-push check (ADR-0012). Fails when a tracked file could expose the…, shingles(), tracked(), shutil, assign() (+10 more)

### Community 7 - "pipeline.py"
Cohesion: 0.12
Nodes (25): extract(), ids(), jl(), judge(), new_edges(), Second extraction pass for concerns with a looser prompt, on the 10 transcripts…, The 10 recall transcripts first; with CONCERN_SCOPE=all, then every other…, Kept new concern edges whose quote is not already the quote of an original kept… (+17 more)

### Community 8 - "themes.py"
Cohesion: 0.11
Nodes (22): argparse, M8 outcome (done 2026-11-07), itertools, math, networkx, fmt(), Score the v3.2 labelling sheets. Usage: uv run --with pandas python…, wilson() (+14 more)

### Community 9 - "pathlib"
Cohesion: 0.17
Nodes (8): asyncio, fastmcp, fastmcp_client_transports, pathlib, Start the MCP server over stdio and call it like a client would. Usage:…, fake_extract(), test_stages_resume_and_assemble(), ext()

### Community 10 - "score.py"
Cohesion: 0.22
Nodes (12): context_numbers(), evaluate(), load(), norm(), nums(), p95(), pct(), quotes_in() (+4 more)

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

### Community 16 - "04. Query routing and MCP tool surface"
Cohesion: 0.20
Nodes (9): 04. Query routing and MCP tool surface, Design rule from the existing project, Example expansion query (used by `find_similar_problems`), ollmcp wiring, Optional: gated text-to-Cypher (phase 3, off by default), Question types and routes, Response shaping for a small model, System prompt additions (sketch) (+1 more)

### Community 17 - "ADR-NNNN: Title (the decision, as a short noun phrase)"
Cohesion: 0.20
Nodes (9): ADR-NNNN: Title (the decision, as a short noun phrase), Confirmation, Consequences, Context, Decision, Decision drivers, Options, Revisit when (+1 more)

### Community 18 - "ADR-0010: Extraction pipeline for the transcripts"
Cohesion: 0.20
Nodes (10): ADR-0010: Extraction pipeline for the transcripts, Confirmation, Consequences, Context, Decision, Decision drivers, M3 amendments (2026-11-06), Options (+2 more)

### Community 19 - "run_eval.py"
Cohesion: 0.31
Nodes (8): chat(), config_A(), config_B(), config_C(), final_answer(), M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble…, Same behaviour as the typed MCP profile., run_tool()

### Community 20 - "test_router.py"
Cohesion: 0.31
Nodes (6): fake(), FakeIndex, test_concept_stats_low_enum_confidence_clarifies(), test_low_confidence_clarifies_and_runs_nothing(), test_out_of_scope_calls_no_query(), test_weak_concept_match_clarifies()

### Community 21 - "collections"
Cohesion: 0.19
Nodes (7): collections, csv, requests, Calibrate the verify step against the LLM-labelled v3.2 sheet (a calibration,…, match(), Compare v3 against the labelled v2 edges (data/labeling_claude, LLM labels).…, statistics

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
Cohesion: 0.16
Nodes (6): Gate 2 proxy: do the top-5 vector hits for 10 queries contain answers that…, quality(), Re-measure groundedness with answer generation, through the grounded path…, score(), Routing accuracy on questions written by a different model (qwen2.5:32b) from…, neo4j

### Community 30 - "Label confirmation"
Cohesion: 0.22
Nodes (9): 08. Evaluation results (M7), All 40, Dev half (tuning allowed), Held-out half, Label confirmation, Per-route latency (median s), Router abstention by threshold (All 40, route confidence only), Router abstention by threshold (Dev half (tuning allowed), route confidence only) (+1 more)

### Community 31 - "ADR-0005: Local LLM selection"
Cohesion: 0.25
Nodes (8): ADR-0005: Local LLM selection, Confirmation, Consequences, Context, Decision, Revisit when, Roles, Weighted decision matrix: orchestrator

### Community 32 - "ADR-0011: Retrieval for the transcript corpus"
Cohesion: 0.25
Nodes (8): ADR-0011: Retrieval for the transcript corpus, Confirmation, Consequences, Context, Decision, Options, Revisit when, Weighted decision matrix

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

### Community 43 - "json"
Cohesion: 0.21
Nodes (9): Graph-wide precision check of the concern edges added by the all-500 concern…, json, ollama, os, pandas, random, re, Blind labelling sheet from extraction v3.2 output -> data/labeling_v3/ (git-… (+1 more)

### Community 46 - "sys"
Cohesion: 0.20
Nodes (8): b_row(), ADR-0008 confirmation on questions written after the router changes were chosen…, timed_decide(), f(), main(), Download the Anthropic/AnthropicInterviewer transcripts into…, sys, urllib_request

## Knowledge Gaps
- **205 isolated node(s):** `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI`, `NEO4J_USER`, `graph-rag` (+200 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 344 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ask_interviews()` connect `mcp_server.py` to `router.py`, `07. Implementation roadmap`?**
  _High betweenness centrality (0.210) - this node is a cross-community bridge._
- **Why does `07. Implementation roadmap` connect `07. Implementation roadmap` to `load.py`, `mcp_server.py`, `docs/README.md`, `themes.py`?**
  _High betweenness centrality (0.163) - this node is a cross-community bridge._
- **Why does `Graph RAG demo: Anthropic Interviewer transcripts` connect `mcp_server.py` to `docs/README.md`?**
  _High betweenness centrality (0.096) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `ask_interviews()` (e.g. with `Tool surface` and `Metrics`) actually correct?**
  _`ask_interviews()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `.venv/bin/python`, `PYTHONPATH`, `NEO4J_URI` to the rest of the system?**
  _205 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `load.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07137254901960784 - nodes in this community are weakly interconnected._
- **Should `mcp_server.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05075187969924812 - nodes in this community are weakly interconnected._