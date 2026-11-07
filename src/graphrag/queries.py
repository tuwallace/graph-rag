"""Typed, parameterised, read-only queries over the interview graph (04-query-and-tools).

Every function takes a Neo4j driver and opens a READ-access-mode session, so a write is refused by the driver even if a
query were wrong. Counts use distinct interviews and only affirmed, current edges (negated or not_current edges are kept in
the graph but excluded by default).
"""
import hashlib, json
import numpy as np
import ollama
from neo4j import READ_ACCESS
from . import config as C
from .normalise import embed as embed_names

KINDS = {"task": ("Task", "DOES_TASK"), "ai_use": ("AIUse", "USES_AI_FOR"), "concern": ("Concern", "RAISES")}
GROUPS = ("all", "workforce", "creatives", "scientists")
COUNTED = "r.status = 'current' AND r.polarity = 'affirmed'"
_REL_ANY = "type(r) IN ['DOES_TASK','USES_AI_FOR','RAISES']"


def _read(driver, cypher: str, **params) -> list[dict]:
    with driver.session(default_access_mode=READ_ACCESS) as s:
        return [dict(r) for r in s.run(cypher, **params)]


def embed_query(text: str, client=None) -> list[float]:
    client = client or ollama.Client(host=C.OLLAMA_URL)
    return client.embed(model=C.EMBED_MODEL, input=["search_query: " + text])["embeddings"][0]


def search_segments(driver, query: str, k: int = 5, embedding=None) -> list[dict]:
    emb = embedding if embedding is not None else embed_query(query)
    return _read(driver, f"""
        CALL db.index.vector.queryNodes('segment_embedding', $k, $emb) YIELD node AS s, score
        MATCH (i:Interview)-[:HAS_SEGMENT]->(s) MATCH (i)-[:IN_GROUP]->(g:Group)
        OPTIONAL MATCH (s)-[r]->(x) WHERE {_REL_ANY}
        RETURN i.transcript_id AS interview, g.name AS group, s.id AS segment, round(score, 3) AS score,
               left(s.answer, 300) AS excerpt, s.attitude AS attitude, collect(DISTINCT x.name)[..5] AS concepts
        ORDER BY score DESC""", k=k, emb=emb)


def concept_stats(driver, kind: str, group: str = "all", limit: int = 10) -> list[dict]:
    label, rel = KINDS[kind]
    return _read(driver, f"""
        MATCH (g:Group)<-[:IN_GROUP]-(i:Interview)-[:HAS_SEGMENT]->(s:Segment)-[r:{rel}]->(c:{label})
        WHERE ($group = 'all' OR g.name = $group) AND {COUNTED}
        RETURN c.name AS concept, count(DISTINCT i) AS interviews
        ORDER BY interviews DESC, concept LIMIT $limit""", group=group, limit=limit)


def group_sizes(driver) -> dict[str, int]:
    return {r["g"]: r["n"] for r in _read(driver, "MATCH (g:Group)<-[:IN_GROUP]-(i:Interview) RETURN g.name AS g, count(i) AS n")}


def quotes(driver, concept: str, limit: int = 5, group: str = "all") -> list[dict]:
    """Quotes for an exact canonical concept name (any kind), strongest verification first."""
    return _read(driver, f"""
        MATCH (g:Group)<-[:IN_GROUP]-(i:Interview)-[:HAS_SEGMENT]->(s:Segment)-[r]->(c)
        WHERE {_REL_ANY} AND c.name = $concept AND ($group = 'all' OR g.name = $group) AND {COUNTED}
        RETURN i.transcript_id AS interview, g.name AS group, s.id AS segment, r.quote AS quote, round(r.supports, 2) AS supports
        ORDER BY r.supports DESC, interview LIMIT $limit""", concept=concept, limit=limit, group=group)


def compare_groups(driver, concept: str) -> dict:
    sizes = group_sizes(driver)
    rows = _read(driver, f"""
        MATCH (g:Group)<-[:IN_GROUP]-(i:Interview)-[:HAS_SEGMENT]->(s:Segment)-[r]->(c)
        WHERE {_REL_ANY} AND c.name = $concept AND {COUNTED}
        RETURN g.name AS group, count(DISTINCT i) AS interviews""", concept=concept)
    got = {r["group"]: r["interviews"] for r in rows}
    out = {}
    for g, n in sizes.items():
        k = got.get(g, 0)
        out[g] = {"interviews": k, "of": n, "share": round(k / n, 3) if n else None, "quotes": quotes(driver, concept, 2, g)}
    return out


def theme_summary(driver, theme: str | None = None, limit: int = 12) -> list[dict]:
    """Pre-built themes (M8): label, summary, size, interviews touched, per-group interview counts and top member concepts with counts.
    `theme` filters by a case-insensitive match on the label, the summary or a member concept name."""
    rows = _read(driver, """
        MATCH (t:Theme)
        OPTIONAL MATCH (c)-[x:IN_THEME]->(t)
        WITH t, c, x ORDER BY x.weight DESC
        WITH t, collect(CASE WHEN c IS NULL THEN NULL ELSE {name: c.name, interviews: x.weight} END)[..6] AS members,
             collect(toLower(c.name)) AS allnames
        WHERE $theme IS NULL OR toLower(t.label) CONTAINS toLower($theme) OR toLower(t.summary) CONTAINS toLower($theme)
              OR any(n IN allnames WHERE n CONTAINS toLower($theme))
        RETURN t.id AS id, t.label AS label, t.summary AS summary, t.size AS concepts, t.interviews AS interviews,
               t.group_counts AS group_counts, members
        ORDER BY interviews DESC LIMIT $limit""", theme=theme, limit=limit)
    for r in rows:
        r["group_counts"] = json.loads(r["group_counts"]) if r.get("group_counts") else {}
    return rows


class ConceptIndex:
    """Embedding match from free text to a canonical concept name. Names are embedded once and cached on disk."""

    def __init__(self, driver, cache_dir=None, client=None):
        self.client = client or ollama.Client(host=C.OLLAMA_URL)
        rows = _read(driver, "MATCH (c:Task|AIUse|Concern) RETURN c.name AS name, labels(c)[0] AS label, c.mentions AS mentions ORDER BY name")
        self.names = [r["name"] for r in rows]; self.labels = [r["label"] for r in rows]; self.mentions = [r["mentions"] for r in rows]
        key = hashlib.sha1("\n".join(f"{l}|{n}" for l, n in zip(self.labels, self.names)).encode()).hexdigest()[:12]
        path = (cache_dir or (C.ROOT / "data")) / f"concept_embeddings_{key}.json"
        if path.exists():
            self.mat = np.array(json.loads(path.read_text()), dtype=np.float32)
        else:
            self.mat = embed_names(self.names, self.client).astype(np.float32)
            path.write_text(json.dumps(self.mat.tolist()))
        self.mat = self.mat / np.linalg.norm(self.mat, axis=1, keepdims=True)

    def match(self, text: str, top: int = 3) -> list[dict]:
        v = np.array(embed_names([text], self.client)[0], dtype=np.float32); v /= np.linalg.norm(v)
        sims = self.mat @ v
        return [{"name": self.names[i], "kind": self.labels[i], "mentions": self.mentions[i], "similarity": round(float(sims[i]), 3)}
                for i in np.argsort(-sims)[:top]]

    _STOP = set("a an the of in on for to and or but with about from by at as is are was were be been do does did how what which who whom why when where "
                "show me tell give list find us our their they them it its this that these those there than then differ differs different compare "
                "between versus vs say said talk talked quotes quote examples example people participants interviewees most more less common main "
                "scientists scientist creatives creative workforce workers worker professionals overall all any some many much often use uses using "
                "used think feel felt".split())

    def match_question(self, question: str, top: int = 3) -> list[dict]:
        """Resolve the concept in a question: embed the whole question and each 1 to 3 word span of content words; keep the best by
        similarity (ties go to the longer, more specific span, then the more frequent concept). Whole-question embeddings alone pick near-miss long names."""
        import re
        words = re.findall(r"[a-z0-9']+", question.lower())
        spans = {" ".join(words[i:j]) for i in range(len(words)) for j in range(i + 1, min(i + 3, len(words)) + 1)
                 if all(w not in self._STOP for w in words[i:j])}
        cands = [question] + sorted(spans)
        vecs = np.array(embed_names(cands, self.client), dtype=np.float32)
        vecs /= np.linalg.norm(vecs, axis=1, keepdims=True)
        sims = vecs @ self.mat.T                      # candidates x concepts
        best = {}
        for ci in range(sims.shape[0]):
            j = int(np.argmax(sims[ci])); sc = float(sims[ci, j])
            if j not in best or sc > best[j][0]:
                best[j] = (sc, cands[ci])
        order = sorted(best.items(), key=lambda kv: (-round(kv[1][0], 2), -len(kv[1][1].split()), -(self.mentions[kv[0]] or 0)))[:top]
        return [{"name": self.names[j], "kind": self.labels[j], "mentions": self.mentions[j], "similarity": round(sc, 3), "from": span}
                for j, (sc, span) in order]
