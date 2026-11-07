# run_eval.py

> 26 nodes

## Key Concepts

- **run_eval.py** (15 connections) — `eval/run_eval.py`
- **confirm_adr0008.py** (14 connections) — `eval/confirm_adr0008.py`
- **neo4j** (10 connections)
- **schema.py** (9 connections) — `src/graphrag/schema.py`
- **apply()** (5 connections) — `src/graphrag/schema.py`
- **f()** (4 connections) — `eval/confirm_adr0008.py`
- **final_answer()** (4 connections) — `eval/run_eval.py`
- **run_tool()** (4 connections) — `eval/run_eval.py`
- **timed_decide()** (3 connections) — `eval/confirm_adr0008.py`
- **chat()** (3 connections) — `eval/run_eval.py`
- **config_A()** (3 connections) — `eval/run_eval.py`
- **embedding_dim()** (3 connections) — `src/graphrag/schema.py`
- **b_row()** (2 connections) — `eval/confirm_adr0008.py`
- **config_B()** (2 connections) — `eval/run_eval.py`
- **config_C()** (2 connections) — `eval/run_eval.py`
- **main()** (2 connections) — `scripts/download_data.py`
- **main()** (2 connections) — `src/graphrag/schema.py`
- **vector_index_stmt()** (2 connections) — `src/graphrag/schema.py`
- **a_row()** (1 connections) — `eval/confirm_adr0008.py`
- **summ()** (1 connections) — `eval/confirm_adr0008.py`
- **res()** (1 connections) — `eval/run_eval.py`
- **ADR-0008 confirmation on questions written after the router changes were chosen…** (1 connections) — `eval/confirm_adr0008.py`
- **M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble…** (1 connections) — `eval/run_eval.py`
- **Same behaviour as the typed MCP profile.** (1 connections) — `eval/run_eval.py`
- **Constraints and indexes (idempotent). Run: PYTHONPATH=src uv run python -m…** (1 connections) — `src/graphrag/schema.py`
- *... and 1 more nodes in this community*

## Relationships

- [json](json.md) (4 shared connections)
- [sys](sys.md) (3 shared connections)
- [load.py](load.py.md) (3 shared connections)
- [pipeline.py](pipeline.py.md) (3 shared connections)
- [__init__.py](__init__.py.md) (3 shared connections)
- [router.py](router.py.md) (2 shared connections)
- [score.py](score.py.md) (2 shared connections)
- [re](re.md) (2 shared connections)
- [queries.py](queries.py.md) (2 shared connections)
- [compare_m2.py](compare_m2.py.md) (1 shared connections)
- [mcp_server.py](mcp_server.py.md) (1 shared connections)
- [themes.py](themes.py.md) (1 shared connections)

## Source Files

- `eval/confirm_adr0008.py`
- `eval/run_eval.py`
- `scripts/download_data.py`
- `src/graphrag/schema.py`

## Audit Trail

- EXTRACTED: 56 (90%)
- INFERRED: 6 (10%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*