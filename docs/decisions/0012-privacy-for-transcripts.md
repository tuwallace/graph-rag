# ADR-0012: Privacy, licensing and public-repo rules for the transcript corpus

- Status: proposed (supersedes [ADR-0007](0007-privacy-and-access.md))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Moderate. A leaked file in public git history is hard to retract.

## Context

The repository is public. The corpus is raw interview transcripts about people's work. The dataset card states participants consented to public release and describes no anonymisation;
its license text is inconsistent (front matter `mit`, body "data CC-BY, code MIT"). A regex scan found no emails or phone numbers and 3 URLs; names and employers were not scanned.
Neo4j Community 5.26.32 has users but no roles (verified in M1: `CREATE ROLE`/`GRANT ROLE` are unsupported), so there is no database-level read-only role. A write in a `READ`-mode session is rejected by the server.

## Decision

1. **Do not commit** the dataset, extracted JSON, spike outputs, Neo4j data or any file containing transcript text. `.gitignore` covers `data/`; setup downloads the dataset. Check `git status` before every push.
2. **Quotes are data.** Extracted quotes may appear in local answers. Do not paste long quotes (more than a sentence) into the README, docs or screenshots; short attributed excerpts only.
3. **Attribution**: README credits Anthropic and links the dataset and the associated research post; state the CC-BY reading and the inconsistent card.
4. **Do a PII pass** before showing outputs publicly: scan for capitalised name patterns, employers and URLs; record what was checked and what was not.
5. **Describe the sample honestly**: results describe these interviews, not workers in general; the interviewer is an AI and the sample is self-selected.
6. **Read mode** on every query session; the MCP server exposes no write tool. This is an application-level guarantee in Community edition.
7. **Typed tools only** by default; a gated text-to-Cypher path (if ever added) rejects writes and allowlists procedures.
8. **Secrets** in `.env` (git-ignored), never in `mcp.json` or compose files; all published ports bound to `127.0.0.1`.
9. **Prompt injection**: transcripts are untrusted text. The extraction prompt treats them as data, output is schema-constrained, and answer tools return short quotes, never instructions.

## Consequences

- Good: nothing sensitive reaches git; the demo stays reproducible by download.
- Costs: the public repo cannot include sample outputs with real quotes; screenshots need review.
- Risk: accidental commit. Mitigation: `.gitignore` now, a secret/data check in CI when the repo gets one.

## Confirmation

A pre-push check lists tracked files and fails on any path under `data/` or file over a size limit.

## Revisit when

The dataset card is corrected, or a larger PII scan finds identifying details.

## PII pass record (2026-11-07, before the first public commit)

Checked over every file to be committed (docs, code, graphify map and wiki; 150 or so files): email addresses (none), URLs (domains only huggingface.co, ollama.com, github.com, anthropic.com, astral.sh and localhost), and capitalised multi-word names that also occur in participant turns of the 1,250 transcripts (one overlap, "Google Sheets", a product). `scripts/prepush_check.py` additionally fails on any run of 25 or more words shared with the corpus. Not checked: single first names, employers named in lowercase, phone-number formats, and anything in the data itself (the corpus is not redistributed). Quotes in docs are short attributed excerpts.

Update 2026-11-09: the owner decided to stay with MIT (code and data), following the card's front matter. Attribution is unchanged.
