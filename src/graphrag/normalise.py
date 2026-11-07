"""Merge near-duplicate extracted names into canonical concepts using embeddings (spike 01: names almost never repeat verbatim)."""
import re
import numpy as np
import ollama
from . import config as C

NORM_VERSION = "v2"
DEFAULT_THRESHOLD = 0.85

def clean(name: str) -> str:
    return re.sub(r"\s+", " ", name.replace("_", " ").replace("-", " ").lower()).strip()

def strip_ai(name: str) -> str:
    """Remove the word 'ai' before embedding: short phrases sharing 'ai' otherwise look similar to nomic and collapse into catch-all clusters (M3 sweep)."""
    return re.sub(r"\s+", " ", re.sub(r"\b(ai's|ai|llms|llm)\b", " ", name)).strip() or name

def embed(names: list[str], client: ollama.Client | None = None, batch: int = 64) -> np.ndarray:
    client = client or ollama.Client(host=C.OLLAMA_URL)
    out = []
    for i in range(0, len(names), batch):
        r = client.embed(model=C.EMBED_MODEL, input=["clustering: " + strip_ai(n) for n in names[i:i + batch]])
        out.extend(r["embeddings"])
    v = np.array(out, dtype=np.float32)
    return v / np.clip(np.linalg.norm(v, axis=1, keepdims=True), 1e-9, None)

def cluster(names: list[str], vecs: np.ndarray, counts: dict[str, int], threshold: float = DEFAULT_THRESHOLD) -> dict[str, str]:
    """Greedy leader clustering: most frequent names become leaders; a name joins the first leader with cosine >= threshold. Returns name -> canonical."""
    order = sorted(range(len(names)), key=lambda i: (-counts.get(names[i], 1), len(names[i]), names[i]))
    leaders: list[int] = []
    mapping: dict[str, str] = {}
    for i in order:
        best, best_s = None, threshold
        for j in leaders:
            s = float(vecs[i] @ vecs[j])
            if s >= best_s:
                best, best_s = j, s
        if best is None:
            leaders.append(i); mapping[names[i]] = names[i]
        else:
            mapping[names[i]] = names[best]
    return mapping

def canonicalise(items: list[dict], threshold: float = DEFAULT_THRESHOLD, client: ollama.Client | None = None) -> dict:
    """items need 'kind' and 'name'. Clusters within each kind. Returns {kind: {raw_clean: canonical}} and alias table."""
    result: dict[str, dict[str, str]] = {}
    for kind in sorted({it["kind"] for it in items}):
        counts: dict[str, int] = {}
        for it in items:
            if it["kind"] == kind:
                n = clean(it["name"]); counts[n] = counts.get(n, 0) + 1
        names = list(counts)
        result[kind] = cluster(names, embed(names, client), counts, threshold) if names else {}
    aliases: dict[str, dict[str, list[str]]] = {}
    for kind, m in result.items():
        aliases[kind] = {}
        for raw, canon in m.items():
            aliases[kind].setdefault(canon, []).append(raw)
    return {"threshold": threshold, "version": NORM_VERSION, "mapping": result, "aliases": aliases}
