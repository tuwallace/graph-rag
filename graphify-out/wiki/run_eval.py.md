# run_eval.py

> 20 nodes

## Key Concepts

- **run_eval.py** (16 connections) — `eval/run_eval.py`
- **confirm_adr0008.py** (14 connections) — `eval/confirm_adr0008.py`
- **neo4j** (11 connections)
- **route_generated.py** (8 connections) — `eval/route_generated.py`
- **final_answer()** (4 connections) — `eval/run_eval.py`
- **run_tool()** (4 connections) — `eval/run_eval.py`
- **timed_decide()** (3 connections) — `eval/confirm_adr0008.py`
- **chat()** (3 connections) — `eval/run_eval.py`
- **config_A()** (3 connections) — `eval/run_eval.py`
- **b_row()** (2 connections) — `eval/confirm_adr0008.py`
- **config_B()** (2 connections) — `eval/run_eval.py`
- **config_C()** (2 connections) — `eval/run_eval.py`
- **a_row()** (1 connections) — `eval/confirm_adr0008.py`
- **summ()** (1 connections) — `eval/confirm_adr0008.py`
- **pct()** (1 connections) — `eval/route_generated.py`
- **res()** (1 connections) — `eval/run_eval.py`
- **ADR-0008 confirmation on questions written after the router changes were chosen…** (1 connections) — `eval/confirm_adr0008.py`
- **Routing accuracy on questions written by a different model (qwen2.5:32b) from…** (1 connections) — `eval/route_generated.py`
- **M7: run the 40 questions through configs A (qwen3 picks typed tools), B (nimble…** (1 connections) — `eval/run_eval.py`
- **Same behaviour as the typed MCP profile.** (1 connections) — `eval/run_eval.py`

## Relationships

- [sys](sys.md) (6 shared connections)
- [json](json.md) (5 shared connections)
- [__init__.py](__init__.py.md) (3 shared connections)
- [score.py](score.py.md) (2 shared connections)
- [pathlib](pathlib.md) (2 shared connections)
- [mcp_server.py](mcp_server.py.md) (2 shared connections)
- [load.py](load.py.md) (2 shared connections)
- [router.py](router.py.md) (1 shared connections)
- [grounded_eval.py](grounded_eval.py.md) (1 shared connections)
- [queries.py](queries.py.md) (1 shared connections)
- [themes.py](themes.py.md) (1 shared connections)

## Source Files

- `eval/confirm_adr0008.py`
- `eval/route_generated.py`
- `eval/run_eval.py`

## Audit Trail

- EXTRACTED: 49 (92%)
- INFERRED: 4 (8%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*