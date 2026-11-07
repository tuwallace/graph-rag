# 02. Architecture

## Components

```mermaid
flowchart LR
  subgraph Host["macOS host (M2 Pro, 32 GB), Apple GPU"]
    OLL["Ollama :11434<br/>qwen3:8b-16k, nomic-embed-text,<br/>nimble (/v1/systemone)"]
    ING["ingest pipeline (Python, uv)<br/>parse, extract, ground, verify, normalise, load"]
    CLI["ollmcp"]
    MCP["MCP server: helpdesk-graph -> interview-graph<br/>(stdio)"]
  end
  subgraph Docker["Docker VM (8 GB), ports on 127.0.0.1"]
    N4[("Neo4j Community<br/>graph + vector index")]
  end
  HF[/"Hugging Face CSVs<br/>(git-ignored data/raw)"/] --> ING
  ING <--> OLL
  ING --> N4
  CLI <-->|chat + tool calls| OLL
  CLI --- MCP
  MCP --> N4
  MCP -->|"route + embed"| OLL
```

Qdrant and Phoenix are no longer required ([ADR-0011](decisions/0011-retrieval-in-neo4j.md)). Tracing can be added later (OpenTelemetry to Phoenix) but is not on the critical path.

## Two flows

**Build (offline, hours):** CSV, parse segments, `qwen3` extraction per transcript, grounding, `nimble` verification and typed attributes, embedding and normalisation, `MERGE` into Neo4j, theme detection.
Each stage writes a rebuildable artefact keyed by `run_id`, `model`, `prompt_version` so a bad stage can be rerun alone.

**Query (interactive):**

```mermaid
sequenceDiagram
  participant U as User
  participant L as qwen3:8b-16k (ollmcp)
  participant G as interview-graph tools
  participant R as nimble router
  participant N as Neo4j
  U->>L: "How do scientists worry about AI errors?"
  L->>G: ask_interviews(question)
  G->>R: route + confidence
  R-->>G: concept_search (0.93)
  G->>N: vector search on Segment, expand to concepts, quotes, group counts
  N-->>G: rows (segment ids, quotes, counts)
  G-->>L: compact JSON
  L-->>U: answer with quotes and interview ids
```

## Routes (decided by `nimble`, see [04](04-query-and-tools.md))

`local_search`, `concept_stats`, `compare_groups`, `theme_overview` (global), `evidence`, `out_of_scope`. Below the confidence threshold the tool asks the user to rephrase.

## Resource budget

| Consumer | Where | Memory |
|---|---|---|
| qwen3:8b-16k | host | 7.4 GB loaded at 16k context (from `ollama ps`) |
| nimble | host | 9.3 GB on disk |
| nomic-embed-text | host | 0.3 GB |
| Neo4j (heap 1 GB, page cache 512 MB) | Docker | about 2 GB |
| `qwen2.5:32b` (offline theme summaries and judge) | host | 19 GB, run alone |

During the build, qwen3 and nimble are used one after another, not together, to keep timings clean. At query time both are resident; set `OLLAMA_MAX_LOADED_MODELS=2`.

## Failure handling

| Failure | Behaviour |
|---|---|
| Neo4j down | Tools return an error; the model says the graph is unavailable. |
| Router below confidence threshold | Ask for clarification; run nothing. |
| No segment above a similarity floor | Say nothing relevant was found; do not guess. |
| Extraction stage crash | Resume from the last written artefact (idempotent stages). |
| Model passes bad arguments | Tools validate enums and clamp limits. |

Code layout (proposed): `src/graphrag/{parse,extract,ground,verify,normalise,load,queries,mcp_server}.py`, `spike/` (existing), `eval/`, `docs/`, `docker-compose.yml`, `mcp.json`.
