"""Drive a live ollmcp session (qwen3:8b-16k, routed profile, mcp.json) through a pseudo-terminal with five fixed questions, confirming each tool call.
Run: uv run --with pexpect python scripts/live_ollmcp_session.py data/live_ollmcp.log   (needs Ollama, Neo4j and the models running; the log is git-ignored)
"""
import pexpect, sys, re, time, json
Q = ["What are the main themes across the interviews?",
     "What are the top concerns among scientists?",
     "Compare scientists and creatives on hallucinations",
     "Show me quotes about losing skills",
     "What is 2+2?"]
log = open(sys.argv[1], "w")
c = pexpect.spawn("/Users/twallace/.local/bin/ollmcp", ["-j", "mcp.json", "-m", "qwen3:8b-16k"], cwd="/Users/twallace/source/ragsandbox/graph-rag",
                  encoding="utf-8", timeout=240, dimensions=(50, 200), env={**__import__("os").environ, "TERM": "dumb", "NO_COLOR": "1"})
c.logfile_read = log
def wait_prompt():
    # the chat prompt ends with '❯' or '>' ; also handle y/n confirmations
    while True:
        i = c.expect([r"[❯>] ?$", r"\(y/n\)|\[y/N\]|\[Y/n\]|Execute|Proceed", pexpect.TIMEOUT], timeout=240)
        if i == 0: return True
        if i == 1: c.sendline("y"); continue
        return False
ok = wait_prompt(); print("started", ok, flush=True)
for q in Q:
    t0 = time.time(); c.sendline(q); r = wait_prompt(); print(f"{time.time()-t0:5.1f}s done={r}  {q}", flush=True)
c.sendline("quit"); time.sleep(2); c.close()
