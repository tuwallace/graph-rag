#!/usr/bin/env python3
"""Bundles the captured outputs under anim/public/captures into anim/src/captures.json for the terminal-replay clips.
Capture first:  PYTHONPATH=src uv run python docs/video/demo/seg3_counts.py > docs/video/anim/public/captures/seg3_graph.txt   (and the other demo scripts)
Run:  python3 docs/video/demo/build_captures.py"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
CAP = ROOT / "docs/video/anim/public/captures"
out = {"seg3_graph": (CAP / "seg3_graph.txt").read_text().strip("\n"), "seg3_plain": (CAP / "seg3_plain.txt").read_text().strip("\n"),
       "seg7": (CAP / "seg7.txt").read_text().strip("\n"), "seg8": json.loads((CAP / "seg8.json").read_text())}
(ROOT / "docs/video/anim/src/captures.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print({k: (len(v) if isinstance(v, (str, list)) else list(v)) for k, v in out.items()})
