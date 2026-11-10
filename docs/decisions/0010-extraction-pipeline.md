# ADR-0010: Extraction pipeline for the transcripts

- Status: accepted 2026-11-10 by the project owner (earlier: proposed (supersedes [ADR-0002](0002-graph-construction.md) for this corpus))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Extraction output is a rebuildable artefact keyed by `run_id`, `model` and `prompt_version`.

## Owner decision (2026-11-10)

The precision target (about 0.80 with verify) is accepted as met on the larger-model measurement (78% correct, 90% counting hypothetical, 90 kept edges; see docs/07). The corpus scope is final at 500 interviews.

## Context

[Spike 01](../spike-01-extraction.md) measured: 31 s per transcript with `qwen3:8b-16k` (about 10.8 h for 1,250), valid JSON 20 of 20, quote grounding 83% against `User` turns,
roughly 0.87 strict (0.70 lenient) precision on 30 items read by one rater, prompt examples copied into results, hypotheticals extracted as facts, and almost no repeated names (115 distinct of 123 task items).
`nimble` runs at p50 2.4 s for three questions per segment.

## Decision drivers

- Precision before recall (wrong edges corrupt counts)
- Auditability (every edge traceable to a quote)
- Local runtime within a day on one Mac
- Counting needs canonical entities

## Options

1. A. One `qwen3:8b-16k` call per transcript (spike setup)
2. B. One call per segment (Q/A pair), `qwen3:8b-16k`
3. C. Per-transcript extraction (A) plus a verification pass: a `nimble` yes/no question per extracted item ("does this quote show the participant currently does X?") to drop hypotheticals and misfiles
4. D. `qwen2.5:32b` per transcript

## Weighted decision matrix

| Criterion | Weight | A. Per transcript | B. Per segment | C. A + verify | D. 32b |
|---|---|---|---|---|---|
| Precision | 35 | 3 | 4 | 4 | 4 |
| Runtime on this Mac | 25 | 4 | 2 | 3 | 1 |
| Auditability | 20 | 4 | 5 | 5 | 4 |
| Simplicity | 10 | 5 | 3 | 3 | 4 |
| Cost of a re-run | 10 | 3 | 1 | 2 | 1 |
| **Weighted score (out of 5)** | 100 | **3.65** | 3.30 | **3.65** | 2.95 |

The scores for B, C and D are **estimates**, not measured. A and C tie; the tie-break is that C addresses the measured main error class (hypotheticals) with a cheap, calibrated check, while A does not.

## Decision

Use **C** at demo scope (500 transcripts, see below), staged:

1. **Parse** into segments; keep `User` text per segment for grounding.
2. **Extract** with `qwen3:8b-16k`: one list of items, each with a required `kind` (`work_task | ai_use | concern`), `status` (`current | hypothetical | desired`) and `polarity` (`affirmed | negated`), no corpus-like examples and no item-count hint in the prompt, quotes at most 25 words, a schema item cap of 25, a token cap, and de-duplication (implemented and measured in M2, prompt `v3.2`; see the [M2 outcome](../07-implementation-roadmap.md)).
3. **Ground**: fuzzy token match against the segment's `User` text; drop failures and count them.
4. **Verify**: `nimble` yes/no on `(quote, name)`; keep items above a threshold tuned on your labels. Test **polarity** (does the participant say they do or feel this?) and **speaker** as well as current/hypothetical, since labelled errors included an interviewer quote and a negated claim; M2 now handles the speaker (grounding) and gives a first polarity/status signal, so the verify step is a second opinion.
5. **Normalise**: embed names with `nomic-embed-text`, cluster, sample-review, write canonical keys and aliases.
6. **Prompt hygiene check**: after every run, compare the top 10 extracted names against the prompt text and fail the run if any match.

Scope: all `creatives` (125), all `scientists` (125) and a fixed random 250 of `workforce`.

## Consequences

- Good: addresses each defect found in the spike; every edge stays auditable; runtime about 4.3 h for extraction plus the verify pass (unmeasured).
- Costs: more stages, a threshold to tune, and a human labelling step.
- Risk: normalisation merges distinct concepts. Mitigation: review a sample, keep aliases, never delete raw names.

## Confirmation

Rerun the same 20 transcripts with the new prompt. Original criterion: precision at least 0.80 on 100 human-labelled edges with the verify step, grounding at least 90% (fuzzy), no prompt-hygiene failure. **Amended 2026-11-06 ([ADR-0013](0013-waive-human-labels.md)):** human labels are waived for the demo. Grounding (97.1%) and hygiene (none) were met in M2; precision is LLM-estimated at 0.74 before the verify step, and M3 reports the verify step's effect on that estimate.

## Revisit when

Precision stays under 0.7 after the changes. Then reduce the graph to `nimble` typed attributes only, or test a larger extractor offline on a sample.

## M3 amendments (2026-11-06)

Measured while building the pipeline ([M3 outcome](../07-implementation-roadmap.md)); human labels are waived ([ADR-0013](0013-waive-human-labels.md)).

- **Status merged** to `current | not_current` (prompt `v3.3`): the model confused `hypothetical` and `desired`, and the graph does not need the difference.
- **Verify step calibrated** on the 100 LLM-labelled edges: `supports` (AUC 0.65) separates `unsupported` items well (mean 0.17 vs 0.62 for `ok`) but not wrong status (0.71) or wrong kind (0.50); `own_current` is weak (AUC 0.60) and is stored, not used.
  A cut at `supports >= 0.2` removes 8 of 9 unsupported items, 2 of 8 wrong-kind, 1 of 2 wrong-polarity and 0 of 7 wrong-status, at the cost of 13 of 74 good items. Precision rises from 0.74 to 0.80 (bootstrap interval for the lift +0.01 to +0.12).
  The threshold was chosen on the same data, so this is optimistic. Residual errors are mainly wrong status and wrong kind.
- **Attributes simplified** to one `nimble` attitude call per segment (1.66 s cold); topic gating and the job-worry question were dropped ([ADR-0008](0008-decision-model-router.md)).
- **Normalisation**: embed names with the word "ai" removed, cluster per kind at cosine 0.85 (a sweep on 306 names gave 241 canonical names, 21% merged; without "ai" removal one catch-all cluster absorbed 22 unrelated names). I eyeballed about 14 merges per setting and found most sensible; this is not a measured merge precision.
