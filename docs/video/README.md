# Companion video: tooling and sources

A 4.8-minute YouTube video about this project ("I built a graph RAG over 500 AI interviews, and checked it honestly"). The structure and tooling follow the
helpdesk-rag video. Rendered audio and video are **not** committed (regenerable); this folder has the sources and the scripts to rebuild them.
The published video: https://youtu.be/Ewr40PPcdpA

| Path | What it is |
|---|---|
| `script.md` | The script: 9 segments, narration, visuals, upload text. Every number comes from `docs/07`, `docs/08` and `docs/09` |
| `narration/build_narration.py` | Turns the script's narration into audio and sentence timings with a synthetic voice (Kokoro-82M, `af_heart`); `PRONOUNCE` holds the spoken respellings |
| `anim/` | A [Remotion](https://www.remotion.dev) project: 6 animated clips and 3 terminal replays, each animation step timed to a spoken phrase |
| `demo/` | The commands whose real output the replays show (`seg3_counts.py`, `seg7_grounded.py`, `capture_seg8.py`) and `build_captures.py` |
| `finalize.py` | Joins the 9 clips and writes `upload/` (video, captions, chapters, description, tags, thumbnail) |
| `upload/` | Captions, description, tags, thumbnail and checklist (the 12 MB video is git-ignored) |

## How it was made
- **Narration is synthetic** (Kokoro-82M). Disclose it when uploading.
- **Three segments are terminal replays** of real captured output (the graph answer and plain vector search; the answer validator and a stored fallback case; two real `ollmcp` sessions).
  Each is labelled on screen as a replay, and lines starting with `[annotation]` are added text, not program output.
- **No transcript text appears on screen** (ADR-0012). The quotes shown in the last replay are the ones the small model invented.
- All numbers are model-judged (`qwen2.5:32b`, labels confirmed by the owner), one run each, on 500 of the 1,250 interviews.

## Rebuilding it
Needs Node.js 22, Python 3.12, `ffmpeg` and `espeak-ng` (`brew install ffmpeg espeak-ng`), Neo4j and the Ollama models running for the captures.
```bash
# 0. captures (real output; needs the graph loaded)
PYTHONPATH=src uv run python docs/video/demo/seg3_counts.py > docs/video/anim/public/captures/seg3_graph.txt
PYTHONPATH=src uv run python docs/video/demo/seg3_counts.py plain > docs/video/anim/public/captures/seg3_plain.txt
PYTHONPATH=src uv run python docs/video/demo/seg7_grounded.py > docs/video/anim/public/captures/seg7.txt
uv run --with pexpect python scripts/live_ollmcp_session.py data/live_a.log nothink clear     # and a second run without nothink/clear, then:
python3 docs/video/demo/capture_seg8.py data/live_a.log data/live_b.log
python3 docs/video/demo/build_captures.py
# 1. narration audio and timings
cd docs/video/narration && uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python kokoro soundfile
.venv/bin/python build_narration.py --engine kokoro --voice af_heart
# 2. clips
cd ../anim && npm install && npm run render:all && npx remotion still src/index.ts Thumbnail out/thumbnail.png --port=3100
# 3. assemble
cd ../../.. && python3 docs/video/finalize.py
```
Before rendering a new script, run `/video-preflight` (screen-recording check, mispronunciation table, audio dropouts).

## Checks on the finished file (2026-11-12)
287 s, 1920x1080, H.264 + AAC. Integrated loudness -16.5 LUFS, true peak -4.4 dBTP. Silences of 0.45 to 0.52 s fall at five commas or colons inside sentences (normal punctuation
pauses, not dropouts); the last 3.3 s is the closing slide held in silence. I could not listen to it: check the pronunciation of "A I", "rag", "Neo for J", "ollmcp" and "GitHub" by ear.

Licences to check before publishing: Remotion (company licence terms apply above a size), Kokoro (Apache-2.0), the dataset card (inconsistent; the owner decided to treat it as MIT, with credit to Anthropic).
