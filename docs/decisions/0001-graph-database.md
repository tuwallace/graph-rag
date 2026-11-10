# ADR-0001: Graph database

- Status: accepted 2026-11-10 by the project owner (earlier: proposed (amended 2026-11-05: written against helpdesk data; the Neo4j Community choice still holds, but node counts are about 1,250 interviews and 14,500 segments, and the vector index now lives here per [ADR-0011](0011-retrieval-in-neo4j.md)))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Moderate. The loader is a few hundred lines of Cypher and Python; the typed tools hold the queries. Switching to another Cypher database means porting those, not the data model.

## Context

The graph is small (about 1,200 nodes on the sample, tens of thousands on the full set). Scale is irrelevant; what matters is how well a **small local LLM** and the
developer can work with it, and whether it fits an **8 GB Docker VM** that already hosts other stacks (postgres, redis, grafana, prometheus, Qdrant, Phoenix).
A `neo4j:5-enterprise` image already exists locally, but Enterprise requires license acceptance and does not suit a public MIT repo.

## Decision drivers

- Cypher availability and familiarity (the model, the docs and the developer all benefit)
- Tooling for inspecting the graph while developing
- License and operational simplicity
- Memory footprint in Docker on Apple silicon
- Vector / hybrid support if ADR-0003 is revisited
- Project longevity

## Options

1. **Neo4j Community 5.x**
2. Memgraph
3. FalkorDB (Redis module)
4. Kuzu (embedded)
5. PostgreSQL + Apache AGE

## Weighted decision matrix

| Criterion | Weight | Neo4j CE | Memgraph | FalkorDB | Kuzu | PG + AGE |
|---|---|---|---|---|---|---|
| Cypher / LLM familiarity | 25 | 5 | 4 | 4 | 4 | 2 |
| Tooling and debuggability | 20 | 5 | 4 | 3 | 3 | 3 |
| License and ops simplicity | 20 | 4 | 3 | 3 | 5 | 5 |
| Fit in 8 GB Docker VM | 15 | 3 | 4 | 4 | 5 | 4 |
| Vector / hybrid support | 10 | 4 | 4 | 4 | 3 | 5 |
| Longevity and maintenance | 10 | 5 | 4 | 3 | 1 | 4 |
| **Weighted score (out of 5)** | 100 | **4.40** | 3.80 | 3.50 | 3.75 | 3.60 |

Notes on the less certain scores (not verified by me in this session):

- Kuzu: scored 1 on longevity because I recall its repository being archived in late 2025. Verify before relying on either the score or this note. Even with a 5 on longevity it would reach 4.15, still behind Neo4j.
- Memgraph and FalkorDB license terms (source-available) change the "license" scores; check the current terms if you care.
- Neo4j's memory score is 3 because its defaults assume a dedicated machine; it fits once heap and page cache are capped (see [05](../05-components.md)).

Sensitivity: Kuzu stays behind Neo4j even with a longevity score of 5 (4.15 vs 4.40), so the ranking holds unless you re-weight heavily toward "no server to run".
PG + AGE would win only if reusing an existing Postgres outweighed Cypher familiarity.

## Decision

Use **Neo4j Community 5.x** (pinned LTS tag) in Docker, bound to localhost, with APOC.

## Consequences

- Good: the best-documented Cypher, Neo4j Browser for visual debugging, and small models have seen plenty of Cypher.
- Costs: about 2 GB of the Docker VM; a JVM service to operate.
- Community edition limits: one user database, no fine-grained RBAC, no clustering. Acceptable here; handled in [ADR-0007](0007-privacy-and-access.md).
- Risk: Docker VM memory pressure. Mitigation: explicit caps; stop unused stacks.

## Confirmation

Phase 0 exit: container healthy, constraints created, `RETURN 1` over Bolt from the host, memory under 2.5 GB in `docker stats` during load.

## Revisit when

The Docker VM cannot be raised above 8 GB and Neo4j plus the other stacks cause swapping, or Neo4j's licensing changes for the Community edition.
