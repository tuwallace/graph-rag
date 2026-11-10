# ADR-0006: Deployment topology

- Status: accepted 2026-11-10 by the project owner (earlier: proposed (amended 2026-11-05: Qdrant and Phoenix are no longer required; only Neo4j runs in Docker))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Everything is configured by URLs and compose files.

## Context

The brief fixes Ollama, ollmcp and Docker. helpdesk-rag already decided: Ollama on the host because Docker on macOS cannot use the Apple GPU (a containerised Ollama would run on CPU).
Qdrant and Phoenix already run in Docker from the helpdesk-rag compose file. The Docker VM currently has 8.2 GB and hosts unrelated stacks. MCP servers launched by ollmcp use stdio.

## Decision drivers

- Use the Apple GPU for LLM inference
- Reproducible service setup; nothing installed globally
- Avoid duplicating services that already run
- Network exposure (this may become a public repo; none of these services authenticate except Neo4j)

## Options

1. **Ollama, ollmcp and the MCP servers on the host; Neo4j, Qdrant, Phoenix in Docker**
2. Everything in Docker, including Ollama
3. Everything on the host (Homebrew Neo4j, local Qdrant binary)

## Weighted decision matrix

| Criterion | Weight | 1. Hybrid | 2. All Docker | 3. All host |
|---|---|---|---|---|
| Apple GPU for inference | 35 | 5 | 1 | 5 |
| Reproducible, isolated services | 25 | 4 | 5 | 2 |
| Resource control | 20 | 4 | 3 | 4 |
| Simplicity | 20 | 4 | 4 | 3 |
| **Weighted score (out of 5)** | 100 | **4.35** | 3.00 | 3.65 |

## Decision

Option 1.

| Piece | Runs on | Port | Binding |
|---|---|---|---|
| Ollama | host | 11434 | default (localhost) |
| ollmcp, `helpdesk-graph` and `helpdesk-rag` MCP servers | host (stdio subprocesses) | none | n/a |
| Neo4j Community | Docker (this repo's compose) | 7474, 7687 | **127.0.0.1 only** |
| Qdrant | Docker (helpdesk-rag compose, reused) | 6333 | 127.0.0.1 only |
| Phoenix | Docker (helpdesk-rag compose, reused) | 6006, 4317 | 127.0.0.1 only |

Operating notes:

- Start order: `docker compose up -d` in helpdesk-rag (Qdrant, Phoenix), then in graph-rag (Neo4j). The loader waits on the Neo4j healthcheck.
- `helpdesk-graph` reaches the host services at `localhost`; no Docker network is shared between the two compose projects.
- Phoenix spans: one per MCP tool call plus one per Cypher query (`openinference.span.kind = TOOL` and `CHAIN`), matching the existing `tracing.py`.

## Consequences

- Good: GPU inference; each service restarts independently; no new Python service container to maintain.
- Costs: two compose projects must be up; helpdesk-rag becomes a runtime dependency of this repo (documented, imported by `PYTHONPATH`).
- Risk: if helpdesk-rag's Qdrant collection is stale, graph tools see stale vectors. Mitigation: the join test in phase 1 fails loudly on missing keys.

## Confirmation

`docker compose ps` healthy for both projects; `ollama ps` shows GPU use; a smoke call to each MCP tool succeeds through ollmcp.

## Revisit when

The Docker VM needs more memory than the Mac can spare, or Ollama ships Apple GPU passthrough in containers.
