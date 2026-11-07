from graphrag import schema

def test_vector_index_statement_uses_dimension():
    q = schema.vector_index_stmt(768)
    assert "`vector.dimensions`: 768" in q and "cosine" in q

def test_statements_are_idempotent_form():
    assert all("IF NOT EXISTS" in s for s in schema.STATEMENTS)
