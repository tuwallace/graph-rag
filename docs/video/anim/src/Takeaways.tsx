import React from "react";
import { Slide, Appear, Narration, beat, C } from "./ui";

const S = "seg9";
const POINTS: [string, string][] = [
  ["A graph pays off for counting and comparing, not everything.", "One, a graph"],
  ["Test every fix on a fresh sample.", "Two, test any fix"],
  ["Say who judged your numbers.", "Three, say who judged"],
  ["Check what a model hands you against the source.", "Four, check what"],
  ["Say how much of the data you used: 500 of 1,250.", "And five, say how much"],
];
export const Takeaways: React.FC = () => (
  <Slide title="Five things I would keep">
    <Narration seg={S} />
    <div style={{ marginTop: 10 }}>
      {POINTS.map(([p, phrase], i) => (
        <Appear key={p} at={beat(S, phrase)} style={{ display: "flex", alignItems: "center", gap: 30, fontSize: 46, margin: "22px 0" }}>
          <span style={{ width: 66, height: 66, borderRadius: 33, background: C.teal, color: C.bg, fontWeight: 800, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 38 }}>{i + 1}</span>
          {p}
        </Appear>
      ))}
    </div>
    <Appear at={beat(S, "The code and every result")} style={{ marginTop: 40, fontSize: 38, color: C.muted, lineHeight: 1.5 }}>
      github.com/tuwallace/graph-rag<br />Data: Anthropic Interviewer dataset (Anthropic). Narration is a synthetic voice.
    </Appear>
  </Slide>
);
