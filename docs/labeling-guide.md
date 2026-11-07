# Labelling guide (v3.2 sheets, about 2 hours)

> **Optional.** For the demo, human labelling is waived ([ADR-0013](decisions/0013-waive-human-labels.md)); the sheets in `data/labeling_v3/` currently hold **LLM labels** (backup of the blanks in `data/labeling_v3/blank_backup/`). This guide remains for anyone who wants a human check.

Goal: get an independent measure of extraction precision (Gate 1, target 0.80) and of how far `nimble` agrees with a person on attitude. **Your** judgement is the point; do not look at what any model thought first.

The sheets contain transcript text, so they live in **git-ignored `data/labeling_v3/`**. Do not copy them into the repo, issues or chat ([ADR-0012](decisions/0012-privacy-for-transcripts.md)).
The older v2 sheets in `data/labeling/` are superseded; ignore them.

## Files

| File | Rows | Time | You fill in |
|---|---|---|---|
| `data/labeling_v3/edges_to_label.csv` | 100 | about 90 min | the `label` column |
| `data/labeling_v3/attitude_to_label.csv` | 30 | about 30 min | the `label` column |
| `edges_key.csv`, `attitude_key.csv` | | | **Do not open until you finish.** They hold the group, an automatic check and `nimble`'s answer, which would bias you. |

## How to fill in the CSV

1. Open the CSV in Numbers, Excel, Google Sheets or a text editor. Add nothing, remove nothing, do not reorder rows, and do not change other columns.
2. Type one label per row into the `label` column, spelled **exactly** as below, lower case, no spaces. A misspelled label is reported as unrecognised and ignored.
3. Use `note` for anything odd (optional). Leave `label` blank if you truly cannot decide; the scorer skips blanks.
4. Save or export as **CSV (UTF-8)** to the **same path and filename**. Spreadsheet apps often offer "save as .xlsx" by default; that will not be read.
5. Work in a few sittings if you like; saved labels persist. Do not regenerate the sheets afterwards (that overwrites your labels).

## Sheet 1: edges

Each row is one thing a model extracted from one interview. Read the **quote** and the surrounding `participant_answer`, and the claimed **kind**, **status**, **polarity** and **name**. Then give the first label that applies, checking in this order:

| Order | Label | Use when | Invented example |
|---|---|---|---|
| 1 | `unsupported` | The quote does not support the name; or it is the interviewer's words; or it describes other people and the participant does not adopt it; or the name is about something else. | Name "tracking inventory", quote "my manager likes spreadsheets". |
| 2 | `wrong_polarity` | The participant says the opposite of what the row claims. The row is `affirmed` but they say they do **not** do or feel it, or the other way round. | Row: concern "job loss", affirmed; quote "I'm not worried about losing my job". |
| 3 | `wrong_status` | The row's status is wrong. Marked `current` but the quote is a wish, plan, prediction or "I would if...". Or marked `hypothetical`/`desired` but they actually do or feel it now. | Row: ai_use "summarising reports", current; quote "I'd love it to summarise my reports someday". |
| 4 | `wrong_kind` | Everything else is right but the kind is wrong. `work_task` = a piece of their own work, described without AI. `ai_use` = how they use, try or avoid AI. `concern` = a worry, frustration, distrust or limitation of AI that they state. | Row: work_task "generating ideas with the chatbot" (that is an ai_use). |
| 5 | `ok` | Supported by the quote, right speaker, right polarity, right status, right kind, and the name is a fair short description. | Row: ai_use "drafting emails", current, affirmed; quote "I use it to draft emails". |

Notes on judgement:

- Judge the **name against the quote and its context**, not whether you would have phrased it the same. A slightly vague name that is still fair is `ok`.
- A quote can look odd on its own but be fine in the surrounding answer; read `participant_answer` before deciding.
- `desired` and `hypothetical` rows are allowed. If the row says `desired` and the quote really is a wish, it is `ok`.
- If a row is wrong in two ways, use the first applicable label in the table order; you do not need to record both.
- When torn between `ok` and anything else, ask: would counting this name across interviews be misleading? If yes, do not use `ok`.

## Sheet 2: attitude (30 rows)

Read the answer (and the interviewer question above it) and label the **participant's attitude toward AI in that answer**:

| Label | Use when |
|---|---|
| `positive` | They say AI is helpful, good, satisfying or promising. |
| `negative` | They say AI is unhelpful, frustrating, untrustworthy or harmful. |
| `mixed` | They clearly say both good and bad things. |
| `none` | No evaluation of AI: consent, small talk, facts about their job, how they use it without judging it, or "none"/"no" to a question about concerns. |

Mild approval counts as `positive` only if they actually express it ("it's useful", "it helps"). A neutral description of use is `none`. Label the answer, not the whole interview.

## Score it

```bash
uv run --python 3.12 --with pandas python scripts/score_labels_v3.py
```

It reports precision with a 95% interval, error types (kind, status, polarity, unsupported), precision by kind, claimed status and group, whether the automatic grounding check predicts correctness, `nimble`'s agreement with you (confusion table, Cohen's kappa, split by confidence).

## Reading the result

| Result | What it means next |
|---|---|
| Precision at least 0.80 | Gate 1 passes: proceed to M3. |
| 0.60 to 0.80 | Look at the dominant error type. `wrong_kind` suggests merging kinds; `wrong_status` or `wrong_polarity` suggests the verify step must test them; `unsupported` suggests tightening grounding. Then proceed to M3 with that fix as its first task. |
| Under 0.60 | Take the fallback in [07](07-implementation-roadmap.md): reduce to `nimble` typed attributes and vector retrieval. |
| `nimble` agreement high at confidence 0.6 or above, low below | The confidence gate works. |
| Wide intervals | n=100 and n=30 give wide ranges; treat as directional. |

For context only (not a target): my own LLM labels on the **v2** output gave lenient precision 0.74 and `nimble` agreement 0.63 ([spike 01 addendum](spike-01-extraction.md)).
If your labels on v3.2 differ a lot from what the model flagged, that is the measurement; do not adjust toward the numbers above.
