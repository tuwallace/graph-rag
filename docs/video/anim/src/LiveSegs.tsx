import React from "react";
import { beat, C } from "./ui";
import { Ev, TerminalScene } from "./Terminal";
import cap from "./captures.json";

// Terminal replays of REAL captured output (docs/video/demo/*), timed to the narration with beat(). Annotation lines in amber/teal are labelled as such.
const typeEnd = (at: number, text: string, cps: number) => at + text.length / cps;

export const Seg3: React.FC = () => {
  const S = "seg3", g = beat(S, "Ask for the top concerns"), plain = beat(S, "Plain retrieval can only");
  const cmd1 = "python docs/video/demo/seg3_counts.py", cmd2 = "python docs/video/demo/seg3_counts.py plain";
  const ev: Ev[] = [
    { kind: "type", at: 0.3, text: cmd1, cps: 40 },
    { kind: "print", at: g + 0.2, text: cap.seg3_graph, reveal: 1.4 },
    { kind: "hl", at: beat(S, "a ranked list"), until: plain - 0.2, match: ["hallucinations", "reliability", "ai inaccuracy"] },
    { kind: "clear", at: plain - 0.1 },
    { kind: "type", at: plain, text: cmd2, cps: 45 },
    { kind: "print", at: typeEnd(plain, cmd2, 45) + 0.3, text: cap.seg3_plain, reveal: 0.8 },
    { kind: "hl", at: beat(S, "so it cannot count"), until: beat(S, "On my forty test"), match: ["-> 5 similar answers"] },
    { kind: "print", at: beat(S, "On my forty test"), text: "\n[annotation from docs/08, 40 test questions, 17 count/compare]\n  plain vector search: 0 of 17 correct", color: "#ff6b6b" },
    { kind: "print", at: beat(S, "The graph answered thirteen"), text: "  graph + router:      13 of 17 correct", color: "#38d3c2" },
  ];
  return <TerminalScene seg={S} events={ev} label="Terminal replay of real captured output (not a live screen recording). The last three lines are an annotation." />;
};

export const Seg7: React.FC = () => {
  const S = "seg7", cmd = "python docs/video/demo/seg7_grounded.py", go = beat(S, "So the server builds");
  const ev: Ev[] = [
    { kind: "type", at: 0.3, text: cmd, cps: 40 },
    { kind: "print", at: go, text: cap.seg7, reveal: 2.6 },
    { kind: "hl", at: beat(S, "If anything doesn't match"), until: beat(S, "Across sixty questions"), match: ["source=rendered_fallback", "issue: quote not in tool output"] },
    { kind: "print", at: beat(S, "Across sixty questions"), text: "\n[annotation, 60 questions] delivered quotes grounded: 98 of 98", color: "#38d3c2" },
    { kind: "print", at: beat(S, "The price is"), text: "[annotation] answers that fell back to the plain facts: 6 of 52 (about 1 in 8)", color: "#ffc857" },
  ];
  return <TerminalScene seg={S} events={ev} label="Terminal replay of real captured output (not a live screen recording). Output trimmed; annotation lines at the end." />;
};

export const Seg8: React.FC = () => {
  const S = "seg8", g = cap.seg8.good, b = cap.seg8.bad;
  const tool = (q: string) => `  tool call: interview-graph.ask_interviews {"question": "${q}"}`;
  const t1 = beat(S, "Then I let a small"), t2 = beat(S, "In a long conversation"), t3 = beat(S, "That happened in three"), t4 = beat(S, "With thinking switched off");
  const ev: Ev[] = [
    { kind: "type", at: 0.3, text: "ollmcp -j mcp.json -m qwen3:8b", cps: 40 },
    { kind: "type", at: t1 + 1.2, text: g.question, cps: 40, prompt: "qwen3/1-tool> " },
    { kind: "print", at: t1 + 3.2, text: g.tool_called ? tool(g.question) : "  (no tool call)", color: "#9aa6bd" },
    { kind: "print", at: t1 + 3.8, text: g.answer.join("\n"), reveal: 1.4 },
    { kind: "clear", at: t2 - 0.1 },
    { kind: "type", at: t2, text: b.question, cps: 40, prompt: "qwen3/1-tool> " },
    { kind: "print", at: t2 + 1.4, text: b.tool_called ? tool(b.question) : "  (no tool call)", color: "#ff6b6b" },
    { kind: "print", at: t2 + 2.0, text: b.answer.join("\n"), reveal: 1.4, color: "#ff9b9b" },
    { kind: "hl", at: t2 + 3.4, until: t3, match: ["science_0123", "science_0456", "creative_0789"] },
    { kind: "print", at: t3, text: "\n[annotation] ids above were never returned by the tool. Skipped the tool and invented quotes: 3 of 5 runs", color: "#ffc857" },
    { kind: "print", at: t4, text: "[annotation] thinking off + conversation cleared before each question: faithful in 2 of 2 runs", color: "#38d3c2" },
  ];
  return <TerminalScene seg={S} events={ev} label="Terminal replay of real captured ollmcp output (not a live screen recording). Annotation lines at the end." />;
};
