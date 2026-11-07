"""Start the MCP server over stdio and call it like a client would. Usage: PYTHONPATH=src uv run python scripts/mcp_smoke.py [routed|typed]"""
import asyncio, json, sys, pathlib
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

ROOT = pathlib.Path(__file__).resolve().parents[1]
profile = sys.argv[1] if len(sys.argv) > 1 else "routed"
CALLS = {"routed": [("ask_interviews", {"question": q}) for q in ["How do creatives use AI for brainstorming?", "Top concerns among scientists?", "Compare scientists and creatives on hallucinations", "What are the main themes?", "Show quotes about losing skills", "What is 2+2?"]],
         "typed": [("search_segments", {"query": "losing creative skills"}), ("concept_stats", {"kind": "concern", "group": "scientists", "limit": 3}), ("compare_groups", {"concept": "hallucinations"}), ("quotes", {"concept": "job security"}), ("theme_summary", {})]}

async def main():
    t = StdioTransport(command=str(ROOT / ".venv/bin/python"), args=["-W", "ignore", "-m", "graphrag.mcp_server"], cwd=str(ROOT),
                       env={"PYTHONPATH": "src", "GRAPHRAG_PROFILE": profile})
    async with Client(t) as c:
        print("tools:", [x.name for x in await c.list_tools()])
        for name, args in CALLS[profile]:
            r = await c.call_tool(name, args)
            d = r.data if r.data is not None else r.content
            print(name, json.dumps(args)[:60], "=>", json.dumps(d, default=str)[:230])

asyncio.run(main())
