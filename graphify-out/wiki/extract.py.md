# extract.py

> 24 nodes

## Key Concepts

- **extract.py** (23 connections) — `src/graphrag/extract.py`
- **parse.py** (17 connections) — `src/graphrag/parse.py`
- **test_pipeline_core.py** (13 connections) — `tests/test_pipeline_core.py`
- **segments()** (11 connections) — `src/graphrag/parse.py`
- **user_text()** (10 connections) — `src/graphrag/parse.py`
- **extract()** (8 connections) — `src/graphrag/extract.py`
- **locate()** (7 connections) — `src/graphrag/ground.py`
- **parse_turns()** (7 connections) — `src/graphrag/parse.py`
- **hygiene_failures()** (3 connections) — `src/graphrag/extract.py`
- **test_locate_finds_the_segment()** (3 connections) — `tests/test_pipeline_core.py`
- **build_prompt()** (2 connections) — `src/graphrag/extract.py`
- **test_hygiene_flags_names_copied_from_prompt()** (2 connections) — `tests/test_pipeline_core.py`
- **test_parse_uses_line_start_labels_and_keeps_both_interviewer_labels()** (2 connections) — `tests/test_pipeline_core.py`
- **test_segments_pair_user_turn_with_preceding_question()** (2 connections) — `tests/test_pipeline_core.py`
- **test_schema_caps_items()** (1 connections) — `tests/test_pipeline_core.py`
- **test_schema_has_status_and_polarity_and_one_list()** (1 connections) — `tests/test_pipeline_core.py`
- **test_status_is_current_or_not_current()** (1 connections) — `tests/test_pipeline_core.py`
- **Client** (1 connections)
- **Extraction v3: one list of typed items per transcript, each with status,…** (1 connections) — `src/graphrag/extract.py`
- **Names among the most frequent that appear verbatim in the prompt (a sign the…** (1 connections) — `src/graphrag/extract.py`
- **Best participant answer for a quote: (segment idx, score).** (1 connections) — `src/graphrag/ground.py`
- **Split a transcript into turns and question/answer segments.** (1 connections) — `src/graphrag/parse.py`
- **One segment per participant turn, paired with the interviewer turn before it.** (1 connections) — `src/graphrag/parse.py`
- **Line-start labels only, so quoted chat logs inside an answer are not split.…** (1 connections) — `src/graphrag/parse.py`

## Relationships

- [ground.py](ground.py.md) (9 shared connections)
- [pipeline.py](pipeline.py.md) (8 shared connections)
- [json](json.md) (6 shared connections)
- [concern_merge.py](concern_merge.py.md) (5 shared connections)
- [load.py](load.py.md) (5 shared connections)
- [sys](sys.md) (4 shared connections)
- [grounded_eval.py](grounded_eval.py.md) (2 shared connections)
- [judge32b.py](judge32b.py.md) (2 shared connections)
- [score.py](score.py.md) (2 shared connections)
- [__init__.py](__init__.py.md) (2 shared connections)
- [mcp_server.py](mcp_server.py.md) (1 shared connections)

## Source Files

- `src/graphrag/extract.py`
- `src/graphrag/ground.py`
- `src/graphrag/parse.py`
- `tests/test_pipeline_core.py`

## Audit Trail

- EXTRACTED: 83 (100%)
- INFERRED: 0 (0%)
- AMBIGUOUS: 0 (0%)

---

*Part of the graphify knowledge wiki. See [index](index.md) to navigate.*