"""Constraints and indexes (idempotent). Run: PYTHONPATH=src uv run python -m graphrag.schema"""
from neo4j import GraphDatabase
from . import config as C

STATEMENTS = [
    "CREATE CONSTRAINT interview_id IF NOT EXISTS FOR (n:Interview)  REQUIRE n.transcript_id IS UNIQUE",
    "CREATE CONSTRAINT segment_id   IF NOT EXISTS FOR (n:Segment)    REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT group_name   IF NOT EXISTS FOR (n:Group)      REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT task_key     IF NOT EXISTS FOR (n:Task)       REQUIRE n.key IS UNIQUE",
    "CREATE CONSTRAINT aiuse_key    IF NOT EXISTS FOR (n:AIUse)      REQUIRE n.key IS UNIQUE",
    "CREATE CONSTRAINT concern_key  IF NOT EXISTS FOR (n:Concern)    REQUIRE n.key IS UNIQUE",
    "CREATE CONSTRAINT occ_key      IF NOT EXISTS FOR (n:Occupation) REQUIRE n.key IS UNIQUE",
    "CREATE CONSTRAINT theme_id     IF NOT EXISTS FOR (n:Theme)      REQUIRE n.id IS UNIQUE",
]

def vector_index_stmt(dim: int) -> str:
    return ("CREATE VECTOR INDEX segment_embedding IF NOT EXISTS FOR (s:Segment) ON (s.embedding) "
            f"OPTIONS {{indexConfig: {{`vector.dimensions`: {dim}, `vector.similarity_function`: 'cosine'}}}}")

def embedding_dim() -> int:
    """Ask the embedder instead of hard-coding the dimension."""
    import ollama
    return len(ollama.Client(host=C.OLLAMA_URL).embed(model=C.EMBED_MODEL, input=["search_document: x"])["embeddings"][0])

def apply(driver, dim: int | None = None) -> list[str]:
    dim = dim or embedding_dim()
    stmts = STATEMENTS + [vector_index_stmt(dim)]
    with driver.session() as s:
        for q in stmts:
            s.run(q).consume()
    return stmts

def main():
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD)) as d:
        d.verify_connectivity()
        done = apply(d)
        with d.session() as s:
            cons = s.run("SHOW CONSTRAINTS YIELD name RETURN count(*) AS n").single()["n"]
            idx = s.run("SHOW INDEXES YIELD name, type WHERE type = 'VECTOR' RETURN name").values()
        print(f"applied {len(done)} statements; constraints={cons}; vector indexes={[r[0] for r in idx]}")

if __name__ == "__main__":
    main()
