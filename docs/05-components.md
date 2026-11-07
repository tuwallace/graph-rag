# 05. Component recommendations

Fixed by the brief: **Ollama, ollmcp, Docker**. Everything else is a recommendation, with reasoning in the linked decision record.

| Slot | Recommendation | Alternatives | Why | ADR |
|---|---|---|---|---|
| Corpus | **Anthropic Interviewer** (500-transcript demo subset) | helpdesk tickets (archived) | Real prose; justifies extraction | [0009](decisions/0009-corpus-anthropic-interviewer.md) |
| Graph DB | **Neo4j Community 5.x**, Docker | Memgraph, FalkorDB, Kuzu, Postgres + AGE | Best Cypher tooling; free | [0001](decisions/0001-graph-database.md) |
| Vector search | **Neo4j native vector index** on `Segment` | Qdrant | One store; vector then traversal in one query | [0011](decisions/0011-retrieval-in-neo4j.md) |
| Extractor | **`qwen3:8b-16k`** with JSON-schema output | `qwen2.5:32b` (too slow), per-segment calls | Measured: valid JSON 20/20, 31 s per transcript | [0010](decisions/0010-extraction-pipeline.md) |
| Verifier, attributes, router | **`nimble`** decision model via `/v1/systemone` | `tev1` (untested), qwen3 | Typed answers with probabilities; measured p50 2.4 s for 3 questions | [0008](decisions/0008-decision-model-router.md) |
| Answer model | **`qwen3:8b-16k`** via ollmcp | `llama3.1:8b-q8`, `glm-4.7-flash` | Tool use proven earlier; fits memory | [0005](decisions/0005-local-llm-selection.md) |
| Theme summaries, judge | **`qwen2.5:32b-instruct-q4_K_M`**, run alone | qwen3 self-judge | Larger, different family; offline only | [0005](decisions/0005-local-llm-selection.md) |
| Embeddings | **`nomic-embed-text`** (768-d; verify) | bge | Installed; prefix-aware | [0005](decisions/0005-local-llm-selection.md) |
| Entity merge | **Embedding clustering + sample review** | LLM merge, string rules | Names rarely repeat (115 distinct of 123 items) | [0010](decisions/0010-extraction-pipeline.md) |
| Agent shell | **ollmcp** 0.33.x | custom loop | Brief | [0006](decisions/0006-deployment-topology.md) |
| Python | **uv + Python 3.12** | system 3.14 | Wheels; matches earlier project | n/a |
| Privacy | Do not commit data; PII pass; CC-BY attribution | | Public repo | [0012](decisions/0012-privacy-for-transcripts.md) |

## Neo4j container

Use Community, pinned to a tag you have verified. Do not use the local `neo4j:5-enterprise` image (license acceptance, public MIT repo). The tag `5.26-community` was verified to pull on this Mac in M1.

```yaml
# docker-compose.yml (running since M1; the file in the repo root is authoritative)
services:
  neo4j:
    image: neo4j:5.26-community        # verify tag before use
    restart: unless-stopped
    ports: ["127.0.0.1:7474:7474", "127.0.0.1:7687:7687"]
    environment:
      NEO4J_AUTH: "neo4j/${NEO4J_PASSWORD:?set in .env}"
      NEO4J_server_memory_heap_initial__size: 1G
      NEO4J_server_memory_heap_max__size: 1G
      NEO4J_server_memory_pagecache_size: 512M
      NEO4J_db_transaction_timeout: 30s
    volumes: ["./data/neo4j:/data"]
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p \"$$NEO4J_PASSWORD\" 'RETURN 1' || exit 1"]
      interval: 10s
      retries: 12
```

APOC is no longer needed by the queries in [04](04-query-and-tools.md); add it only if community detection or the loader needs it. Theme detection can run in Python (for example `networkx`) and write results back.
Community edition has one user database, and in M1 `CREATE USER` worked but `CREATE ROLE` and `GRANT ROLE` were rejected, so there is no database-level read-only role; read mode is enforced in the application ([ADR-0012](decisions/0012-privacy-for-transcripts.md)). The Docker VM has 8.2 GB shared with other stacks.

## Installed models and their role

| Model | Size | Role |
|---|---|---|
| `qwen3:8b-16k` | 5.2 GB (7.4 GB loaded) | Extractor, answer writer |
| `nimble` | 9.3 GB | Router, verifier, typed attributes |
| `nomic-embed-text` | 0.3 GB | Embeddings |
| `qwen2.5:32b-instruct-q4_K_M` | 19 GB | Offline themes and judging; run alone |
| `qwen2.5-coder:7b-instruct-q8_0` | 8.1 GB | Text-to-Cypher drafts, only if that path is enabled |
| `llama3.1:8b-instruct-q8_0`, `glm-4.7-flash` | 8.5 / 19 GB | Comparison runs only |
| `qwen3:8b`, `phi3`, `llama3`, `llava`, `llama3.2-vision` | | Not used |

Optional pull: `tev1` (4B) or `tev1:0.8b` to test a lighter, faster router (described as experimental). No other pulls needed.

## Throughput reality (measured, one machine)

| Stage | Measured | Full corpus (1,250) | Demo scope (500) |
|---|---|---|---|
| Extraction, qwen3 (v3.2 prompt, measured in M2) | 44.9 s per transcript (31 s in the spike with the simpler v2 prompt) | about 15.6 h | about 6.2 h |
| `nimble` attitude, 1 question per segment (M3, `attributes` v2) | 1.66 s mean (50 segments) | about 6.7 h | about 2.7 h (about 5,800 segments, estimated) |
| `nimble` verify, 2 yes/no per item (M3) | about 1.05 s per item, 16 s per transcript | about 5.6 h | about 2.3 h |

Plan runs overnight and in resumable stages. Slimming the `nimble` calls is the cheapest win ([spike 01](spike-01-extraction.md)).
