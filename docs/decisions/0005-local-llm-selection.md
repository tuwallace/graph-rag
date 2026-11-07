# ADR-0005: Local LLM selection

- Status: proposed (amended 2026-11-05: model roles are now extractor, verifier and router, answer writer and offline judge; see [05](../05-components.md))
- Date: 2026-11-05
- Deciders: twallace
- Reversibility: Easy. Model names are config (`GEN_MODEL`, ollmcp `--model`).

## Context

Hardware: Apple M2 Pro, 32 GB unified memory. The Docker VM takes 8 GB of that. Installed Ollama models (from `ollama list`): `qwen3:8b`, `qwen3:8b-16k`, `nomic-embed-text`,
`qwen2.5-coder:7b-instruct-q8_0`, `qwen2.5:32b-instruct-q4_K_M` (19 GB), `glm-4.7-flash` (19 GB), `llama3.1:8b-instruct-q8_0`, `llama3`, `phi3`, `llava`, `llama3.2-vision`, `nimble` (a decision model, see ADR-0008).

Evidence in this repo: qwen3:8b is described as the reliable tool-caller and drove the MCP tests (`data/mcp_test.log`); it also over-fills optional arguments (ADR-0004).
HyDE, fine-tuning and embedder swaps did not improve the full pipeline, so the embedder stays.
Nothing about `glm-4.7-flash` or `llama3.1` tool-calling has been measured here; those scores are assumptions to test.

## Roles

| Role | Needs |
|---|---|
| Orchestrator and answer writer | Reliable tool calls, follows "only use tool numbers", fits memory alongside Docker, interactive latency |
| Cypher drafter (conditional, ADR-0004 option 4) | Code-tuned, fits alongside the orchestrator |
| Offline judge | Stronger than the orchestrator, different family if possible; may be slow |
| Embedder | Unchanged |

## Weighted decision matrix: orchestrator

| Criterion | Weight | qwen3:8b-16k | qwen3:8b | llama3.1:8b-q8 | glm-4.7-flash | qwen2.5:32b-q4 |
|---|---|---|---|---|---|---|
| Tool-calling evidence in this project | 35 | 4 | 4 | 3 | 3 | 4 |
| Memory fit (host + 8 GB Docker VM) | 25 | 5 | 5 | 4 | 2 | 1 |
| Interactive latency | 20 | 4 | 4 | 3 | 3 | 1 |
| Usable context for tool results | 10 | 4 | 2 | 3 | 4 | 4 |
| Local, no cloud dependency | 10 | 5 | 5 | 5 | 5 | 5 |
| **Weighted score (out of 5)** | 100 | **4.35** | 4.15 | 3.45 | 3.05 | 2.75 |

Scores for `llama3.1`, `glm-4.7-flash` and `qwen2.5:32b` on tool-calling are **unmeasured guesses**; the eval in [06](../06-evaluation-and-roadmap.md) tests `llama3.1:8b-instruct-q8_0` as one alternative.
The margin between the two qwen3 variants is small and comes from context length: a 4k context can truncate multi-tool conversations (verify the effective context of plain `qwen3:8b` in your Ollama version).

## Decision

| Role | Model | Notes |
|---|---|---|
| Orchestrator, answers | **`qwen3:8b-16k`** | Keep tool results under about 1.5k tokens each |
| Cypher drafter (only if ADR-0004 option 4 is enabled) | `qwen2.5-coder:7b-instruct-q8_0` | Escalate to `qwen2.5:32b` only if it fails the eval |
| Offline judge | `qwen2.5:32b-instruct-q4_K_M` | Run alone: `OLLAMA_MAX_LOADED_MODELS=1`; stop the Docker stacks you do not need |
| Router (decision model) | **`nimble`** | See [ADR-0008](0008-decision-model-router.md); typed `choice` questions, not chat |
| Embeddings | `nomic-embed-text` | Unchanged; keep `search_document:` / `search_query:` prefixes |
| Alternative to test | `llama3.1:8b-instruct-q8_0` | Comparison run only |

No new model pulls required.

## Consequences

- Good: everything runs locally with no cloud keys (the shell exports cloud keys; the project rule is to always pass the Ollama backend explicitly).
- Costs: an 8B model limits multi-step reasoning; the typed tools (ADR-0004) compensate by doing the reasoning in Cypher.
- Risk: memory. The 19 GB models cannot run beside the 8B model and the Docker VM. Mitigation: one model at a time for judging.

## Confirmation

Config B and C results in the eval: tool-selection accuracy per model, and the number of calls where the model fabricated an argument value.

## Revisit when

The tool-selection accuracy for `qwen3:8b-16k` is below the baseline's in config C (it picks the wrong server), or a newer local model with better tool-use is pulled.
