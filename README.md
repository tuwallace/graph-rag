# graph-rag

A local graph-RAG demo over interview transcripts: an LLM extracts what people do with AI and what worries them, the results go into a Neo4j graph with a vector index, and a small decision model routes questions to typed queries exposed over MCP. Everything runs on one Mac (Ollama on the host, Neo4j in Docker). It is a demo and a set of measured findings, not a product.

**Data.** [Anthropic/AnthropicInterviewer](https://huggingface.co/datasets/Anthropic/AnthropicInterviewer) by Anthropic: 1,250 AI-led interviews (1,000 workforce, 125 creatives, 125 scientists), published with participant consent for research. **This project uses 500 of them** (all 125 creatives, all 125 scientists and a fixed random 250 of the 1,000 workforce); every count, share and result below describes those 500, not the full dataset. See Anthropic's [Introducing Anthropic Interviewer](https://www.anthropic.com/research/anthropic-interviewer) post. The dataset card is inconsistent about its license (front matter `mit`, body "data CC-BY, code MIT"); the owner decided on 2026-11-09 to treat it as MIT, and Anthropic is credited either way. **No transcript text or extracted graph is stored in this repository**; `scripts/download_data.py` fetches the data and everything derived stays in the git-ignored `data/` folder.

**Read the results with the limits in mind.** The sample is self-selected and interviewed by an AI, so findings describe these interviews, not workers in general. The demo uses 500 of the 1,250 interviews. Extraction precision is estimated by a language model, not by humans (about 0.74 before and about 0.80 after the verify step; one rater, in-sample threshold). Recall was measured once, on 10 transcripts, by a larger model: the graph captures about 34% of what the judge lists participants as saying (about 28% for concerns), so counts are lower bounds; a looser second pass for concerns lifted concern coverage on those 10 transcripts to about 51% and has since been applied to all 500 interviews (concern edges 1,358 to 1,861). An unfiltered pass was only 49% correct in a 120-edge sample, so new edges are kept only at verify score 0.6 or more; a fresh 100-edge sample of those was 76% correct and 14% wrong by the larger model's labels, and concern coverage on the 10 recall transcripts then went from 22% to 42% (all kinds 32% to 40%). The author-written evaluation questions have 36 in-scope items, so differences of a question or two are noise; two further sets of 48 questions written by `qwen2.5:32b` give router accuracy of 75% to 78% in scope. Concern merging is the coarsest step (about 15% of sampled concern merges join different ideas), attitude labels agree 82.5% with a larger model, and a sampled rerun of extraction changes about 40% of the items (production runs at temperature 0, where reruns matched in 9 of 10 transcripts). All results are model-judged and from one run each; see [docs/09](docs/09-completion-status.md) for the full status.

## What was built

| Stage | Module | What it does |
|---|---|---|
| Extract | `src/graphrag/extract.py` | `qwen3:8b-16k` returns tasks, AI uses and concerns with a verbatim quote; fuzzy grounding against participant turns only |
| Verify, attributes | `verify.py`, `attributes.py` | `nimble` decision model scores support per edge and attitude per segment |
| Normalise | `normalise.py` | Embedding clustering of near-duplicate names into canonical concepts |
| Pipeline | `pipeline.py` | Resumable, stage-major build over a fixed 500-interview sample |
| Load | `load.py` | Idempotent `MERGE` into Neo4j 5.26 Community with a 768-d vector index |
| Themes | `themes.py` | Louvain communities on concept co-occurrence, summarised offline by `qwen2.5:32b` with checked citations |
| Query, route | `queries.py`, `router.py` | Typed read-only queries; `nimble` picks the route and fills enums, with a confidence gate |
| Answers | `grounded.py` | Server-rendered facts, model framing only, every quote and figure validated, fallback to the facts |
| MCP | `mcp_server.py` | `ask_interviews` (routed) or five typed tools (`GRAPHRAG_PROFILE=typed`) |

## Findings so far (one machine, one run each)

- **The graph earns its place on counts and comparisons.** On 17 count and comparison questions, plain vector RAG answered none correctly; the graph-backed configurations answered 71% to 82%. For plain "what did people say about X" questions the graph made no clear difference.
- **The decision-model router is about as accurate as letting qwen3 pick among tools** (92% vs 86% route accuracy on 36 in-scope questions, within noise), abstains instead of guessing, and adds about 1.1 s per question. It did not meet the original "under 1 s" bound; see [ADR-0008](docs/decisions/0008-decision-model-router.md).
- **Groundedness can be enforced, not just prompted.** Through the validated path, 90 of 90 delivered quotes were found in the cited interview (the raw model text was 89 of 92), at the cost of falling back to plain facts on 2 of 51 answers.
- **Builds are slow on a laptop.** 500 interviews took about 10.7 h of compute (extract 6.5 h, verify 1.9 h, attributes 2.3 h). Names almost never repeat, so normalisation is required before counting.

Full write-ups: [implementation roadmap and outcomes](docs/07-implementation-roadmap.md), [evaluation results](docs/08-evaluation-results.md), [decision records](docs/decisions/README.md).

## Run it

Requires macOS or Linux, [uv](https://docs.astral.sh/uv/), Docker, and [Ollama](https://ollama.com) with a `nimble` decision model available (see the Ollama blog post on decision models) plus:

```bash
ollama pull qwen3:8b && ollama pull nomic-embed-text && ollama pull qwen2.5:32b-instruct-q4_K_M
```

The `qwen3:8b-16k` tag used here is `qwen3:8b` with a 16k context:

```bash
printf 'FROM qwen3:8b\nPARAMETER num_ctx 16384\n' > /tmp/Modelfile && ollama create qwen3:8b-16k -f /tmp/Modelfile
```

```bash
uv sync
cp .env.example .env            # then set NEO4J_PASSWORD
docker compose up -d            # Neo4j on 127.0.0.1 only
uv run python scripts/download_data.py
PYTHONPATH=src uv run python -m graphrag.schema
PYTHONPATH=src uv run python -m graphrag.pipeline --run-id tiny1 --scope tiny --stage all   # 5 interviews, minutes
# full 500-interview build is about 11 hours: --scope demo (resumable; rerun the same command if interrupted)
PYTHONPATH=src uv run python -m graphrag.load --run-id tiny1 --scope tiny
PYTHONPATH=src uv run python -m graphrag.themes --run-id demo1      # needs the 500-interview scope for meaningful themes
ollmcp --servers-json mcp.json --model qwen3:8b-16k
```

**Using it in `ollmcp`.** The server returns validated facts in an `answer` field and tells the client to relay it unchanged, but a small client model can ignore that. In a live test, `qwen3:8b-16k` only called the tool reliably with thinking off (`/tm` in `ollmcp`) and the conversation cleared before each question (`/cc`); otherwise it sometimes skipped the tool and invented quotes. Questions unrelated to the interviews may be answered by the model itself without the tool. See `docs/08-evaluation-results.md`.

Tests: `uv run pytest`. Evaluation: `eval/`.

## Privacy and safety

- `data/` and `.env` are git-ignored; `scripts/prepush_check.py` fails on any tracked `data/` path, large file, run of 25+ words shared with the corpus, or gitleaks finding. Enable it with `git config core.hooksPath .githooks`.
- Query sessions use Neo4j READ access mode and the MCP server exposes no write tool (Community edition has no read-only role, so this is an application-level guarantee).
- Transcripts are untrusted text: extraction output is schema-constrained and answers return short quotes only. Quotes in docs are short attributed excerpts. A PII pass is recorded in [ADR-0012](docs/decisions/0012-privacy-for-transcripts.md).

## License

Code: MIT (see `LICENSE`). Data: not redistributed here. The dataset card's front matter says MIT and its body says data CC-BY; the project owner decided on 2026-11-09 to treat it as MIT. Attribution to Anthropic is kept regardless.
