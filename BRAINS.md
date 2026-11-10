# Repository Instructions & Memory Orchestration
Structural memory: ./graphify-out/ (graph.json, GRAPH_REPORT.md)  |  Declarative memory: ./graphify-out/wiki/ (generated) + ./Session_Logs.md (hand-maintained) + ./docs/ (decisions, results)

Before starting work: read ./Session_Logs.md and ./docs/09-completion-status.md, then query the graph instead of grepping the whole repo
(`graphify query`, `graphify explain`, `graphify path`).
After any meaningful change, refresh the map (no LLM needed):
`~/.local/share/uv/tools/ollmcp/bin/python ~/.claude/skills/graphify-vault-sync/scripts/ollmcp-vault-task.py --repo-root "$PWD"`
(= `graphify update .` then `graphify export wiki`). To rename communities with Ollama run `OLLAMA_BASE_URL=http://localhost:11434/v1 graphify label . --backend ollama`
(the `/v1` suffix is required; without it Ollama returns 404 and the labels fall back to placeholders).
Before ending a session: append to ./Session_Logs.md with what got done, decisions made, and what is next.
Use native [[Wikilinks]] when linking within Session_Logs.md.

Project rules (see docs/decisions/0012): never commit `data/`, `.env` or transcript text; run `uv run python scripts/prepush_check.py` before pushing (the `.githooks/pre-push` hook does it when `git config core.hooksPath .githooks` is set).
Run order for models on a 32 GB Mac: the 32b judge/summary model must run alone (`ollama stop` the small ones first).
