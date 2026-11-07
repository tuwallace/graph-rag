# load.py

> 54 nodes

## Key Concepts

- **load.py** (24 connections) — `src/graphrag/load.py`
- **extract.py** (21 connections) — `src/graphrag/extract.py`
- **ground.py** (13 connections) — `src/graphrag/ground.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **parse.py** (12 connections) — `src/graphrag/parse.py`
- **segments()** (11 connections) — `src/graphrag/parse.py`
- **score()** (9 connections) — `src/graphrag/ground.py`
- **extract()** (8 connections) — `src/graphrag/extract.py`
- **build()** (8 connections) — `src/graphrag/load.py`
- **main()** (8 connections) — `src/graphrag/load.py`
- **is_grounded()** (7 connections) — `src/graphrag/ground.py`
- **parse_turns()** (7 connections) — `src/graphrag/parse.py`
- **user_text()** (7 connections) — `src/graphrag/parse.py`
- **select()** (7 connections) — `src/graphrag/pipeline.py`
- **locate()** (6 connections) — `src/graphrag/ground.py`
- **dedupe()** (5 connections) — `src/graphrag/extract.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **checks()** (3 connections) — `src/graphrag/load.py`
- **embed_segments()** (3 connections) — `src/graphrag/load.py`
- **write()** (3 connections) — `src/graphrag/load.py`
- **test_fuzzy_grounding_tolerates_punctuation_and_case()** (3 connections) — `tests/test_pipeline_core.py`
- **test_interviewer_text_is_not_user_text()** (3 connections) — `tests/test_pipeline_core.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **build_prompt()** (2 connections) — `src/graphrag/extract.py`
- **_nq()** (2 connections) — `src/graphrag/extract.py`
- *... and 29 more nodes in this community*

## Relationships

- [pipeline.py](pipeline.py.md) (11 shared connections)
- [re](re.md) (7 shared connections)
- [07. Implementation roadmap](07._Implementation_roadmap.md) (3 shared connections)
- [run_eval.py](run_eval.py.md) (3 shared connections)
- [score.py](score.py.md) (3 shared connections)
- [json](json.md) (3 shared connections)
- [queries.py](queries.py.md) (3 shared connections)
- [compare_m2.py](compare_m2.py.md) (2 shared connections)
- [__init__.py](__init__.py.md) (2 shared connections)
- [themes.py](themes.py.md) (1 shared connections)

## Source Files

- `docs/07-implementation-roadmap.md`
- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `src/graphrag/load.py`
- `src/graphrag/parse.py`
- `src/graphrag/pipeline.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 133 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*