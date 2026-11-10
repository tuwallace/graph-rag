# judge32b.py

> 12 nodes

## Key Concepts

- **judge32b.py** (17 connections) — `eval/judge32b.py`
- **route_generated.py** (8 connections) — `eval/route_generated.py`
- **recall()** (5 connections) — `eval/judge32b.py`
- **os** (5 connections)
- **ask()** (4 connections) — `eval/judge32b.py`
- **load_records()** (4 connections) — `eval/judge32b.py`
- **precision()** (4 connections) — `eval/judge32b.py`
- **done_ids()** (3 connections) — `eval/judge32b.py`
- **questions()** (3 connections) — `eval/judge32b.py`
- **pct()** (1 connections) — `eval/route_generated.py`
- **Independent checks by a larger model (qwen2.5:32b, run alone), so the 8B…** (1 connections) — `eval/judge32b.py`
- **Routing accuracy on questions written by a different model (qwen2.5:32b) from…** (1 connections) — `eval/route_generated.py`

## Relationships

- [json](json.md) (5 shared connections)
- [pipeline.py](pipeline.py.md) (4 shared connections)
- [run_eval.py](run_eval.py.md) (4 shared connections)
- [load.py](load.py.md) (2 shared connections)
- [__init__.py](__init__.py.md) (2 shared connections)
- [ADR-0008: Decision model (Jev-style) as the question router](ADR-0008-_Decision_model_Jev-style_as_the_question_router.md) (1 shared connections)
- [queries.py](queries.py.md) (1 shared connections)
- [mcp_server.py](mcp_server.py.md) (1 shared connections)

## Source Files

- `eval/judge32b.py`
- `eval/route_generated.py`

## Audit Trail

- EXTRACTED: 34 (89%)
- INFERRED: 4 (11%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*