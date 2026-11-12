import React from "react";
import { Slide, Appear, Footnote, Narration, beat, C } from "./ui";

const S = "seg5";
const ROWS: [string, string, string, string][] = [
  ["1", "Looser prompt for concerns", "So I tried to fix recall", C.blue],
  ["2", "Coverage up: 28% → 51%", "Coverage went up", C.teal],
  ["3", "Random sample of new facts: 49% correct, 33% wrong", "only forty-nine percent", C.red],
  ["4", "Keep only verify score ≥ 0.6 (about 40% kept)", "I raised the verification threshold", C.amber],
  ["5", "Fresh sample: 76% correct", "Seventy-six percent were correct", C.teal],
  ["6", "Concern coverage, 10 transcripts: 22% → 42%", "Concern coverage on those ten", C.teal],
];
export const Backfire: React.FC = () => (
  <Slide title="The recall fix that backfired">
    <Narration seg={S} />
    <div style={{ marginTop: 10 }}>
      {ROWS.map(([n, text, phrase, color]) => (
        <Appear key={n} at={beat(S, phrase)} style={{ display: "flex", alignItems: "center", gap: 28, margin: "20px 0" }}>
          <span style={{ width: 64, height: 64, borderRadius: 32, background: color, color: C.bg, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 36 }}>{n}</span>
          <span style={{ fontSize: 46 }}>{text}</span>
        </Appear>
      ))}
    </div>
    <Appear at={beat(S, "tested on a fresh sample")} style={{ fontSize: 34, color: C.muted, marginTop: 20 }}>
      The 0.6 threshold was chosen on one sample and tested on <b style={{ color: C.text }}>different</b> edges.
    </Appear>
    <Footnote>120-edge sample then 100-edge fresh sample, judged by a larger model {"·"} n is small, about ±9 points</Footnote>
  </Slide>
);
