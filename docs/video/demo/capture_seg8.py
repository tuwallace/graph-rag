"""Segment 8 replay source: pulls two real exchanges out of ollmcp session logs recorded by scripts/live_ollmcp_session.py
(logs are git-ignored under data/). A: thinking off + context cleared (faithful). B: thinking on, long conversation (tool skipped, quotes invented).
Writes anim/public/captures/seg8.json. Usage: python3 docs/video/demo/capture_seg8.py data/live_ollmcp6.log data/live_ollmcp2.log"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]

def exchanges(path):
    s = re.sub(r"\x1b\[[0-9;?]*[A-Za-z]", "", pathlib.Path(path).read_text(errors="ignore")).replace("\r", "")
    L = s.split("\n"); P = [i for i, l in enumerate(L) if "❯" in l and "qwen3" in l and not re.search(r"/tm|/cc", l)]
    out = {}
    for a in P:
        nxt = [i for i, l in enumerate(L) if "❯" in l and "qwen3" in l and i > a]; b = nxt[0] if nxt else len(L)
        seg = "\n".join(L[a:b]); q = L[a].split("❯")[-1].strip()
        i = seg.rfind("Answer (Markdown)"); ans = seg[i:].split("\n")[2:] if i >= 0 else []
        ans = [re.sub(r"[│]", " ", x).rstrip() for x in ans]; ans = [x for x in ans if x.strip() and not set(x.strip()) <= set("─-")]
        out[q] = {"tool_called": "Executing Tool" in seg, "answer": ans}
    return out

a, b = exchanges(sys.argv[1]), exchanges(sys.argv[2])
good = a["What are the top concerns among scientists?"]
bad = b["Show me quotes about losing skills"]
cap = {"good": {"question": "What are the top concerns among scientists?", "tool_called": good["tool_called"], "answer": good["answer"][:9]},
       "bad": {"question": "Show me quotes about losing skills", "tool_called": bad["tool_called"], "answer": bad["answer"][:8]}}
(ROOT / "docs/video/anim/public/captures").mkdir(parents=True, exist_ok=True)
(ROOT / "docs/video/anim/public/captures/seg8.json").write_text(json.dumps(cap, indent=1, ensure_ascii=False))
print(json.dumps(cap, indent=1, ensure_ascii=False)[:2600])
