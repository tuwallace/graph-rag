"""Extraction v3: one list of typed items per transcript, each with status, polarity and a verbatim quote.
Changes from the spike (see docs/spike-01-extraction.md): one kind per phrase, status and polarity fields,
no corpus-like examples in the prompt, grounding against participant turns only."""
import json, re, time
import ollama
from . import config as C
from .parse import segments, user_text
from .ground import score, locate, THRESHOLD

PROMPT_VERSION = "v3.3"
MAX_NEW_TOKENS = 3000      # guard against runaway generation (one run hung for 10+ minutes without this)
KINDS = ["work_task", "ai_use", "concern"]
STATUSES = ["current", "not_current"]
ATTITUDES = ["positive", "mixed", "negative", "unclear"]

SCHEMA = {
    "type": "object",
    "properties": {
        "role_guess": {"type": ["string", "null"]},
        "overall_attitude_to_ai": {"type": "string", "enum": ATTITUDES},
        "items": {"type": "array", "maxItems": 25, "items": {"type": "object", "properties": {
            "kind": {"type": "string", "enum": KINDS},
            "name": {"type": "string"},
            "status": {"type": "string", "enum": STATUSES},
            "polarity": {"type": "string", "enum": ["affirmed", "negated"]},
            "quote": {"type": "string"}},
            "required": ["kind", "name", "status", "polarity", "quote"]}},
    },
    "required": ["role_guess", "overall_attitude_to_ai", "items"],
}

PROMPT = """You read an interview transcript about how a professional uses AI at work. Extract ONLY what the participant said (the "User" turns). Never use the interviewer's words.

Return a list of items. Each item has:
- kind, exactly one of:
  work_task: a piece of the participant's own work. If the quote is about using AI for it, use ai_use instead.
  ai_use: a way the participant uses, tries, or deliberately avoids AI.
  concern: a worry, frustration, distrust or limitation of AI that the participant states. The name must restate what the quote itself complains about or fears; do not name a broader theme the quote does not state.
- name: a short, specific, lowercase noun phrase.
- status: current (the participant does, did or feels this now or has done) or not_current (a wish, plan, prediction, "would" or "might", or something about other people).
- polarity: affirmed, or negated if the participant says they do NOT do or feel this.
- quote: an exact copied span of at most 25 words from a participant turn that supports the item.

Rules: each phrase appears once, under one kind only, and each quote is used for at most one item. Do not invent items. Empty lists are fine.
Also give role_guess (the participant's job if stated or clearly implied, else null) and overall_attitude_to_ai.

TRANSCRIPT:
"""

def build_prompt(text: str) -> str:
    return PROMPT + text

def hygiene_failures(items: list[dict], prompt: str = PROMPT, top: int = 10) -> list[str]:
    """Names among the most frequent that appear verbatim in the prompt (a sign the model copied an example)."""
    counts: dict[str, int] = {}
    for it in items:
        n = it["name"].strip().lower()
        counts[n] = counts.get(n, 0) + 1
    p = prompt.lower()
    ranked = sorted(counts, key=lambda k: -counts[k])[:top]
    return [n for n in ranked if len(n.split()) >= 2 and n in p]

def _nq(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()

def dedupe(items: list[dict]) -> list[dict]:
    """Drop repeats of the same quote, or of the same (kind, name); keep the first. Runs of repeated items were seen in 4 of 20 transcripts."""
    seen_q, seen_n, out = set(), set(), []
    for it in items:
        q, n = _nq(it["quote"]), (it["kind"], it["name"].strip().lower())
        if q in seen_q or n in seen_n:
            continue
        seen_q.add(q); seen_n.add(n); out.append(it)
    return out

def extract(text: str, client: ollama.Client | None = None, model: str | None = None) -> dict:
    client = client or ollama.Client(host=C.OLLAMA_URL)
    t0 = time.time()
    r = client.chat(model=model or C.GEN_MODEL, messages=[{"role": "user", "content": build_prompt(text)}],
                    format=SCHEMA, think=False, options={"temperature": 0, "num_ctx": 16384, "num_predict": MAX_NEW_TOKENS})
    secs = time.time() - t0
    try:
        data, ok = json.loads(r["message"]["content"]), True
    except Exception:
        data, ok = {"role_guess": None, "overall_attitude_to_ai": "unclear", "items": []}, False
    n_raw = len(data.get("items", []))
    data["items"] = dedupe(data.get("items", []))
    segs, utext = segments(text), user_text(text)
    for it in data.get("items", []):
        it["ground_score"] = round(score(it["quote"], utext), 3)
        it["grounded"] = it["ground_score"] >= THRESHOLD
        idx, sc = locate(it["quote"], segs)
        it["segment_idx"] = idx if sc >= THRESHOLD else None
    return {"valid_json": ok, "truncated": r.get("done_reason") == "length", "n_raw_items": n_raw, "secs": round(secs, 1), "prompt_version": PROMPT_VERSION,
            "model": model or C.GEN_MODEL, "extraction": data}
