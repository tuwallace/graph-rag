# ADR-0007: Privacy and access control

- Status: superseded by [ADR-0012](0012-privacy-for-transcripts.md) (written for helpdesk comments and the first-name issue)
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Moderate. Loading internal comments later means a schema change and re-review of every tool's output.

## Context

- helpdesk-rag already enforces "public comments only: internal notes must never reach an end-user answer". The graph must not weaken that.
- In the sample, 557 of 2,000 comments are internal, and the 24 distinct bodies appear in both visibilities ([F4](../01-data-analysis.md)), so the flag carries no content signal here, but the rule is the point.
- Ticket descriptions end with "Reported by <first name> from <dept>" (355 distinct first names, many collisions). Synthetic, but a real system would hold real names.
- Neo4j Community has one database and no fine-grained RBAC, so a database-enforced read-only role is not available (verify against the pinned version).
- The repo may be public; helpdesk-rag's rules forbid home paths, usernames, emails or keys in tracked files.

## Decision drivers

- Leak safety first
- Analytical value
- Simplicity
- Auditability

## Options for internal comments

1. **Do not load internal comments into the graph**
2. Load with a `visibility` property and filter in every query
3. Load into a separate labelled subgraph (`:InternalNote`) that no tool queries

## Weighted decision matrix

| Criterion | Weight | 1. Do not load | 2. Filter in queries | 3. Separate subgraph |
|---|---|---|---|---|
| Leak safety (fails closed) | 40 | 5 | 2 | 4 |
| Analytical value | 20 | 2 | 4 | 4 |
| Simplicity | 20 | 5 | 3 | 2 |
| Auditability | 20 | 3 | 4 | 4 |
| **Weighted score (out of 5)** | 100 | **4.00** | 3.00 | 3.60 |

Option 2 fails open: one forgotten `WHERE` leaks. Option 1 fails closed.

## Decision

1. **Internal comments are not loaded.** The graph holds public comments only (as `Action` nodes via `HAD_ACTION`).
2. **No `Reporter`/`Person` node**, and the "Reported by ..." text is never stored in the graph or returned by a tool.
3. **Read mode on every query session** (`default_access_mode=READ`); the MCP server exposes no write tool. Because Community has no read-only role, this is an application-layer guarantee, and the
   MCP server uses a separate code path from the loader.
4. **Typed tools only** by default (ADR-0004), so there is no model-authored Cypher. If the gated fallback is enabled later, it additionally rejects writes and `CALL` outside an allowlist, and enforces `LIMIT` and a timeout.
5. **Secrets**: `NEO4J_PASSWORD` in `.env` (git-ignored). Not in `mcp.json`, compose files or logs. Provide `.env.example`.
6. **Network**: all published ports bound to `127.0.0.1`.
7. **Public repo hygiene**: no absolute home paths in tracked files (the `mcp.json` uses relative paths); data files stay git-ignored; keep the CC-BY-NC-4.0 attribution and non-commercial notice from helpdesk-rag for any derived files.
8. **Prompt-injection note**: ticket text is untrusted. Tools return only fields the design lists (counts, action text from the 24-value set, ticket IDs), not raw descriptions, which shrinks the injection surface. Free-text fields are re-introduced only with a sanitising step.

## Consequences

- Good: fails closed; simple to reason about; small injection surface.
- Costs: no analysis of internal notes; the loader and the server must stay separate (different credentials not possible in Community, so separate code paths).
- Risk: someone adds a tool that concatenates raw ticket text. Mitigation: a test asserting no tool output contains "Reported by", and a code-review checklist item.

## Confirmation

Tests: (a) load a fixture containing internal comments and assert zero `Action` nodes derive from them; (b) a scan of every tool's output on the eval questions finds no "Reported by" and no internal text;
(c) a write attempt through the server's query path fails (READ mode).

## Revisit when

Real data arrives (re-run a privacy review), the pinned Neo4j supports a read-only role in your edition, or an analyst use case needs internal notes (then option 3 with an explicit, separate tool and access decision).
