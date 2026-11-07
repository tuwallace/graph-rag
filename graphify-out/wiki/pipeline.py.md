# pipeline.py

> 27 nodes

## Key Concepts

- **pipeline.py** (29 connections) — `src/graphrag/pipeline.py`
- **grounded_eval.py** (13 connections) — `eval/grounded_eval.py`
- **time** (13 connections)
- **Stage** (12 connections) — `src/graphrag/manifest.py`
- **main()** (8 connections) — `src/graphrag/pipeline.py`
- **select()** (8 connections) — `src/graphrag/pipeline.py`
- **manifest.py** (8 connections) — `src/graphrag/manifest.py`
- **assemble()** (5 connections) — `src/graphrag/pipeline.py`
- **score()** (4 connections) — `eval/grounded_eval.py`
- **stage_attributes()** (4 connections) — `src/graphrag/pipeline.py`
- **stage_normalise()** (4 connections) — `src/graphrag/pipeline.py`
- **.__init__()** (3 connections) — `src/graphrag/manifest.py`
- **kept_items()** (3 connections) — `src/graphrag/pipeline.py`
- **stage_extract()** (3 connections) — `src/graphrag/pipeline.py`
- **stage_verify()** (3 connections) — `src/graphrag/pipeline.py`
- **quality()** (2 connections) — `eval/grounded_eval.py`
- **._load()** (2 connections) — `src/graphrag/manifest.py`
- **run()** (1 connections) — `eval/grounded_eval.py`
- **.done()** (1 connections) — `src/graphrag/manifest.py`
- **.records()** (1 connections) — `src/graphrag/manifest.py`
- **.write()** (1 connections) — `src/graphrag/manifest.py`
- **Path** (1 connections)
- **Re-measure groundedness with answer generation, through the grounded path…** (1 connections) — `eval/grounded_eval.py`
- **Resumable stage bookkeeping: each stage appends one JSON line per finished key;…** (1 connections) — `src/graphrag/manifest.py`
- **Stage-major build pipeline: extract (qwen) -> verify + attributes (nimble) ->…** (1 connections) — `src/graphrag/pipeline.py`
- *... and 2 more nodes in this community*

## Relationships

- [extract.py](extract.py.md) (10 shared connections)
- [json](json.md) (9 shared connections)
- [load.py](load.py.md) (6 shared connections)
- [__init__.py](__init__.py.md) (4 shared connections)
- [score.py](score.py.md) (3 shared connections)
- [decision.py](decision.py.md) (3 shared connections)
- [themes.py](themes.py.md) (2 shared connections)
- [pathlib](pathlib.md) (2 shared connections)
- [queries.py](queries.py.md) (1 shared connections)
- [confirm_adr0008.py](confirm_adr0008.py.md) (1 shared connections)
- [run_eval.py](run_eval.py.md) (1 shared connections)
- [calibrate_verify.py](calibrate_verify.py.md) (1 shared connections)

## Source Files

- `eval/grounded_eval.py`
- `src/graphrag/manifest.py`
- `src/graphrag/pipeline.py`

## Audit Trail

- EXTRACTED: 89 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*