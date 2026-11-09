# 08. Evaluation results (M7)

> All results in this file and in the follow-up checks describe the **500-interview** graph (500 of the 1,250 interviews in the dataset), not the full dataset.

## Label confirmation

The project owner stated on 2026-11-07 and 2026-11-09 that they confirmed the model-judged labels (the 120-edge precision sample, the recall coverage judgements, and the 27 labels on the second-pass concern edges) and reviewed the generated evaluation questions. I could not see which items they inspected, so this is recorded as their statement. `eval/check_labels.py` checks that the label files are complete and well formed (120 unique edges, valid labels, 30 kept per kind plus 30 rejected, 10 transcripts, 8 questions per route); it does not judge whether labels are right.

Follow-up results from the 32b judge, second pass and router v3 are in `07-implementation-roadmap.md` ("Open items").


Run 2026-11-07 on the 500-interview graph (`demo1`; 500 of the 1,250 interviews in the dataset: all creatives, all scientists, 250 of 1,000 workforce). 40 questions I wrote (`eval/questions.json`), split alternately within each route into a dev half (21) and a held-out half (19). Configs: **A** qwen3:8b-16k picks among 5 typed tools; **B** `nimble` routes to one tool (threshold 0.6); **C** plain vector top 5 with no graph. All use the same answer model (qwen3:8b-16k, thinking off, temperature 0) and the same answer rules. Runner: `eval/run_eval.py`; scorer: `eval/score.py`. Raw answers are in git-ignored `data/eval/`; this page holds aggregates only.

Read with care: one author wrote the questions, the gold routes and the scoring rules, after seeing which concepts the graph holds. With 36 in-scope questions, a gap of 3 questions is 8 points and is within noise. Two scorer corrections were made after the first scores: (1) the compare-answer check was revised after I saw the first scores (answers often gave a percent of the group, not a raw count; both versions are shown); (2) quote pairing and list numbers (the first scorer mis-paired quote marks after short quoted terms and counted list markers such as "1." as figures, which understated quote validity and number groundedness; the corrected scores are below, and B's quote validity moved from 84% to 94%). Router configuration B in this page is router v1 (threshold 0.6); see ADR-0008 for router v2 routing results.




### Dev half (tuning allowed)

| Measure | A: qwen3 picks tools | B: nimble router | C: plain vector RAG |
|---|---|---|---|
| Questions run | 21 | 21 | 21 |
| Route or tool correct (in scope) | 16/19 (84%) | 17/19 (89%) | n/a |
| Abstained (in scope) | 0/19 (0%) | 3/19 (16%) | never |
| Route correct when it answered | 16/19 (84%) | 16/16 (100%) | n/a |
| Arguments correct (stats, compare, evidence) | 11/13 (85%) | 10/13 (77%) | n/a |
| Out-of-scope handled (no query / refusal) | 2/2 (100%) | 2/2 (100%) | 2/2 (100%) *heuristic |
| Count answers correct (stats + compare; compare check revised) | 6/9 (67%) | 5/9 (56%) | 0/9 (0%) |
| Compare answers correct, original strict check | 0/4 (0%) | 0/4 (0%) | 0/4 (0%) |
| Quotes found in the cited interview | 33/37 (89%) | 31/34 (91%) | 56/63 (89%) |
| Quotes found anywhere in the corpus | 35/37 (95%) | 32/34 (94%) | 56/63 (89%) |
| Numbers in answer found in tool output | 29/30 (97%) | 18/18 (100%) | 2/2 (100%) |
| Latency p50 / p95 (s) | 4.4 / 11.3 | 5.2 / 17.9 | 6.1 / 8.6 |
| Errors | 0 | 0 | 0 |

### Router abstention by threshold (Dev half (tuning allowed), route confidence only)

| Threshold | In-scope abstained | Route correct when answered | Out-of-scope questions answered as in-scope |
|---|---|---|---|
| 0.5 | 1/19 (5%) | 17/18 (94%) | 0/2 (0%) |
| 0.6 | 2/19 (11%) | 16/17 (94%) | 0/2 (0%) |
| 0.7 | 4/19 (21%) | 15/15 (100%) | 0/2 (0%) |
| 0.8 | 6/19 (32%) | 13/13 (100%) | 0/2 (0%) |

### Held-out half

| Measure | A: qwen3 picks tools | B: nimble router | C: plain vector RAG |
|---|---|---|---|
| Questions run | 19 | 19 | 19 |
| Route or tool correct (in scope) | 15/17 (88%) | 16/17 (94%) | n/a |
| Abstained (in scope) | 0/17 (0%) | 1/17 (6%) | never |
| Route correct when it answered | 15/17 (88%) | 15/16 (94%) | n/a |
| Arguments correct (stats, compare, evidence) | 10/11 (91%) | 11/11 (100%) | n/a |
| Out-of-scope handled (no query / refusal) | 2/2 (100%) | 2/2 (100%) | 1/2 (50%) *heuristic |
| Count answers correct (stats + compare; compare check revised) | 8/8 (100%) | 7/8 (88%) | 0/8 (0%) |
| Compare answers correct, original strict check | 0/3 (0%) | 0/3 (0%) | 0/3 (0%) |
| Quotes found in the cited interview | 27/35 (77%) | 27/28 (96%) | 29/33 (88%) |
| Quotes found anywhere in the corpus | 31/35 (89%) | 27/28 (96%) | 29/33 (88%) |
| Numbers in answer found in tool output | 33/34 (97%) | 27/27 (100%) | 2/2 (100%) |
| Latency p50 / p95 (s) | 6.4 / 8.2 | 6.3 / 9.1 | 4.0 / 7.5 |
| Errors | 0 | 0 | 0 |

### Router abstention by threshold (Held-out half, route confidence only)

| Threshold | In-scope abstained | Route correct when answered | Out-of-scope questions answered as in-scope |
|---|---|---|---|
| 0.5 | 1/17 (6%) | 15/16 (94%) | 0/2 (0%) |
| 0.6 | 1/17 (6%) | 15/16 (94%) | 0/2 (0%) |
| 0.7 | 3/17 (18%) | 14/14 (100%) | 0/2 (0%) |
| 0.8 | 5/17 (29%) | 12/12 (100%) | 0/2 (0%) |

### All 40

| Measure | A: qwen3 picks tools | B: nimble router | C: plain vector RAG |
|---|---|---|---|
| Questions run | 40 | 40 | 40 |
| Route or tool correct (in scope) | 31/36 (86%) | 33/36 (92%) | n/a |
| Abstained (in scope) | 0/36 (0%) | 4/36 (11%) | never |
| Route correct when it answered | 31/36 (86%) | 31/32 (97%) | n/a |
| Arguments correct (stats, compare, evidence) | 21/24 (88%) | 21/24 (88%) | n/a |
| Out-of-scope handled (no query / refusal) | 4/4 (100%) | 4/4 (100%) | 3/4 (75%) *heuristic |
| Count answers correct (stats + compare; compare check revised) | 14/17 (82%) | 12/17 (71%) | 0/17 (0%) |
| Compare answers correct, original strict check | 0/7 (0%) | 0/7 (0%) | 0/7 (0%) |
| Quotes found in the cited interview | 60/72 (83%) | 58/62 (94%) | 85/96 (89%) |
| Quotes found anywhere in the corpus | 66/72 (92%) | 59/62 (95%) | 85/96 (89%) |
| Numbers in answer found in tool output | 62/64 (97%) | 45/45 (100%) | 4/4 (100%) |
| Latency p50 / p95 (s) | 5.0 / 10.0 | 5.5 / 12.8 | 5.0 / 8.6 |
| Errors | 0 | 0 | 0 |

### Router abstention by threshold (All 40, route confidence only)

| Threshold | In-scope abstained | Route correct when answered | Out-of-scope questions answered as in-scope |
|---|---|---|---|
| 0.5 | 2/36 (6%) | 32/34 (94%) | 0/4 (0%) |
| 0.6 | 3/36 (8%) | 31/33 (94%) | 0/4 (0%) |
| 0.7 | 7/36 (19%) | 29/29 (100%) | 0/4 (0%) |
| 0.8 | 11/36 (31%) | 25/25 (100%) | 0/4 (0%) |

### Per-route latency (median s)

A {'compare_groups': 6.6, 'concept_stats': 4.2, 'evidence': 7.1, 'local_search': 7.8, 'out_of_scope': 1.1, 'theme_overview': 1.9}
B {'compare_groups': 6.3, 'concept_stats': 4.8, 'evidence': 7.8, 'local_search': 9.6, 'out_of_scope': 2.5, 'theme_overview': 2.7}
C {'compare_groups': 4.5, 'concept_stats': 5.3, 'evidence': 4.1, 'local_search': 7.0, 'out_of_scope': 3.2, 'theme_overview': 5.6}
