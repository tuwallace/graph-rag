# 01. Data analysis: what a graph can honestly add

Source: `helpdesk-rag/data/raw/data/*.csv`, the free sample of
[mindweave/help-desk-tickets](https://huggingface.co/datasets/mindweave/help-desk-tickets) (synthetic, CC-BY-NC-4.0, non-commercial).
All numbers below were measured on the files, not copied from the dataset card.

## Tables

| Table | Rows (sample) | Key columns |
|---|---|---|
| `tickets` | 1,000 | `ticket_id`, `created_at`, `first_response_at`, `resolved_at`, `priority` (P1-P4), `status`, `channel`, `category_id`, `assigned_agent_id`, `requester_department`, `affected_service`, `summary`, `description`, `escalated`, `outage_related` |
| `comments` | 2,000 | `comment_id`, `ticket_id`, `agent_id`, `created_at`, `visibility` (public/internal), `team`, `body` |
| `agents` | 10 | `id`, `name`, `team` |
| `categories` | 8 | `id`, `name`, `service` |
| `sla_breaches` | 1,249 | `breach_id`, `ticket_id`, `breach_type`, `sla_target_hours`, `actual_hours`, `breach_minutes` |

The full set has 10,000 tickets. `sla_breaches.csv` ships with the sample but is built for the full set.

## Findings that drive the design

| # | Finding | Consequence |
|---|---|---|
| F1 | Only **56 distinct `summary` values** across 1,000 tickets (about 18 tickets each). Descriptions are the summary plus "Reported by <first name> from <dept>". | The natural hub is a **Problem** node keyed by summary. Free-text entity extraction would find nothing the columns do not already give. |
| F2 | **Every one of the 56 summaries maps to more than one `category_id`** (56 of 56). Category and `affected_service` are effectively random per ticket. | Do **not** build `Problem -> Category` as a fact. Keep category on the Ticket and report distributions ("seen under 5 categories"), never "the category is X". |
| F3 | Comments have only **24 distinct bodies** (for example "Found stale token in local credential manager."). 878 of 1,000 tickets have at least one. | Model comments as **Action** nodes (24), shared across tickets. This gives the graph its one piece of real signal the vector index lacks: *which actions were taken on which problems*. The current system says tickets hold "NO fix steps"; actions are the closest thing. |
| F4 | `visibility` is split 1,443 public / 557 internal, and the **same 24 bodies appear in both**. | Internal vs public is not a content signal here, but the privacy rule still holds: internal comments must never reach an end-user answer. See [ADR-0007](decisions/0007-privacy-and-access.md). |
| F5 | **101 of 1,249** `sla_breaches` rows match a ticket in the 1,000-ticket sample. The rest reference tickets 1,001+ that are not present. All rows are `breach_type = resolution`. | Load only matching rows in the sample; warn on orphans. SLA questions are only meaningful on the full 10k set. |
| F6 | `Reported by <name>` yields **355 distinct first names** with heavy collisions (John 19, Christopher 17). | **No Reporter/Person node.** First names are not identities, and modelling them invents false merges. Strip or ignore. |
| F7 | `outage_related` is `False` for all 1,000 sample tickets. The card says month 6 has a 5x outage spike in the full set. | Keep the property; temporal and outage queries need the full data to test. |
| F8 | Time-to-resolve is derivable (`resolved_at - created_at`); 794 resolved + 105 closed, 101 open (in_progress/pending). | Store `hours_to_resolve` on Ticket. |
| F9 | The existing README caveat: metrics on 56 problems are directional, golden set is n=19 in-scope. | Any graph-vs-baseline claim needs a **new graph-shaped question set**, see [06](06-evaluation-and-roadmap.md). |

## What this means

**The graph will not improve semantic recall.** Retrieval over 56 near-templated problems is already at hit@5 0.95 (rerank-only).
Microsoft-style GraphRAG (LLM-extracted entities, community summaries) targets large unstructured corpora; this corpus is small and
already structured. Using it here would add cost for no signal.

**Where a graph does help**, and where the current pipeline is weak (the README names them: "any P1 outages last month?", aggregates, text-to-SQL):

1. **Aggregation and relationship questions.** "Which problems are escalated most?", "who resolves VPN tickets fastest?", "which problems share the same actions?"
2. **Multi-hop explanation.** Problem -> actions taken -> agents/teams -> SLA breaches, returned as evidence with ticket IDs.
3. **Neighbourhood expansion.** Retrieve a problem by meaning, then add "related problems" via shared actions, services and agents.
4. **Auditability.** Every answer can cite Cypher result rows and ticket IDs; no hallucinated numbers, because counts come from the database.

Be honest about what is synthetic: relationships such as agent specialisation or problem-to-service are largely random in this data. The goal of
this project is the **method and plumbing**, proven on data whose structure is real in form but noisy in meaning. Do not read the output as IT insight.
