# load.py

> 22 nodes

## Key Concepts

- **load.py** (24 connections) — `src/graphrag/load.py`
- **schema.py** (9 connections) — `src/graphrag/schema.py`
- **build()** (8 connections) — `src/graphrag/load.py`
- **main()** (8 connections) — `src/graphrag/load.py`
- **apply()** (5 connections) — `src/graphrag/schema.py`
- **checks()** (3 connections) — `src/graphrag/load.py`
- **embed_segments()** (3 connections) — `src/graphrag/load.py`
- **write()** (3 connections) — `src/graphrag/load.py`
- **embedding_dim()** (3 connections) — `src/graphrag/schema.py`
- **chunks()** (2 connections) — `src/graphrag/load.py`
- **counts()** (2 connections) — `src/graphrag/load.py`
- **edge_id()** (2 connections) — `src/graphrag/load.py`
- **seg_id()** (2 connections) — `src/graphrag/load.py`
- **main()** (2 connections) — `src/graphrag/schema.py`
- **vector_index_stmt()** (2 connections) — `src/graphrag/schema.py`
- **hashlib** (2 connections)
- **M5: load an assembled run (graph_input.jsonl) into Neo4j. Idempotent (MERGE…** (1 connections) — `src/graphrag/load.py`
- **Post-load invariants. Returns {name: (ok, detail)}.** (1 connections) — `src/graphrag/load.py`
- **Return (interviews, segments, edges_by_kind, stats) ready for UNWIND. Pure: no…** (1 connections) — `src/graphrag/load.py`
- **Embed question+answer per segment; cached on disk so a reload or crash does not…** (1 connections) — `src/graphrag/load.py`
- **Constraints and indexes (idempotent). Run: PYTHONPATH=src uv run python -m…** (1 connections) — `src/graphrag/schema.py`
- **Ask the embedder instead of hard-coding the dimension.** (1 connections) — `src/graphrag/schema.py`

## Relationships

- [extract.py](extract.py.md) (6 shared connections)
- [pipeline.py](pipeline.py.md) (5 shared connections)
- [__init__.py](__init__.py.md) (3 shared connections)
- [ground.py](ground.py.md) (2 shared connections)
- [pathlib](pathlib.md) (2 shared connections)
- [themes.py](themes.py.md) (1 shared connections)
- [queries.py](queries.py.md) (1 shared connections)

## Source Files

- `src/graphrag/load.py`
- `src/graphrag/schema.py`

## Audit Trail

- EXTRACTED: 53 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*