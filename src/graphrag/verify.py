"""Verify extracted items with the decision model: does the quote support this exact claim, and is it the participant's own, current statement?
Calibrated against the LLM-labelled sheet in scripts/calibrate_verify.py (see docs/07 M3 outcome)."""
from .decision import decide

VERIFY_VERSION = "v1"
CLAIM = {
    "work_task": "The participant does this work: {name}.",
    "ai_use": "The participant uses, tries or deliberately avoids AI for: {name}.",
    "concern": "The participant is worried, frustrated or distrustful about AI because of: {name}.",
}
QUESTIONS = {
    "supports": {"type": "noul", "instructions": "Does what the participant said directly state the claim? It must say this exact thing, not a nearby idea, not the opposite, and not something about other people."},
    "own_current": {"type": "noul", "instructions": "Is the participant describing something they themselves do or feel, not a wish, a prediction, an 'if' or something about other people?"},
}

def claim_for(item: dict) -> str:
    return CLAIM[item["kind"]].format(name=item["name"].replace("_", " "))

def state_for(item: dict) -> str:
    return f'Claim: {claim_for(item)}\nParticipant said: "{item["quote"]}"'

def verify_item(item: dict) -> dict:
    a = decide(state_for(item), QUESTIONS)
    return {"supports": round(float(a["supports"]["noul"]), 4), "own_current": round(float(a["own_current"]["noul"]), 4)}

def keep(v: dict, supports_min: float, current_min: float = 0.0) -> bool:
    return v["supports"] >= supports_min and v["own_current"] >= current_min
