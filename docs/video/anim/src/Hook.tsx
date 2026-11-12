import React from "react";
import { Slide, Appear, Footnote, Narration, beat, useProgress, C } from "./ui";

// Segment 1: each step is anchored to the phrase being spoken (see ui.tsx `beat`).
const S = "seg1";
const HBar: React.FC<{ label: string; frac: number; text: string; color: string; at: number }> = ({ label, frac, text, color, at }) => {
  const p = useProgress(at, 1.1);
  return (
    <div style={{ margin: "26px 0" }}>
      <div style={{ fontSize: 34, color: C.muted, marginBottom: 10 }}>{label}</div>
      <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
        <div style={{ width: 760, height: 64, background: C.panel, borderRadius: 14, border: `2px solid ${C.panelLine}`, overflow: "hidden" }}>
          <div style={{ width: `${frac * 100 * p}%`, height: "100%", background: color }} />
        </div>
        <div style={{ fontSize: 64, fontWeight: 800, color, opacity: p }}>{text}</div>
      </div>
    </div>
  );
};
export const Hook: React.FC = () => (
  <Slide>
    <Narration seg={S} />
    <div style={{ marginTop: 40 }}>
      <Appear at={beat(S, "I built a system")} dur={1}><div style={{ fontSize: 92, fontWeight: 800, letterSpacing: -2 }}>A graph RAG over <span style={{ color: C.teal }}>500</span> AI interviews.</div></Appear>
      <Appear at={beat(S, "Ask it which concerns")} dur={0.8} style={{ marginTop: 36, fontSize: 40, color: C.muted }}>
        “Which concerns do scientists raise most?” → it counts.
      </Appear>
    </div>
    <div style={{ marginTop: 40, background: C.panel, borderRadius: 24, padding: "30px 50px", border: `2px solid ${C.panelLine}` }}>
      <div style={{ fontSize: 30, color: C.muted }}>Count and comparison questions answered correctly (17 questions)</div>
      <Appear at={beat(S, "Plain vector search")}><HBar label="Plain vector search" frac={0} text="0 of 17" color={C.red} at={beat(S, "Plain vector search")} /></Appear>
      <Appear at={beat(S, "The graph got thirteen")}><HBar label="Graph + router" frac={13 / 17} text="13 of 17" color={C.teal} at={beat(S, "The graph got thirteen")} /></Appear>
    </div>
    <Appear at={beat(S, "But the part worth watching")} dur={1} style={{ marginTop: 34, fontSize: 44 }}>
      …but the story is how often <span style={{ color: C.amber }}>my own checks were wrong</span>.
    </Appear>
    <Footnote>Anthropic Interviewer dataset {"·"} 500 of 1,250 interviews {"·"} scores judged by a larger model, one run each</Footnote>
  </Slide>
);
