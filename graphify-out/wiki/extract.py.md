# extract.py

> 57 nodes

## Key Concepts

- **extract.py** (21 connections) — `src/graphrag/extract.py`
- **judge32b.py** (16 connections) — `eval/judge32b.py`
- **ground.py** (13 connections) — `src/graphrag/ground.py`
- **parse.py** (13 connections) — `src/graphrag/parse.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **segments()** (11 connections) — `src/graphrag/parse.py`
- **ADR-0008: Decision model (Jev-style) as the question router** (11 connections) — `docs/decisions/0008-decision-model-router.md`
- **score()** (9 connections) — `src/graphrag/ground.py`
- **extract()** (8 connections) — `src/graphrag/extract.py`
- **user_text()** (8 connections) — `src/graphrag/parse.py`
- **is_grounded()** (7 connections) — `src/graphrag/ground.py`
- **parse_turns()** (7 connections) — `src/graphrag/parse.py`
- **locate()** (6 connections) — `src/graphrag/ground.py`
- **recall()** (5 connections) — `eval/judge32b.py`
- **dedupe()** (5 connections) — `src/graphrag/extract.py`
- **ask()** (4 connections) — `eval/judge32b.py`
- **load_records()** (4 connections) — `eval/judge32b.py`
- **precision()** (4 connections) — `eval/judge32b.py`
- **done_ids()** (3 connections) — `eval/judge32b.py`
- **questions()** (3 connections) — `eval/judge32b.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **test_fuzzy_grounding_tolerates_punctuation_and_case()** (3 connections) — `tests/test_pipeline_core.py`
- **test_interviewer_text_is_not_user_text()** (3 connections) — `tests/test_pipeline_core.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **build_prompt()** (2 connections) — `src/graphrag/extract.py`
- *... and 32 more nodes in this community*

## Relationships

- [json](json.md) (12 shared connections)
- [pipeline.py](pipeline.py.md) (10 shared connections)
- [load.py](load.py.md) (8 shared connections)
- [grounded.py](grounded.py.md) (2 shared connections)
- [calibrate_verify.py](calibrate_verify.py.md) (2 shared connections)
- [score.py](score.py.md) (2 shared connections)
- [__init__.py](__init__.py.md) (2 shared connections)
- [pathlib](pathlib.md) (1 shared connections)
- [07. Implementation roadmap](07._Implementation_roadmap.md) (1 shared connections)
- [docs/README.md](docs-README.md.md) (1 shared connections)

## Source Files

- `docs/07-implementation-roadmap.md`
- `docs/decisions/0008-decision-model-router.md`
- `eval/judge32b.py`
- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `src/graphrag/parse.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 128 (96%)
- INFERRED: 5 (4%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*