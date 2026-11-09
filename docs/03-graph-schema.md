# 03. Graph schema (Interviewer corpus)

## Model

```mermaid
flowchart LR
  G[Group] <-- IN_GROUP --- I[Interview]
  I -- HAS_SEGMENT --> S["Segment (Q/A pair, embedded)"]
  S -- DOES_TASK --> T[Task]
  S -- USES_AI_FOR --> U[AIUse]
  S -- RAISES --> C[Concern]
  I -- WORKS_AS --> O[Occupation]
  T & U & C -- IN_THEME --> TH[Theme]
```

### Nodes

| Label | Key | Source | Properties | Approx. count (full corpus) |
|---|---|---|---|---|
| `Group` | `name` | split | `workforce`, `creatives`, `scientists` | 3 |
| `Interview` | `transcript_id` | CSV | `n_turns`, `chars` | 500 loaded (of 1,250 in the dataset) |
| `Segment` | `id` = `transcript_id#idx` | parsed Q/A pairs | `idx`, `question`, `answer`, `embedding`, plus decision-model attributes below | 5,450 loaded (500 interviews) |
| `Task` | `key` (canonical) | extraction + merge | `name`, `aliases[]`, `mentions` | hundreds to low thousands (**unmeasured**) |
| `AIUse` | `key` | extraction + merge | same | same |
| `Concern` | `key` | extraction + merge | same | tens to hundreds |
| `Occupation` | `key` | `role_guess` + merge | `name` | hundreds |
| `Theme` | `id` | community detection over canonical nodes | `label`, `summary` (LLM, offline) | tens |

### Relationships (all carry provenance)

| Type | From to | Properties |
|---|---|---|
| `IN_GROUP` | Interview to Group | |
| `HAS_SEGMENT` | Interview to Segment | |
| `DOES_TASK`, `USES_AI_FOR`, `RAISES` | Segment to Task / AIUse / Concern | `quote` (verbatim, from a `User` turn), `status` (`current|not_current`), `raw_name`, `model`, `prompt_version`, `run_id` |
| `WORKS_AS` | Interview to Occupation | `raw_name`, `model`, `run_id` |
| `IN_THEME` | Task / AIUse / Concern to Theme | `weight` |

### Decision-model attributes on `Segment` (properties, not nodes)

From `nimble` ([ADR-0008](decisions/0008-decision-model-router.md)): `attitude` (`positive|negative|mixed|none`) and `attitude_conf`, one call per segment (M3 dropped `topic` and `job_worry_p`: gating saved almost nothing and the job-worry question fired once in 50 segments). Store the model and prompt version alongside (`attributes` v2). Low-confidence values (below a tuned threshold) are kept but excluded from counts by default.

## Provenance rule

Mapping from the extractor's `kind` to labels: `work_task` to `Task`, `ai_use` to `AIUse`, `concern` to `Concern`. Edges also store `polarity`; `negated` edges are kept but excluded from counts by default.

Every extracted edge stores the exact quote and which model and prompt produced it. The quote must be a substring of a **`User`** turn of that segment (checked at load time;
failures are dropped and counted). This makes every answer auditable and gives an automatic precision floor ([spike 01](spike-01-extraction.md)).

## Pipeline

1. **Parse** (`parse.py`): split on line-start `Assistant|AI|User:`; pair each `User` turn with the preceding interviewer turn.
2. **Extract** (`extract.py`, prompt `v3.3`): per transcript, `qwen3:8b-16k` with a JSON schema; one list of items with `kind`, `status` (`current|not_current`), `polarity`, `quote`; capped and de-duplicated.
3. **Ground** (`ground.py`): check that the quote is in the participant's turns (fuzzy match, threshold 0.9) and record the segment it came from; ungrounded items stay in the artefact but are flagged `keep: false`.
4. **Verify** (`verify.py`): `nimble` yes/no scores `supports` and `own_current` per item; edges with `supports` below 0.2 are kept in the artefact but flagged `keep: false` and excluded from counts.
5. **Attributes** (`attributes.py`): `nimble` attitude per segment.
6. **Normalise** (`normalise.py`): embed raw names with `nomic-embed-text` after removing the word "ai", greedy leader clustering per kind at cosine 0.85; canonical = most frequent name; aliases kept.
7. **Assemble** (`pipeline.py`): one JSONL record per interview (segments with attitude, edges with canonical name, verify scores and `keep`), the input to the loader in M5.
8. **Load**: idempotent `MERGE` into Neo4j; vector index on `Segment.embedding`.
9. **Themes**: community detection on the canonical-node co-occurrence graph; summaries written offline by the 32b model.

Stages run stage-major (all transcripts through one model, then the next) and are resumable per transcript; see `src/graphrag/manifest.py`.

## Constraints and indexes

```cypher
CREATE CONSTRAINT interview_id IF NOT EXISTS FOR (n:Interview)  REQUIRE n.transcript_id IS UNIQUE;
CREATE CONSTRAINT segment_id   IF NOT EXISTS FOR (n:Segment)    REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT group_name   IF NOT EXISTS FOR (n:Group)      REQUIRE n.name IS UNIQUE;
CREATE CONSTRAINT task_key     IF NOT EXISTS FOR (n:Task)       REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT aiuse_key    IF NOT EXISTS FOR (n:AIUse)      REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT concern_key  IF NOT EXISTS FOR (n:Concern)    REQUIRE n.key IS UNIQUE;
CREATE CONSTRAINT occ_key      IF NOT EXISTS FOR (n:Occupation) REQUIRE n.key IS UNIQUE;
CREATE VECTOR INDEX segment_embedding IF NOT EXISTS FOR (s:Segment) ON (s.embedding)
  OPTIONS {indexConfig: {`vector.dimensions`: 768, `vector.similarity_function`: 'cosine'}};   // nomic-embed-text is 768-d (verify)
```

## What was removed from the helpdesk model

No `Ticket`, `Agent`, `Category`, `Service`, `Department`, `SLABreach`. Archived at [archive/helpdesk](archive/helpdesk/README.md).
