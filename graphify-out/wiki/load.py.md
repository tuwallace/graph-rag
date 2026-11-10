# load.py

> 52 nodes

## Key Concepts

- **load.py** (24 connections) — `src/graphrag/load.py`
- **extract.py** (23 connections) — `src/graphrag/extract.py`
- **parse.py** (17 connections) — `src/graphrag/parse.py`
- **ground.py** (14 connections) — `src/graphrag/ground.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **segments()** (11 connections) — `src/graphrag/parse.py`
- **score()** (10 connections) — `src/graphrag/ground.py`
- **user_text()** (10 connections) — `src/graphrag/parse.py`
- **extract()** (8 connections) — `eval/concern_pass.py`
- **extract()** (8 connections) — `src/graphrag/extract.py`
- **build()** (8 connections) — `src/graphrag/load.py`
- **main()** (8 connections) — `src/graphrag/load.py`
- **is_grounded()** (7 connections) — `src/graphrag/ground.py`
- **locate()** (7 connections) — `src/graphrag/ground.py`
- **parse_turns()** (7 connections) — `src/graphrag/parse.py`
- **dedupe()** (5 connections) — `src/graphrag/extract.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **checks()** (3 connections) — `src/graphrag/load.py`
- **embed_segments()** (3 connections) — `src/graphrag/load.py`
- **write()** (3 connections) — `src/graphrag/load.py`
- **test_fuzzy_grounding_tolerates_punctuation_and_case()** (3 connections) — `tests/test_pipeline_core.py`
- **test_interviewer_text_is_not_user_text()** (3 connections) — `tests/test_pipeline_core.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **build_prompt()** (2 connections) — `src/graphrag/extract.py`
- **tokens()** (2 connections) — `src/graphrag/ground.py`
- *... and 27 more nodes in this community*

## Relationships

- [pipeline.py](pipeline.py.md) (24 shared connections)
- [re](re.md) (6 shared connections)
- [__init__.py](__init__.py.md) (5 shared connections)
- [json](json.md) (5 shared connections)
- [calibrate_verify.py](calibrate_verify.py.md) (4 shared connections)
- [grounded.py](grounded.py.md) (2 shared connections)
- [judge32b.py](judge32b.py.md) (2 shared connections)
- [score.py](score.py.md) (2 shared connections)
- [queries.py](queries.py.md) (1 shared connections)
- [pathlib](pathlib.md) (1 shared connections)
- [07. Implementation roadmap](07._Implementation_roadmap.md) (1 shared connections)

## Source Files

- `docs/07-implementation-roadmap.md`
- `eval/concern_pass.py`
- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `src/graphrag/load.py`
- `src/graphrag/parse.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 145 (99%)
- INFERRED: 2 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*