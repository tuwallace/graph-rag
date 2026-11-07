"""Resumable stage bookkeeping: each stage appends one JSON line per finished key; a rerun skips keys already done."""
import json, pathlib, time
from . import config as C

class Stage:
    def __init__(self, run_id: str, name: str, root: pathlib.Path | None = None):
        self.dir = (root or C.ROOT / "data" / "artefacts") / run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / f"{name}.jsonl"
        self.done_keys = self._load()

    def _load(self) -> set[str]:
        if not self.path.exists():
            return set()
        keys = set()
        for line in self.path.read_text().splitlines():
            if line.strip():
                try: keys.add(json.loads(line)["key"])
                except (json.JSONDecodeError, KeyError): pass       # a half-written last line is ignored and redone
        return keys

    def done(self, key: str) -> bool:
        return key in self.done_keys

    def write(self, key: str, record: dict) -> None:
        rec = {"key": key, "ts": int(time.time()), **record}
        with open(self.path, "a") as f:
            f.write(json.dumps(rec) + "\n")
        self.done_keys.add(key)

    def records(self) -> list[dict]:
        out = []
        for line in self.path.read_text().splitlines() if self.path.exists() else []:
            try: out.append(json.loads(line))
            except json.JSONDecodeError: pass
        return out
