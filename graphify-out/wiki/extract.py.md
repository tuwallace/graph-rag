# extract.py

> 38 nodes

## Key Concepts

- **extract.py** (21 connections) — `src/graphrag/extract.py`
- **re** (15 connections)
- **ground.py** (14 connections) — `src/graphrag/ground.py`
- **parse.py** (14 connections) — `src/graphrag/parse.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **segments()** (11 connections) — `src/graphrag/parse.py`
- **score()** (10 connections) — `src/graphrag/ground.py`
- **user_text()** (9 connections) — `src/graphrag/parse.py`
- **extract()** (8 connections) — `src/graphrag/extract.py`
- **is_grounded()** (7 connections) — `src/graphrag/ground.py`
- **locate()** (7 connections) — `src/graphrag/ground.py`
- **parse_turns()** (7 connections) — `src/graphrag/parse.py`
- **dedupe()** (5 connections) — `src/graphrag/extract.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **test_fuzzy_grounding_tolerates_punctuation_and_case()** (3 connections) — `tests/test_pipeline_core.py`
- **test_interviewer_text_is_not_user_text()** (3 connections) — `tests/test_pipeline_core.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **build_prompt()** (2 connections) — `src/graphrag/extract.py`
- **_nq()** (2 connections) — `src/graphrag/extract.py`
- **tokens()** (2 connections) — `src/graphrag/ground.py`
- **test_dedupe_drops_repeated_quotes_and_names_keeps_first()** (2 connections) — `tests/test_pipeline_core.py`
- **test_hygiene_flags_names_copied_from_prompt()** (2 connections) — `tests/test_pipeline_core.py`
- **test_parse_uses_line_start_labels_and_keeps_both_interviewer_labels()** (2 connections) — `tests/test_pipeline_core.py`
- **test_segments_pair_user_turn_with_preceding_question()** (2 connections) — `tests/test_pipeline_core.py`
- **test_schema_caps_items()** (1 connections) — `tests/test_pipeline_core.py`
- *... and 13 more nodes in this community*

## Relationships

- [load.py](load.py.md) (8 shared connections)
- [pipeline.py](pipeline.py.md) (7 shared connections)
- [themes.py](themes.py.md) (6 shared connections)
- [json](json.md) (6 shared connections)
- [collections](collections.md) (4 shared connections)
- [grounded.py](grounded.py.md) (3 shared connections)
- [score.py](score.py.md) (3 shared connections)
- [sys](sys.md) (3 shared connections)
- [judge32b.py](judge32b.py.md) (2 shared connections)
- [__init__.py](__init__.py.md) (2 shared connections)
- [07. Implementation roadmap](07._Implementation_roadmap.md) (1 shared connections)
- [prepush_check.py](prepush_check.py.md) (1 shared connections)

## Source Files

- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `src/graphrag/parse.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 113 (99%)
- INFERRED: 1 (1%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*