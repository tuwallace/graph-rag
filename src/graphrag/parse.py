"""Split a transcript into turns and question/answer segments."""
import re

_LABEL = re.compile(r"(?m)^(Assistant|AI|User):[ \t]*")
INTERVIEWER = ("Assistant", "AI")

def parse_turns(text: str) -> list[tuple[str, str]]:
    """Line-start labels only, so quoted chat logs inside an answer are not split. Both interviewer labels are kept."""
    parts = _LABEL.split(text)
    return [(who, body.strip()) for who, body in zip(parts[1::2], parts[2::2])]

def segments(text: str) -> list[dict]:
    """One segment per participant turn, paired with the interviewer turn before it."""
    out, last = [], None
    for who, body in parse_turns(text):
        if who in INTERVIEWER:
            last = body
        elif last is not None:
            out.append({"idx": len(out), "question": last, "answer": body})
    return out

def user_text(text: str) -> str:
    return "\n".join(body for who, body in parse_turns(text) if who == "User")
