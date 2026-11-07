"""Thin client for Ollama's /v1/systemone decision-model endpoint (typed choice / yes-no questions with probabilities)."""
import time, requests
from . import config as C

class DecisionError(RuntimeError):
    pass

def decide(state: str, questions: dict, model: str | None = None, retries: int = 1, timeout: int = 180) -> dict:
    """Returns the 'answers' dict. 'choice' answers carry choice/probabilities/confidence; 'noul' answers carry a probability under 'noul'."""
    body = {"model": model or C.ROUTER_MODEL, "state": state, "questions": questions}
    last = None
    for attempt in range(retries + 1):
        try:
            r = requests.post(f"{C.OLLAMA_URL}/v1/systemone", json=body, timeout=timeout)
            if r.status_code == 200:
                return r.json()["answers"]
            last = f"HTTP {r.status_code}: {r.text[:200]}"
        except requests.RequestException as e:
            last = str(e)
        time.sleep(1 + attempt)
    raise DecisionError(last)
