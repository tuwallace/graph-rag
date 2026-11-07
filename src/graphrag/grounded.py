"""Grounded answers: the server renders facts as text, a model may only add framing, and nothing reaches the user unvalidated.

Pipeline: payload (typed query output) -> render() deterministic text -> optional LLM framing -> validate() -> deliver the LLM text if every
quote and figure checks out against the payload, otherwise deliver the rendered text (which is grounded by construction).

Guarantee and its limits: quotes in double quotes must be found (ground.is_grounded) in a quote or excerpt of the payload AND the interview id
of that item must be cited in the answer; every cited id must be in the payload; every digit-form figure must appear in the rendered facts
(rounding to an integer allowed). Not checked: number words ("three"), claims without quote marks or digits, and the quality of the framing.
Applies to answers produced through grounded_answer(); a client model that writes free text around the MCP tool output is not intercepted.
"""
import re
import ollama
from . import config as C, ground, router, queries as Q

IDRE = re.compile(r"\b[a-z]+_\d{4}(?:#\d+)?\b")
QMARK = re.compile(r'["“”]')
LISTNUM = re.compile(r"(?m)^\s*(?:[-*]\s*)?(?:\*\*)?\d{1,2}[.)]\s")
NUM = re.compile(r"(?<![\w#.])\d+(?:\.\d+)?")
KIND_NAME = {"ai_use": "Uses of AI", "task": "Work tasks", "concern": "Concerns about AI"}
CAVEAT = "These are findings from a sample of AI-led interviews, not facts about workers in general."

SYSTEM = ("You write short answers about AI interview transcripts using ONLY the facts provided. Rules: copy any quote exactly as given, inside double quotes, "
          "and cite its interview id in the same sentence; do not put anything else in double quotes; use only figures that appear in the facts; "
          "do not add numbers or outside knowledge; if the facts say clarify, unavailable or out of scope, say that. Keep it under 150 words.")


def quotes_in(text: str) -> list[str]:
    idx = [m.start() for m in QMARK.finditer(text)]
    return [q for q in (text[a + 1:b] for a, b in zip(idx[0::2], idx[1::2])) if len(q.split()) >= 4]


def numbers(text: str) -> set[str]:
    t = LISTNUM.sub(" ", IDRE.sub(" ", text))
    return set(NUM.findall(t))


def allowed_numbers(rendered: str) -> set[str]:
    out = numbers(rendered)
    for n in list(out):
        try:
            out.add(str(round(float(n))))
        except ValueError:
            pass
    return out


def items(payload: dict) -> list[tuple[str, str]]:
    """(interview id, verbatim text) for every quote or excerpt in the payload."""
    out = [(r["interview"], r["excerpt"]) for r in payload.get("results", [])]
    out += [(q["interview"], q["quote"]) for q in payload.get("quotes", [])]
    for g in (payload.get("by_group") or {}).values():
        out += [(q["interview"], q["quote"]) for q in g.get("quotes", [])]
    return out


def render(payload: dict) -> str:
    st = payload.get("status")
    if st != "ok":
        return payload.get("message", "No answer available.") + (" Candidates: " + ", ".join(payload["candidates"]) if payload.get("candidates") else "")
    route = payload["route"]
    if route == "concept_stats":
        n = payload["group_size"]
        lines = [f'{KIND_NAME[payload["kind"]]} mentioned most among {payload["group"]} interviews ({n} interviews; counted once per interview, affirmed and current mentions only):']
        lines += [f'{i}. {r["concept"]}: {r["interviews"]} interviews ({100 * r["interviews"] / n:.1f}%)' for i, r in enumerate(payload["ranking"], 1)]
    elif route == "compare_groups":
        lines = [f'Interviews mentioning "{payload["concept"]}" by group:'.replace('"', "'")]
        for g, v in payload["by_group"].items():
            lines.append(f'- {g}: {v["interviews"]} of {v["of"]} interviews ({100 * v["share"]:.1f}%)')
            lines += [f'  "{q["quote"]}" ({q["interview"]})' for q in v["quotes"]]
    elif route == "evidence":
        lines = [f'Participant quotes about \'{payload["concept"]}\':'] + [f'- "{q["quote"]}" ({q["interview"]}, {q["group"]})' for q in payload["quotes"]]
    elif route == "local_search":
        lines = ["Closest participant answers (excerpts):"] + [f'- "{r["excerpt"]}" ({r["interview"]}, {r["group"]})' for r in payload["results"]]
    elif route == "theme_overview":
        lines = ["Themes found by clustering concepts that are mentioned together (interviews touching each theme are counted once):"]
        for t in payload["themes"]:
            mem = ", ".join(f'{m["name"]} ({m["interviews"]})' for m in t["members"][:4])
            lines.append(f'- {t["label"]} ({t["interviews"]} interviews): {t["summary"]} Top concepts: {mem}.')
    else:
        lines = [str(payload)]
    return "\n".join(lines + ["", CAVEAT])


def validate(answer: str, payload: dict, rendered: str, question: str = "") -> list[str]:
    issues, its = [], items(payload)
    ids = {i for i, _ in its}
    cited = {c.split("#")[0] for c in IDRE.findall(answer)}
    if payload.get("status") == "ok":
        ids |= {r["segment"].split("#")[0] for r in payload.get("results", [])}
    for c in cited - ids:
        issues.append(f"cited id not in tool output: {c}")
    for q in quotes_in(answer):
        srcs = {i for i, t in its if ground.is_grounded(q, t)}
        if not srcs:
            issues.append(f"quote not in tool output: {q[:60]!r}")
        elif not (srcs & cited):
            issues.append(f"quote source not cited: {q[:60]!r}")
    bad = numbers(answer) - numbers(question) - allowed_numbers(rendered)
    if bad:
        issues.append(f"figures not in tool output: {sorted(bad)}")
    return issues


def llm_frame(question: str, rendered: str, client=None) -> str:
    client = client or ollama.Client(host=C.OLLAMA_URL, timeout=600)
    r = client.chat(model=C.GEN_MODEL, think=False, options={"temperature": 0, "num_predict": 500},
                    messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": f"Question: {question}\n\nFacts:\n{rendered}"}])
    return r.message.content or ""


def grounded_answer(question: str, driver, index, decide_fn=None, llm=llm_frame) -> dict:
    """Route, render, frame with the LLM, validate, fall back to the rendered facts on any issue."""
    payload = router.answer(question, driver, index, **({"decide_fn": decide_fn} if decide_fn else {}))
    rendered = render(payload)
    if payload.get("status") != "ok":                       # nothing for a model to add; the message is the answer
        return {"text": rendered, "source": "rendered", "issues": [], "raw": None, "payload": payload}
    raw = llm(question, rendered)
    issues = validate(raw, payload, rendered, question)
    return {"text": raw if not issues else rendered, "source": "llm" if not issues else "rendered_fallback", "issues": issues, "raw": raw, "payload": payload}
