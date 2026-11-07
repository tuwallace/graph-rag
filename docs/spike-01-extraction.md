# Spike 01: can local models build the graph from the transcripts?

Date: 2026-11-05. Machine: Apple M2 Pro, 32 GB. Server: Ollama 0.40.14. Scripts: `spike/01_profile.py` to `spike/04_analyze.py`, `spike/02b_extract_v2.py`
(outputs are in git-ignored `data/` because they contain transcript text).

Question from [ADR-0009](decisions/0009-corpus-anthropic-interviewer.md): are extraction speed, precision and `nimble` attribute quality good enough to commit to this corpus?

## Setup

- 20 transcripts, stratified: 10 `workforce`, 5 `creatives`, 5 `scientists` (pandas `sample(random_state=7)`).
- **Extraction**: `qwen3:8b-16k`, one call per whole transcript, JSON-schema output (`format=` with a schema), `think=False`, temperature 0, `num_ctx=16384`.
  Fields: `role_guess`, `overall_attitude_to_ai`, and lists of `tasks`, `ai_uses`, `concerns`, each item with a verbatim `quote`.
- **Grounding check**: normalised quote must be a substring of the transcript (v1) or of the `User` turns only (v2).
- **Decision model**: `nimble` via `/v1/systemone` on the 208 Q/A pairs from the same 20 transcripts, three typed questions per pair (`attitude` choice, `topic` choice, `job_worry` yes/no).

## Results

| Measure | Result | Notes |
|---|---|---|
| Valid JSON | 20 of 20 (both runs) | Schema-constrained output works |
| Extraction time | **31 s per transcript** mean (v1 30.7, v2 31.1; range about 17 to 50 s) | Scales with items extracted, not only input length |
| Projected full corpus | **about 10.8 hours** for 1,250 transcripts (naive extrapolation) | Serial; the GPU is shared with anything else loaded |
| Items per transcript | about 14 to 15 (v1 280, v2 289 over 20) | |
| Quote grounding | v1 90.4% (any text); v2 83.0% (`User` turns only) | v2 is stricter by design; see below |
| Prompt contamination (v1) | Items named exactly like my prompt examples: 25; about half of the 14 I read were wrong or weak | The model copied "losing skills" 13 times, "writing sales pitches" 6 times |
| Contamination after fix (v2) | None: no phrase repeated more than 3 times | Removed corpus-like examples from the prompt |
| Name vocabulary (v2) | tasks 123 items, 115 distinct; AI uses 95 and 93; concerns 71 and 71 | **Almost nothing repeats**, so counting needs normalisation |
| My read of 30 random v2 items | 4 clearly wrong, 5 weak, 21 sound | About 87% under a strict reading, about 70% if weak items count as errors. Single rater (me), n=30, so wide uncertainty |
| `nimble` calls | 208 segments, 0 errors | |
| `nimble` latency | **p50 2.4 s, p95 3.2 s, max 7.7 s** for three questions on one pair (inputs up to 2,937 tokens) | The blog's 91 ms was for a faster machine and presumably a lighter request; I did not isolate the cause |
| `nimble` projected | about 9.7 hours for 14,495 pairs with 3 questions | |
| `nimble` attitude confidence | mean 0.68; 37% of segments below 0.6 | The confidence gate will abstain often |
| `nimble` yes/no | returns a probability, not a boolean; 5 of 208 segments above 0.5 for "worried about job" | |
| `nimble` vs `qwen3` on overall attitude | 15 of 20 transcripts agree (75%); all 5 disagreements are adjacent labels (positive vs mixed, mixed vs negative) | **Not ground truth.** Compares two models, not a model to human labels |

## What went wrong, and what it teaches

1. **Prompt examples leak into the data.** Concrete examples in an extraction prompt become high-frequency fake entities. Use abstract instructions only, and check the top-10 names of
   any run against the prompt text. This would have silently corrupted every count.
2. **Grounding catches interviewer text, not all errors.** The v2 check flagged a quote taken from the interviewer's recap. It also flags near-verbatim quotes with whitespace or punctuation
   differences, so use a fuzzy token match (threshold to tune) instead of exact substring, and treat grounding as a floor, not as correctness.
3. **The main error class is hypotheticals typed as facts.** Wishes, predictions and "I would use it if..." statements were extracted as current tasks and uses
   ("storytelling innovation", "integrated assistant"). Add a required `status` field (`current | hypothetical | desired`) and filter on it.
4. **Category confusion.** The same phrase landed under `tasks` and `ai_uses`. Merging those two types, or adding a rule that each phrase goes in one list, would remove the duplicates.
5. **Names do not repeat.** 92 of 98 distinct task names in v1 were singletons. Without embedding-based merging, "how many people use AI for data analysis" returns tiny, misleading counts.

## Against the ADR-0009 thresholds

| Threshold set in ADR-0009 | Outcome |
|---|---|
| Extraction time per transcript measured | Done: 31 s, so about 10.8 h for everything |
| Precision on 100 hand-checked edges, fall back if under about 0.7 | **Partly done**: 30 edges, one rater, 0.87 strict and about 0.70 lenient. Borderline; needs your own labels on at least 100 edges |
| `nimble` agreement with your labels on 30 segments | **Not done**: no human labels exist yet. Only model-vs-model agreement (75%) |

## Verdict

**Go, with scope and prompt changes.** The corpus is workable, but the full run is expensive and precision is acceptable rather than strong.

1. Cut scope for the demo: all 250 `creatives` and `scientists` transcripts plus a 250-transcript random sample of `workforce` (500 total, about 4.3 h of extraction).
2. Fix the prompt (status field, one list per phrase, no examples), then rerun the same 20 before scaling.
3. Slim the `nimble` calls: run `topic` first and `attitude` / `job_worry` only on relevant topics, or test `tev1`; expect to cut the roughly 10 h projection by more than half (unmeasured).
4. Build the normalisation step and measure how many canonical nodes 500 transcripts produce before writing any aggregate tool.
5. You label 30 segments (attitude) and 100 edges (correct or not), so the two unfinished thresholds can be closed. A review file can be generated from `data/spike_review_sample.json`.

## Limits of this spike

n=20 transcripts, one run each at temperature 0, one human-ish rater (me, not independent), no inter-annotator agreement, no recall measurement (I never checked what was missed), and timings
from a single machine state. Nothing here is a benchmark.

## Addendum: provisional labels by Claude (2026-11-05), not a human result

At your request I labelled both sheets myself, blind to the key files (`data/labeling_claude/`, git-ignored; your blank sheets are untouched). I am an LLM and a single rater,
and I applied the guide strictly (a phrase filed under the wrong kind counts as `wrong`). Treat this as a second-opinion estimate that **does not close Gate 1**; human labels still should.

| Measure | Result (n, 95% interval) |
|---|---|
| Edge precision, strict (only `wrong` is an error) | 0.81 (100; 0.72 to 0.87) |
| Edge precision, lenient (`hypo` and `wrong` are errors) | 0.74 (100; 0.65 to 0.82) |
| Label mix | 74 ok, 7 hypo, 19 wrong |
| By kind (lenient) | AI use 0.83, concern 0.83, **task 0.61** |
| By group (lenient) | scientists 0.86, workforce 0.75, creatives 0.63 |
| Auto-grounded vs not | grounded 0.78, ungrounded 0.58: the grounding check is a useful but weak signal |
| `nimble` attitude vs my labels | 19 of 30 agree = 0.63 (0.46 to 0.78), Cohen kappa 0.46 |
| `nimble` agreement by confidence | at least 0.6: 16 of 22 = 0.73; under 0.6: 3 of 8 = 0.38 (small n) |

What the 19 wrong edges were (my own tally, approximate): about 10 phrases filed under the wrong kind (an AI use or AI behaviour filed as a task, such as "generating ideas", "logo generation",
"guitar tablature generation"); 5 where the name did not match the quote; 1 quote taken from the **interviewer** (edge 9); 2 about other people or the opposite polarity (edge 86 says the participant does *not* fear job loss);
1 a task that belongs to someone else. Only 7 were hypotheticals, fewer than the earlier 30-item read suggested.

Implications, before any human labels:

1. **Kind confusion is the largest fixable error.** Merging `tasks` and `ai_uses` into one list, or a rule that a task must be work done without AI, would remove most of it. If those 10 were forgiven, lenient precision would be about 0.84.
2. The status filter ([ADR-0010](decisions/0010-extraction-pipeline.md)) addresses fewer errors than planned (7 hypotheticals), so the verify step must also test **polarity** ("does the participant say they do or feel this?") and **speaker** (participant, not interviewer).
3. `nimble` over-assigns `positive`: 5 of my 11 `none` answers were called positive. Some of those are judgement calls (mild approval versus no attitude), so agreement is sensitive to the `none` boundary; define it more tightly or allow `neutral`.
4. The confidence gate has signal: agreement drops from 0.73 to 0.38 below 0.6, though only 8 segments fall below it.

Open: replace or confirm with human labels. If your labels differ from mine, the difference is itself a measurement of how subjective the task is.

## Addendum 2: v3.2 labels by Claude (2026-11-06), not a human result

At your request I filled in `data/labeling_v3/edges_to_label.csv` (100 edges) and `attitude_to_label.csv` (30 segments), blind to the key files, using the order in the [labelling guide](labeling-guide.md).
Each row's `note` says it was labelled by an LLM. Your blank originals are in `data/labeling_v3/blank_backup/`. I am a single rater and I also wrote the guide, so this is **not independent** and does not satisfy Gate 1 as a human check.

| Measure | Result (n, 95% interval) |
|---|---|
| Edge precision (`ok` / labelled) | **0.74** (100; 0.65 to 0.82), under the 0.80 target |
| Error types | unsupported 9, wrong_kind 8, wrong_status 7, wrong_polarity 2 |
| By kind | ai_use 0.81, work_task 0.67 (n=12), **concern 0.62** |
| By status the model claimed | current 0.78, desired 0.60 (n=10), hypothetical 0.58 (n=12) |
| By group | creatives 0.91, scientists 0.74, workforce 0.67 |
| Precision on `status=current` items | 0.78 (68 to 86) |
| Auto-grounded vs not | grounded 0.75 (n=97), ungrounded 0.33 (n=3: too few to conclude) |
| `nimble` attitude vs my labels | 19 of 30 = 0.63 (0.46 to 0.78), kappa 0.48 |
| `nimble` agreement by confidence | at least 0.6: 15 of 22 = 0.68; under 0.6: 4 of 8 = 0.50 (the earlier 0.73 vs 0.38 gap did not reappear) |

What the errors look like (my read):

- **unsupported (9):** the name does not match the quote. Examples of the pattern: a concern named "AI over-reliance" backed by a quote about the AI agreeing with the user's hypothesis; "AI inaccuracy" backed by a quote about the AI producing bloat; a quote taken from the interviewer's turn despite the speaker check, because the interviewer text had been echoed inside the participant's answer window; a fear attributed to the participant that they attribute to other people.
- **wrong_kind (8):** an AI use filed as a work task (for example generating unit tests, drafting emails), and attitudes or predictions filed as concerns.
- **wrong_status (7):** present-tense benefits labelled `desired`, "I'd love to have" labelled `hypothetical` instead of `desired`, and a current worry labelled `desired`.
- **Concerns are the weakest kind** (0.62): the model names a concern loosely, and the quote supports a nearby but different point.

Implications (Gate 1 band 0.60 to 0.80 in [07](07-implementation-roadmap.md)):

1. **Verify step first.** M3's `nimble` check should test "does this quote support this exact name?" This targets the largest group (unsupported) and part of wrong_kind.
2. Merge `hypothetical` and `desired` into one `not_current` status; the model confuses them and the difference is not needed for the graph.
3. Tighten the concern definition: the name must restate what the quote says, not a nearby theme.
4. `nimble` calls `positive` on 6 of my 12 `none` answers, matching the earlier finding. Define `none` more tightly or run attitude only on segments whose topic is an evaluation.

Open: a human re-label. If yours differs from mine, report both; the gap measures how subjective the rubric is.
