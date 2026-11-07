"""M8: themes for global questions. Louvain communities on the canonical-concept co-occurrence graph (Python, networkx),
offline summaries by a large model run alone, written to Theme nodes with IN_THEME edges.

Run: PYTHONPATH=src uv run python -m graphrag.themes --run-id demo1 [--stage detect|summarise|load|all]

Co-occurrence unit: the interview. Only concepts mentioned (affirmed, current) in at least MIN_DEG interviews take part, and an
edge needs at least MIN_SHARED shared interviews; weight is shared / sqrt(deg_a * deg_b), which damps hub concepts.
"""
import argparse, collections, itertools, json, math, re
import networkx as nx
import ollama
from neo4j import GraphDatabase, READ_ACCESS
from . import config as C

THEMES_VERSION = "v2"   # v2: distinctive, unique labels (v1 gave three themes the label 'AI in Creative Work')
MIN_DEG, MIN_SHARED, RESOLUTION, SEED, MIN_MEMBERS = 2, 2, 1.0, 7, 5
SUMMARY_MODEL = "qwen2.5:32b-instruct-q4_K_M"
KIND_OF = {"Task": "task", "AIUse": "ai_use", "Concern": "concern"}


def fetch(driver):
    """Per-interview concept sets and per-concept stats. Read-only."""
    with driver.session(default_access_mode=READ_ACCESS) as s:
        rows = s.run("""MATCH (g:Group)<-[:IN_GROUP]-(i:Interview)-[:HAS_SEGMENT]->(:Segment)-[r:DOES_TASK|USES_AI_FOR|RAISES]->(c)
                        WHERE r.status='current' AND r.polarity='affirmed'
                        RETURN i.transcript_id AS t, g.name AS g, labels(c)[0] AS l, c.name AS n""").values()
    by, group_of = collections.defaultdict(set), {}
    for t, g, l, n in rows:
        by[t].add((l, n)); group_of[t] = g
    return by, group_of


def build_graph(by, min_deg=MIN_DEG, min_shared=MIN_SHARED):
    deg = collections.Counter(c for cs in by.values() for c in cs)
    keep = {c for c, v in deg.items() if v >= min_deg}
    co = collections.Counter()
    for cs in by.values():
        for a, b in itertools.combinations(sorted(cs & keep), 2):
            co[(a, b)] += 1
    G = nx.Graph()
    for (a, b), w in co.items():
        if w >= min_shared:
            G.add_edge(a, b, weight=w / math.sqrt(deg[a] * deg[b]), shared=w)
    return G, deg


def detect(by, group_of, resolution=RESOLUTION, seed=SEED, min_members=MIN_MEMBERS):
    G, deg = build_graph(by)
    comms = [c for c in nx.community.louvain_communities(G, weight="weight", resolution=resolution, seed=seed) if len(c) >= min_members]
    themes = []
    for members in comms:
        interviews = {t for t, cs in by.items() if cs & members}
        per_group = collections.Counter(group_of[t] for t in interviews)
        ms = sorted(({"name": n, "kind": KIND_OF[l], "label": l, "interviews": deg[(l, n)], "strength": round(G.degree((l, n), weight="weight"), 3)} for l, n in members),
                    key=lambda m: (-m["interviews"], m["name"]))
        themes.append({"members": ms, "interviews": len(interviews), "per_group": dict(per_group)})
    themes.sort(key=lambda t: (-t["interviews"], t["members"][0]["name"]))
    for i, t in enumerate(themes):
        t["id"] = f"theme{i + 1:02d}"
    cover = {"concepts_in_graph": G.number_of_nodes(), "concepts_total": len(deg), "concepts_in_themes": sum(len(t["members"]) for t in themes),
             "mentions_in_themes": sum(m["interviews"] for t in themes for m in t["members"]), "mentions_total": sum(deg.values())}
    return themes, cover


def sample_quotes(driver, names: list[str], k=3):
    with driver.session(default_access_mode=READ_ACCESS) as s:
        return [dict(r) for r in s.run("""
            MATCH (i:Interview)-[:HAS_SEGMENT]->(:Segment)-[r:DOES_TASK|USES_AI_FOR|RAISES]->(c)
            WHERE c.name IN $names AND r.status='current' AND r.polarity='affirmed'
            RETURN c.name AS concept, i.transcript_id AS interview, r.quote AS quote ORDER BY r.supports DESC LIMIT $k""", names=names, k=k)]


def prompt_for(theme, quotes, used_labels=()):
    mem = "\n".join(f"- {m['name']} ({m['kind']}, {m['interviews']} interviews)" for m in theme["members"][:25])
    qs = "\n".join(f'- ({q["interview"]}, {q["concept"]}) "{q["quote"][:220]}"' for q in quotes)
    pg = ", ".join(f"{g}: {n}" for g, n in sorted(theme["per_group"].items()))
    used = ("Labels already used by other clusters (yours must differ): " + "; ".join(used_labels) + "\n\n") if used_labels else ""
    return (f"These concepts were extracted from interviews about AI and tend to be mentioned together by the same participants.\n"
            f"Interviews touching this cluster: {theme['interviews']} of 500 ({pg}).\n\nConcepts:\n{mem}\n\nSample participant quotes:\n{qs}\n\n{used}"
            'Write a JSON object with keys "label" (3 to 6 words naming what is distinctive about this cluster, such as the activity or the worry; do not use the word AI), "summary" (2 to 3 sentences, under 70 words, describing what this cluster is about) and '
            '"cited_concepts" (the 3 to 6 concept names from the list that your summary relies on, copied exactly). '
            "Use only the concepts and quotes given. Do not add numbers. Do not claim anything about people in general.")


def validate(out: dict, theme, used_labels=()) -> list[str]:
    names = {m["name"] for m in theme["members"]}
    errs = []
    if not isinstance(out.get("label"), str) or not 1 <= len(out["label"].split()) <= 8: errs.append("label")
    elif re.search(r"\bAI\b", out["label"], re.I) or out["label"].strip().lower() in {u.lower() for u in used_labels}: errs.append("label generic or duplicate")
    if not isinstance(out.get("summary"), str) or not 10 <= len(out["summary"].split()) <= 90: errs.append("summary length")
    cited = out.get("cited_concepts")
    if not isinstance(cited, list) or not 2 <= len(cited) <= 8 or any(c not in names for c in cited): errs.append("cited_concepts not members")
    if re.search(r"\d", out.get("summary", "")): errs.append("summary contains a number")
    return errs


def summarise(driver, themes, client=None, retries=2, log=print):
    client = client or ollama.Client(host=C.OLLAMA_URL, timeout=900)
    used = []
    for t in themes:
        quotes = sample_quotes(driver, [m["name"] for m in t["members"][:12]])
        for attempt in range(retries + 1):
            r = client.chat(model=SUMMARY_MODEL, messages=[{"role": "user", "content": prompt_for(t, quotes, used)}], format="json",
                            options={"temperature": 0, "num_predict": 500})
            try:
                out = json.loads(r.message.content)
            except json.JSONDecodeError:
                out = {}
            errs = validate(out, t, used)
            if not errs:
                break
        if not errs: used.append(out["label"])
        t.update(label=out.get("label"), summary=out.get("summary"), cited_concepts=out.get("cited_concepts"), validation_errors=errs,
                 summary_model=SUMMARY_MODEL, themes_version=THEMES_VERSION)
        log(f"[summarise {t['id']}] {len(t['members'])} members -> {t['label']!r} errors={errs}")
    return themes


def write(driver, themes, run_id):
    with driver.session() as s:
        s.run("MATCH (t:Theme) DETACH DELETE t").consume()   # themes are derived: rebuild from scratch
        for t in themes:
            if t["validation_errors"]:
                continue   # never store an unvalidated summary
            s.run("""CREATE (t:Theme {id:$id, label:$label, summary:$summary, size:$size, interviews:$interviews, group_counts:$gc,
                                      cited_concepts:$cited, summary_model:$model, themes_version:$ver, run_id:$run})""",
                  id=t["id"], label=t["label"], summary=t["summary"], size=len(t["members"]), interviews=t["interviews"],
                  gc=json.dumps(t["per_group"]), cited=t["cited_concepts"], model=t["summary_model"], ver=t["themes_version"], run=run_id).consume()
            for kind in KIND_OF:
                rows = [{"name": m["name"], "w": m["interviews"]} for m in t["members"] if m["label"] == kind]
                if rows:
                    s.run(f"UNWIND $rows AS r MATCH (c:{kind} {{name:r.name}}) MATCH (t:Theme {{id:$id}}) MERGE (c)-[x:IN_THEME]->(t) SET x.weight=r.w",
                          rows=rows, id=t["id"]).consume()


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); ap.add_argument("--stage", default="all", choices=["detect", "summarise", "load", "all"])
    a = ap.parse_args()
    path = C.ROOT / "data" / "artefacts" / a.run_id / "themes.json"
    with GraphDatabase.driver(C.NEO4J_URI, auth=(C.NEO4J_USER, C.NEO4J_PASSWORD), notifications_min_severity="OFF") as d:
        if a.stage in ("detect", "all"):
            by, group_of = fetch(d); themes, cover = detect(by, group_of)
            path.write_text(json.dumps({"themes": themes, "coverage": cover, "params": dict(min_deg=MIN_DEG, min_shared=MIN_SHARED, resolution=RESOLUTION, seed=SEED)}))
            print("detected", len(themes), "themes; coverage", cover, flush=True)
        if a.stage in ("summarise", "all"):
            doc = json.loads(path.read_text())
            from .pipeline import unload
            for m in (C.GEN_MODEL, C.ROUTER_MODEL, C.EMBED_MODEL): unload(m)   # run the large model alone
            doc["themes"] = summarise(d, doc["themes"], log=lambda s: print(s, flush=True))
            path.write_text(json.dumps(doc)); unload(SUMMARY_MODEL)
        if a.stage in ("load", "all"):
            doc = json.loads(path.read_text()); write(d, doc["themes"], a.run_id)
            with d.session() as s:
                print("loaded themes:", s.run("MATCH (t:Theme) RETURN count(t)").single()[0], "IN_THEME edges:", s.run("MATCH ()-[x:IN_THEME]->() RETURN count(x)").single()[0])


if __name__ == "__main__":
    main()
