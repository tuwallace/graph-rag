"""Check that an extracted quote really comes from the participant (User turns), tolerating small wording and punctuation drift."""
import re
from difflib import SequenceMatcher

THRESHOLD = 0.9
_PUNCT = re.compile(r"[^\w\s]")

def tokens(s: str) -> list[str]:
    return _PUNCT.sub(" ", s.lower().replace("’", "'")).split()

def score(quote: str, haystack: str) -> float:
    """Fraction of quote tokens covered by in-order matching blocks of the haystack (1.0 = verbatim)."""
    q, h = tokens(quote), tokens(haystack)
    if not q or not h:
        return 0.0
    blocks = SequenceMatcher(None, q, h, autojunk=False).get_matching_blocks()
    return sum(b.size for b in blocks) / len(q)

def is_grounded(quote: str, haystack: str, threshold: float = THRESHOLD) -> bool:
    return score(quote, haystack) >= threshold

def locate(quote: str, segs: list[dict]) -> tuple[int | None, float]:
    """Best participant answer for a quote: (segment idx, score)."""
    best, best_s = None, 0.0
    for s in segs:
        sc = score(quote, s["answer"])
        if sc > best_s:
            best, best_s = s["idx"], sc
    return best, best_s
