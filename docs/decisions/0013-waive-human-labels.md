# ADR-0013: Proceed without human labels for the demo

- Status: accepted by twallace on 2026-11-06
- Date: 2026-11-06
- Deciders: twallace
- Reversibility: Easy. The blank human sheets are kept in `data/labeling_v3/blank_backup/` and the scorer still works on them.

## Context

[ADR-0010](0010-extraction-pipeline.md) set a Gate 1: edge precision of at least 0.80 on 100 human-labelled edges, plus `nimble` agreement on 30 segments. Nobody has labelled the sheets.
At your request I labelled them as an LLM ([spike 01, addendum 2](../spike-01-extraction.md)): edge precision **0.74** (95% interval 0.65 to 0.82), `nimble` attitude agreement **0.63** (kappa 0.48).
That is a single rater, I also wrote the rubric, and the interval is wide. It falls in the 0.60 to 0.80 band the roadmap said to handle by fixing the dominant error type and continuing.

## Decision

Proceed to M3 and beyond **without human labels**, as a demo. Gate 1 is **waived, not passed**: the target of 0.80 was not met on any measurement.

What replaces it:

1. Treat 0.74 as the working estimate and say so wherever precision is mentioned (README, results).
2. Fix the dominant errors in code before scaling (M3): a `nimble` verify step ("does this quote support this exact name?"), merged `hypothetical`/`desired` status, a tighter concern-naming rule.
3. Measure the verify step against the LLM-labelled sheet (a calibration, not a validation) and report the precision/recall trade-off.
4. Keep provenance on every edge (quote, model, prompt version, verify score) so any count can be audited by reading the quotes.
5. Evaluation (M7) uses questions whose answers are computed from the database and checked against quotes, plus spot checks; there is **no independent human ground truth**, and results must carry that caveat.

## Consequences

- Good: the demo is not blocked on a 2 hour task.
- Costs: precision and `nimble` agreement are LLM-estimated; any aggregate count (such as "N interviews mention X") has an unmeasured error of roughly a quarter.
- Risk: presenting counts as findings. Mitigation: answer rules already say these are findings from a sample of AI-led interviews; add "estimated, not human-verified" to count outputs.

## Confirmation

The verify step's calibration on the labelled sheet (M3) shows a precision gain at an acceptable recall cost, and the published README states the 0.74 estimate and its source.

## Revisit when

Anyone fills in the human sheets (see [labelling guide](../labeling-guide.md)): run `scripts/score_labels_v3.py` and compare with the LLM labels; supersede this record if the human precision is under 0.60.
