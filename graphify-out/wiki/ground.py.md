# ground.py

> 26 nodes

## Key Concepts

- **ground.py** (14 connections) — `src/graphrag/ground.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **score()** (10 connections) — `src/graphrag/ground.py`
- **is_grounded()** (7 connections) — `src/graphrag/ground.py`
- **locate()** (7 connections) — `src/graphrag/ground.py`
- **dedupe()** (5 connections) — `src/graphrag/extract.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **test_fuzzy_grounding_tolerates_punctuation_and_case()** (3 connections) — `tests/test_pipeline_core.py`
- **test_interviewer_text_is_not_user_text()** (3 connections) — `tests/test_pipeline_core.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **match()** (2 connections) — `scripts/compare_m2.py`
- **tokens()** (2 connections) — `src/graphrag/ground.py`
- **test_dedupe_drops_repeated_quotes_and_names_keeps_first()** (2 connections) — `tests/test_pipeline_core.py`
- **test_hygiene_flags_names_copied_from_prompt()** (2 connections) — `tests/test_pipeline_core.py`
- **test_parse_uses_line_start_labels_and_keeps_both_interviewer_labels()** (2 connections) — `tests/test_pipeline_core.py`
- **test_segments_pair_user_turn_with_preceding_question()** (2 connections) — `tests/test_pipeline_core.py`
- **Groundedness: what was needed (written 2026-11-07; built and measured below)** (2 connections) — `docs/07-implementation-roadmap.md`
- **test_schema_caps_items()** (1 connections) — `tests/test_pipeline_core.py`
- **test_schema_has_status_and_polarity_and_one_list()** (1 connections) — `tests/test_pipeline_core.py`
- **test_status_is_current_or_not_current()** (1 connections) — `tests/test_pipeline_core.py`
- **Names among the most frequent that appear verbatim in the prompt (a sign the…** (1 connections) — `src/graphrag/extract.py`
- **Drop repeats of the same quote, or of the same (kind, name); keep the first.…** (1 connections) — `src/graphrag/extract.py`
- **Check that an extracted quote really comes from the participant (User turns),…** (1 connections) — `src/graphrag/ground.py`
- **Fraction of quote tokens covered by in-order matching blocks of the haystack…** (1 connections) — `src/graphrag/ground.py`
- **Best participant answer for a quote: (segment idx, score).** (1 connections) — `src/graphrag/ground.py`
- *... and 1 more nodes in this community*

## Relationships

- [extract.py](extract.py.md) (15 shared connections)
- [pipeline.py](pipeline.py.md) (4 shared connections)
- [__init__.py](__init__.py.md) (3 shared connections)
- [grounded.py](grounded.py.md) (2 shared connections)
- [load.py](load.py.md) (2 shared connections)
- [07. Implementation roadmap](07._Implementation_roadmap.md) (1 shared connections)

## Source Files

- `docs/07-implementation-roadmap.md`
- `scripts/compare_m2.py`
- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 58 (98%)
- INFERRED: 1 (2%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*