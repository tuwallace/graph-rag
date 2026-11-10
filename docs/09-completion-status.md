# 09. Completion status (2026-11-10, updated after the owner's decisions and Test 1)

What is done, what is open, and what still needs a decision or a test before the project is marked complete. All results describe the **500-interview** graph (500 of the 1,250 interviews in the dataset). Model-judged means judged by `qwen2.5:32b`; the owner has stated they confirmed the labels (see [08](08-evaluation-results.md)).

## Done

| Area | State |
|---|---|
| Build M0 to M9 | Done; published at tuwallace/graph-rag (commit history on `main`) |
| Graph | 500 interviews, 5,450 segments; 600 task, 3,020 AI-use and 1,861 concern edges; 12 validated themes |
| Router and tools | Router v3, MCP server, typed tools; 34/36 on the original 40, 18/18 on the confirmation 20, 30/40 on a fresh 48-question set (config A: 23/40) |
| Grounded answers | Quotes delivered to the user 90/90 valid on 60 questions (older graph) |
| Concern recall pass | Applied at verify 0.6; fresh sample 76% correct; concern coverage 22% to 42% on 10 transcripts |
| Privacy and publishing | Pre-push check, gitleaks, no data in git; clean clone installs and passes the 42 tests |
| Licence | MIT, owner decision 2026-11-09 |

## Targets in 06 against the evidence

| Target | Result | Verdict |
|---|---|---|
| Extraction precision at least 0.80 with verify | Larger model, 90 kept edges: 78% correct, 90% counting hypothetical; concerns 63% | **Borderline: not met on the strict reading** |
| Grounding at least 90% | Kept edges re-grounded at load: 0 ungrounded of 5,503 kept edges | Met for kept edges |
| Prompt hygiene, zero failures | 0 on the main extraction | **Not run on the loose concern prompt** |
| Retrieval recall at 5 at least 0.7 | Passed on a proxy query set | **Owner's own 10 queries not done (waived)** |
| Quotes exist and belong to the cited interview | 100% after the validator, on 60 questions | Met on the final graph: 98/98 delivered (raw model text 91%; fallback 12%) |
| Number groundedness | 0 flagged figures on 60 questions (first run) | Met in the first run; the final-graph run flagged 2 answers for figures and replaced them |
| Router vs plain RAG | Reported in 08, re-run on the final graph | Done |
| Latency p50 and p95 per route | Router decision p95 1.98 s (bound 2 s); end-to-end per route re-run | `theme_overview` in config B regressed to 24.5 s median (lead, not investigated) |

## Decided by the owner (2026-11-10)

All ADRs accepted; precision target met; Gates G1 and G2 stay closed; router v3 kept (p95 under 2 s); scope final at 500 interviews; the 22 kept edges with no single segment (0.4%) are skipped at load and that stays.

## Open: needs your decision (superseded by the section above; kept for the record)

1. **ADR statuses.** ADR-0001, 0004, 0005, 0006, 0010, 0011 and 0012 are still "proposed". Decide accept, amend or supersede each; ADR-0010 carries the precision target above.
2. **Precision target.** Accept 78% strict (90% lenient) as meeting "about 0.80", or require a better extractor or a stricter verify.
3. **Gates G1 and G2.** Both were waived or passed on a proxy ([ADR-0013](decisions/0013-waive-human-labels.md)). Confirm they stay closed on those terms.
4. **Router latency.** p95 of 1.98 s leaves almost no margin to 2 s. Keep v3 (your earlier decision) or trim the examples.
5. **Scope.** 500 of 1,250 interviews. Declare 500 final, or schedule the remaining 750 (roughly 15 to 20 h of extraction, verify and attributes at the measured rates).

## Open: tests not yet run (after Test 1)

1. ~~Re-run the end-to-end evaluation on the final graph~~ **Done 2026-11-10** (M7 table, groundedness, end-to-end latency per route; see 08).
2. ~~Hygiene check on the concern-loose prompt~~ **Done:** 2 of 500 transcripts flagged ("human connection", a phrase in the prompt; 31 raw items, none kept in the graph).
3. ~~Live session check~~ **Done 2026-11-10** (see 08): routes and tool use work; the model's final text is not validated (a false "2x", unsupported explanations, edited quotes, an out-of-scope answer given without the tool), and each answer takes 51 to 72 s with thinking on.
4. **PII residuals** listed in ADR-0012: first names alone, lowercase employers, phone formats.
5. **Run-to-run stability:** every result is one run; the larger-model judge was run once per item.
6. **Normalisation error rate:** merge errors and missed merges on a sample, as the plan in 06 asks; the new concern names were merged by the same 0.85 threshold without a sample review.
7. **Attitude labels:** agreement was 0.63 in M3 and no calibration curve was reported.

## Housekeeping

- Doc 06 still reads as a plan ("optional", "waived") in places; align it with what happened.
- Refresh the graphify map after the final doc edits.
- 22 kept edges (0.4%) have no single segment for their quote and are skipped at load; decide whether that is acceptable.
- `docs/decisions/README.md` and `docs/README.md` list ADR-0008 as "proposed"; the ADR itself says accepted.
