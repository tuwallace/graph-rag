"""Per-segment attitude from the decision model: one call per segment.
M3 finding: gating on `topic` first saved almost nothing (36 of 50 segments needed the second call, 2.8 s per segment) and the job-worry
question fired once in 50, so v2 asks only for attitude (spike 01: p50 2.4 s for three questions)."""
from .decision import decide

ATTR_VERSION = "v2"
ATTITUDE = {"type": "choice", "instructions": "What attitude toward AI does the participant express in this answer?", "criteria": {
    "positive": "explicitly says AI is helpful, good, satisfying or promising",
    "negative": "explicitly says AI is unhelpful, frustrating, untrustworthy or harmful",
    "mixed": "clearly says both good and bad things about AI",
    "none": "no evaluation of AI: facts, a plain description of how they use it, consent, small talk, or 'no'/'none'"}}

def segment_state(seg: dict) -> str:
    return f"Interviewer: {seg['question']}\nParticipant: {seg['answer']}"

def attributes(seg: dict) -> dict:
    a = decide(segment_state(seg), {"attitude": ATTITUDE})["attitude"]
    return {"attitude": a["choice"], "attitude_conf": round(a["confidence"], 3), "calls": 1}
