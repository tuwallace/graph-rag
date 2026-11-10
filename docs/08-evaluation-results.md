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

## Re-run on the final graph (2026-11-10)

The M7 evaluation above was run on the graph before the concern pass. It was re-run on the final graph (concern pass applied at verify 0.6, 1,861 concern edges, 12 themes, router v3) with the same 40 questions, the same scorer and one run per config. The previous outputs are kept in `data/eval/pre-concern-pass/`. 500 of the 1,250 interviews; one author's questions; one run each, so gaps of one or two questions are noise.

### All 40, final graph

| Measure | A: qwen3 picks tools | B: nimble router | C: plain vector RAG |
|---|---|---|---|
| Questions run | 40 | 40 | 40 |
| Route or tool correct (in scope) | 31/36 (86%) | 34/36 (94%) | n/a |
| Abstained (in scope) | 0/36 (0%) | 2/36 (6%) | never |
| Route correct when it answered | 31/36 (86%) | 32/34 (94%) | n/a |
| Arguments correct (stats, compare, evidence) | 21/24 (88%) | 23/24 (96%) | n/a |
| Out-of-scope handled (no query / refusal) | 4/4 (100%) | 4/4 (100%) | 3/4 (75%) *heuristic |
| Count answers correct (stats + compare; compare check revised) | 14/17 (82%) | 13/17 (76%) | 0/17 (0%) |
| Compare answers correct, original strict check | 1/7 (14%) | 0/7 (0%) | 0/7 (0%) |
| Quotes found in the cited interview | 48/80 (60%) | 58/102 (57%) | 88/98 (90%) |
| Quotes found anywhere in the corpus | 60/80 (75%) | 65/102 (64%) | 88/98 (90%) |
| Numbers in answer found in tool output | 67/78 (86%) | 69/69 (100%) | 4/4 (100%) |
| Latency p50 / p95 (s) | 5.5 / 14.5 | 6.6 / 21.2 | 5.0 / 8.7 |
| Errors | 0 | 0 | 0 |

### Per-route end-to-end latency (median s), final graph

A {'compare_groups': 6.4, 'concept_stats': 4.2, 'evidence': 7.2, 'local_search': 7.7, 'out_of_scope': 1.1, 'theme_overview': 10.1}
B {'compare_groups': 6.6, 'concept_stats': 5.5, 'evidence': 8.1, 'local_search': 10.5, 'out_of_scope': 3.0, 'theme_overview': 24.5}
C {'compare_groups': 4.4, 'concept_stats': 5.4, 'evidence': 5.0, 'local_search': 7.0, 'out_of_scope': 3.2, 'theme_overview': 5.6}

### What changed against the first run (all 40)

| Measure | First run, B | Final graph, B | First run, A | Final graph, A |
|---|---|---|---|---|
| Route correct (in scope) | 33/36 | 34/36 | 31/36 | 31/36 |
| Arguments correct | 21/24 | 23/24 | 21/24 | 21/24 |
| Quotes found in the cited interview | 58/62 (94%) | 58/102 (57%) | 60/72 (83%) | 48/80 (60%) |
| Numbers found in tool output | 45/45 | 69/69 | 62/64 | 67/78 (86%) |
| Latency p50 / p95 (s) | 5.5 / 12.8 | 6.6 / 21.2 | 5.0 / 10.0 | 5.5 / 14.5 |

**Quote validity fell, mostly for scoring reasons, not fabricated quotes.** The scorer takes any double-quoted span of four or more words as a quote. In this run the model (a) quoted whole theme summaries and wrapped each paragraph in double quotes on the four `theme_overview` questions (30 spans, none an interview quote), and (b) on q31 (evidence) wrapped each paragraph in double quotes around correct single-quoted verbatim quotes (5 spans, all inner quotes are in the tool output). Excluding those 35 spans, B scores 58 of 67 (87%), still below the first run's 94%, so some real drop remains (q05, q23). I did not change the scorer after seeing the result. The production path (`ask_interviews` with `grounded.py`) is the check that matters and is below.

**`theme_overview` latency in config B regressed:** median 24.5 s against 2.7 s in the first run (plain RAG 5.6 s). The answers now restate every stored theme summary and are much longer; I have not investigated why they changed (the themes were rebuilt and router v3 is in use). It affects 4 questions, so treat it as a lead, not a measurement.

### Groundedness on the final graph (60 questions, `eval/grounded_eval.py`, router v3)

| Measure | First run (graph before the pass, router v2) | Final graph (router v3) |
|---|---|---|
| Questions that went through the model | 51 of 60 | 52 of 60 |
| Fell back to the rendered facts | 2 of 51 (4%) | 6 of 52 (12%) |
| Quotes found in the cited interview, raw model text | 89/92 (97%) | 97/107 (91%) |
| Quotes found in the cited interview, text delivered | 90/90 (100%) | **98/98 (100%)** |
| Stats answers matching the database | 15/15 | 15/15 |
| Median time per question | 7.6 s | 6.7 s |

Fallback reasons: quote not in tool output 10, figures not in tool output 2, quote source not cited 1 (routes: `concept_stats` 4, `evidence` 1, `theme_overview` 1). The validator caught every invalid quote again, so the delivered text is 100% grounded in the tool output, but the model needs the fallback three times as often as before.

## Live `ollmcp` session on the final graph (2026-11-10)

`scripts/live_ollmcp_session.py` ran one real session: `ollmcp` with `qwen3:8b-16k` (thinking on, its default), the routed profile (`mcp.json`, one tool `ask_interviews`), five fixed questions typed in order, each tool call confirmed with "y". One run; I read the answers against the tool output by hand and with a quote-containment check.

| Question | Route (confidence) | Tool calls | Time | Check against the tool output |
|---|---|---|---|---|
| Main themes across the interviews | theme_overview (0.99) | 1 | 65 s | Themes, counts and concerns match the stored summaries; adds a "Key Takeaways" section |
| Top concerns among scientists | concept_stats (0.92) | 1 | 72 s | Concepts and percentages match; adds interpretation |
| Compare scientists and creatives on hallucinations | compare_groups (0.97) | 1 | 57 s | 4 of 4 quotes verbatim and the counts are right, but it says scientists are "2x more likely" than creatives (11.2% vs 0%), which is wrong (a ratio against 0% is undefined) and adds a "Why the Difference?" explanation the data does not give |
| Show quotes about losing skills | evidence (0.92) | 1 | 51 s | 5 quotes, all from the tool output; 2 of them with editorial insertions in square brackets ("[AI tools]", "[to AI]") and one with changed capitalisation |
| What is 2+2? | none | 0 | 12 s | The model answered "4" itself and never called the tool, so the `out_of_scope` route was not exercised |

**What it shows.** The wiring works end to end: `ollmcp` lists the tool, the router picks the right route with high confidence on four of four in-scope questions, each answer rests on the stored data, and the quotes are real. But in this path `qwen3` writes the final text, so **the guarantees of `grounded.py` (validated quotes, no unsupported figures) do not apply**: the model added a false "2x" and unsupported explanations, lightly edited two quotes, and answered an out-of-scope question from its own knowledge. Latency is 51 to 72 s per in-scope question with thinking on, against about 7 s through the grounded path in the evaluation. Fixing this is a decision: for example return the grounded text from the server with an instruction to relay it unchanged, or turn thinking off in `ollmcp`.

### Fix attempt and re-test (2026-11-10)

Change: `ask_interviews` now returns the validated facts in an `answer` field plus an `instruction`, and the server instructions tell the client to call the tool for every message (also unrelated ones), pass the message word for word, relay `answer` unchanged, and never invent quotes. `tests` and `scripts/mcp_smoke.py` pass; the out-of-scope route now returns its refusal through the tool. The same five questions were then run through `ollmcp` several times (`scripts/live_ollmcp_session.py`; one run per row; a quote counts as valid only if it appears in that answer's tool output).

| Run | Thinking | Context cleared before each question | In-scope questions where the tool was called | Quotes in answers found in tool output | Notes |
|---|---|---|---|---|---|
| 1 (before the fix) | on | no | 4/4 | 8/8 in the checked answers, 2 with bracketed edits | false "2x", added explanations, 2+2 answered by the model |
| 2 | on | no | 3/4 | 4/11 | skipped the tool on the quotes question and **invented seven quotes with made-up interview ids** |
| 3 | off | no | 4/4 | 4/4 | clean relay; the model shortened the last query, so the router asked for clarification; 2+2 refused through the tool |
| 4 | off | no | 1/4 | 0/9 | skipped the tool for three questions and invented quotes |
| 5 | off | no | 2/4 | 0/9 | skipped the tool for two questions and invented quotes |
| 6 | off | yes | 4/4 | 9/9 | all figures in the tool output, no added sections; 2+2 answered by the model |
| 7 | off | yes | 4/4 | 9/9 | same as run 6 |

**Result.** With thinking off and the conversation cleared before each question (`/tm`, `/cc` in `ollmcp`) the relay is faithful in two of two runs: the tool is called every time, quotes are verbatim, no unsupported figures or added sections. Without that, `qwen3:8b-16k` skipped the tool in a long conversation in 3 of 5 runs and wrote quotes with invented ids. **The server cannot enforce this:** the client model decides whether to call the tool and what to say. Treat free-form `ollmcp` chat with this model as unvalidated; the validated path is `grounded.py` and the evaluation harness. Out-of-scope questions are sometimes answered by the model itself without the tool (runs 6 and 7: "4"). Latency with thinking off and context cleared: 24 to 59 s per in-scope question (51 to 105 s with thinking on), still far above the 7 s of the grounded path because the client model has to read and rewrite long tool output. Small n (7 runs of 5 questions), one model.
