# load.py

> 27 nodes

## Key Concepts

- **load.py** (24 connections) — `src/graphrag/load.py`
- **config.py** (15 connections) — `src/graphrag/config.py`
- **schema.py** (9 connections) — `src/graphrag/schema.py`
- **build()** (8 connections) — `src/graphrag/load.py`
- **main()** (8 connections) — `src/graphrag/load.py`
- **apply()** (5 connections) — `src/graphrag/schema.py`
- **os** (4 connections)
- **checks()** (3 connections) — `src/graphrag/load.py`
- **embed_segments()** (3 connections) — `src/graphrag/load.py`
- **write()** (3 connections) — `src/graphrag/load.py`
- **embedding_dim()** (3 connections) — `src/graphrag/schema.py`
- **argparse** (3 connections)
- **chunks()** (2 connections) — `src/graphrag/load.py`
- **counts()** (2 connections) — `src/graphrag/load.py`
- **edge_id()** (2 connections) — `src/graphrag/load.py`
- **seg_id()** (2 connections) — `src/graphrag/load.py`
- **main()** (2 connections) — `src/graphrag/schema.py`
- **vector_index_stmt()** (2 connections) — `src/graphrag/schema.py`
- **hashlib** (2 connections)
- **Settings from environment / .env. No secrets in code.** (1 connections) — `src/graphrag/config.py`
- **M5: load an assembled run (graph_input.jsonl) into Neo4j. Idempotent (MERGE…** (1 connections) — `src/graphrag/load.py`
- **Post-load invariants. Returns {name: (ok, detail)}.** (1 connections) — `src/graphrag/load.py`
- **Return (interviews, segments, edges_by_kind, stats) ready for UNWIND. Pure: no…** (1 connections) — `src/graphrag/load.py`
- **Embed question+answer per segment; cached on disk so a reload or crash does not…** (1 connections) — `src/graphrag/load.py`
- **Constraints and indexes (idempotent). Run: PYTHONPATH=src uv run python -m…** (1 connections) — `src/graphrag/schema.py`
- *... and 2 more nodes in this community*

## Relationships

- [extract.py](extract.py.md) (8 shared connections)
- [pipeline.py](pipeline.py.md) (6 shared connections)
- [__init__.py](__init__.py.md) (5 shared connections)
- [queries.py](queries.py.md) (3 shared connections)
- [mcp_server.py](mcp_server.py.md) (2 shared connections)
- [themes.py](themes.py.md) (2 shared connections)
- [pathlib](pathlib.md) (1 shared connections)
- [decision.py](decision.py.md) (1 shared connections)
- [grounded.py](grounded.py.md) (1 shared connections)
- [json](json.md) (1 shared connections)
- [sys](sys.md) (1 shared connections)
- [judge32b.py](judge32b.py.md) (1 shared connections)

## Source Files

- `src/graphrag/config.py`
- `src/graphrag/load.py`
- `src/graphrag/schema.py`

## Audit Trail

- EXTRACTED: 71 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*