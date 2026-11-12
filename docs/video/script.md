# Video script: "I built a graph RAG over 500 AI interviews, and checked it honestly"

Target length: about 5:10 (about 686 spoken words at 150 words a minute, plus a few seconds per segment for visuals). Draft 1, modelled on the structure of the helpdesk-rag video
(`helpdesk-rag/docs/video/`): short segments, each tied to a number from this repo's own runs.
Types: **ANIM** = animated clip (Remotion), **REPLAY** = terminal replay of real captured output, clearly labelled as a replay, **LIVE** = your screen recording.
Every number below comes from `docs/08-evaluation-results.md`, `docs/09-completion-status.md` or `docs/07-implementation-roadmap.md`. All scores are model-judged
(`qwen2.5:32b`, labels confirmed by the owner), one run each, on **500 of the 1,250 interviews** of the Anthropic Interviewer dataset.

Rules for the footage (ADR-0012): no transcript text on screen beyond one short attributed sentence; no real names; show the dataset credit.

## Segment plan

| # | Time | Segment | Type |
|---|---|---|---|
| 1 | 0:00 | Hook | ANIM |
| 2 | 0:31 | What I built | ANIM |
| 3 | 1:17 | Why a graph: counting questions | REPLAY |
| 4 | 1:50 | How good is the extraction? | ANIM |
| 5 | 2:20 | The recall fix that backfired | ANIM |
| 6 | 2:54 | Routing the question | ANIM |
| 7 | 3:25 | Answers you can trust | REPLAY |
| 8 | 3:57 | A small model in ollmcp | REPLAY |
| 9 | 4:34 | Takeaways | ANIM |

---

## 1. Hook (0:00)

**Visual (ANIM):** title card; two questions appear: "Which concerns do scientists raise most?" and "Do creatives and scientists differ on hallucinations?" Then a bar: "plain RAG 0 of 17, graph 13 of 17".

**Narration:**
> I built a system that answers questions about five hundred AI interviews, entirely on my laptop. Ask it which concerns scientists raise most,
> and it counts. Plain vector search got none of seventeen counting and comparison questions right. The graph got thirteen. But the part worth
> watching is how often my own checks were wrong, and how I found out. Here is the whole story, with the numbers.

## 2. What I built (0:35)

**Visual (ANIM):** pipeline appearing step by step: interview transcript → extract (qwen3 eight billion) → verify (nimble) → merge similar names → Neo4j graph → router → typed queries → answer. Credit line: "Data: Anthropic Interviewer dataset, 500 of 1,250 interviews".

**Narration:**
> The data is five hundred interviews from the Anthropic Interviewer dataset, where people describe how they use AI at work. A local model reads each
> transcript and pulls out tasks, uses of AI, and concerns, each with a quote. A second small model checks that every quote really supports its claim.
> Similar names are merged, and everything goes into Neo4j. When you ask a question, a router picks one of a few fixed queries. No model writes database code.
> One important limit: the interviews were run by an AI and the people chose to take part, so every count describes this sample, not workers in general.

## 3. Why a graph: counting questions (1:25)

**Visual (REPLAY, labelled):** `ask_interviews "What are the top concerns among scientists?"` output: ranked concerns with counts and percentages out of 125 interviews. Then the plain-RAG answer beside it with no counts.

**Narration:**
> Here is why a graph. Ask for the top concerns among scientists, and the answer is a ranked list with counts out of one hundred twenty-five interviews.
> Plain retrieval can only show you a few similar answers, so it cannot count. On my forty test questions, it got zero of seventeen count and comparison
> questions right. The graph answered thirteen. That is the one place the extra machinery clearly earns its place.

## 4. How good is the extraction? (2:15)

**Visual (ANIM):** a bar split "correct 78%, hypothetical 12%, wrong 10%" for 90 kept edges; small chips: "AI uses 87%", "tasks 83%", "concerns 63%". Caption: "checked by a larger model, not by people".

**Narration:**
> How good is the extraction? I asked a bigger model to check ninety of the extracted facts. Seventy-eight percent were correct, and ninety percent
> if you count things the person only wished for. Concerns were the weak spot, at sixty-three percent. And recall was worse. On ten transcripts,
> the graph captured only about a third of what people actually said. So counts here are lower bounds.

## 5. The recall fix that backfired (3:10)

**Visual (ANIM):** timeline: "looser prompt for concerns" → "coverage 28% to 51%" → "sample of new edges: 49% correct, 33% wrong" → "filter at verify score 0.6" → "fresh sample: 76% correct". Caption: "the filter was chosen on one sample and tested on a different one".

**Narration:**
> So I tried to fix recall with a looser prompt for concerns. Coverage went up, but when I checked a random sample of the new facts, only forty-nine percent
> were correct and a third were wrong. I raised the verification threshold, kept about forty percent of them, and tested on a fresh sample so I wasn't grading my own homework.
> Seventy-six percent were correct. Concern coverage on those ten transcripts went from twenty-two to forty-two percent.

## 6. Routing the question (4:05)

**Visual (ANIM):** the router picking among "search, count, compare, themes, quotes, out of scope" with confidence bars; then a table "router 34 of 36, model choosing tools 31 of 36"; then a stopwatch "about two seconds".

**Narration:**
> A small decision model routes each question. It picked the right route on thirty-four of thirty-six questions, against thirty-one for a model choosing tools
> itself. Shorter route descriptions were faster but it gave up more often, so I kept the longer ones and accepted about two seconds for routing.
> On forty questions written by a different model, accuracy was about seventy-five percent, so treat it as good, not perfect.

## 7. Answers you can trust (4:50)

**Visual (REPLAY, labelled):** a validated answer with a quote and interview id; a red line "quote not found in tool output: fell back to the facts". Stat: "delivered quotes: 98 of 98 grounded; fallback 12%".

**Narration:**
> A language model writing the answer can invent a quote. So the server builds the facts itself, lets the model only phrase them, and checks every
> quote and number against the tool output. If anything doesn't match, it falls back to the plain facts. Across sixty questions, every delivered quote was
> real: ninety-eight of ninety-eight. The price is that about one answer in eight falls back to the plain text.

## 8. A small model in ollmcp (5:35)

**Visual (REPLAY, labelled):** a real ollmcp session: tool call, faithful answer. Then a red caption: "3 of 5 runs: skipped the tool, invented quotes". Then: "thinking off + clear context: 2 of 2 faithful".

**Narration:**
> Then I let a small local model use the tool in ollmcp. In a long conversation it sometimes skipped the tool and wrote quotes with made-up interview ids.
> That happened in three of five runs. With thinking switched off and the conversation cleared before each question, it relayed the answers faithfully
> in both runs. The server cannot force that. The lesson is that free chat with a small model is unvalidated, so keep the validated path for anything you publish.

## 9. Takeaways (6:25)

**Visual (ANIM):** five lines appearing one by one, then the GitHub URL.

**Narration:**
> Five things I would keep. One, a graph is worth it for counting and comparing, not for everything. Two, test any fix on a fresh sample. Three, say who judged
> your numbers; mine were a larger model, confirmed by me. Four, check what a model hands you against the source, every time. And five, say how much of the
> data you used. This was five hundred of twelve hundred fifty interviews. The code and every result are on GitHub, linked below.

---

## Upload text (draft)

**Title:** I built a graph RAG over 500 AI interviews (and checked it honestly)

**Description:** A local graph-RAG over 500 of the 1,250 Anthropic Interviewer transcripts: Ollama (qwen3:8b, nomic-embed-text), a small decision model as router, Neo4j, and ollmcp.
What worked (counting and comparing), what didn't (a looser extraction prompt, an unvalidated small client model), and how it was checked. All scores are model-judged, one run each, on a sample.
Data: Anthropic/AnthropicInterviewer (credit: Anthropic). Code and write-up: https://github.com/tuwallace/graph-rag. Narration is synthetic.

**Chapters:** 0:00 Hook, 0:31 What I built, 1:17 Why a graph, 1:50 Extraction quality, 2:20 The recall fix that backfired, 2:54 Routing, 3:25 Answers you can trust, 3:57 A small model in ollmcp, 4:34 Takeaways

**Tags:** graph RAG, local LLM, Ollama, Neo4j, ollmcp, MCP, evaluation, knowledge graph, AI engineering

**Disclosure:** the narration is synthetic, so YouTube's "altered or synthetic content" label may apply.
