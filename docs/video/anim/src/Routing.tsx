import React from "react";
import { Slide, Appear, Footnote, Narration, beat, useProgress, C } from "./ui";

const S = "seg6";
const HB: React.FC<{ label: string; frac: number; text: string; color: string; at: number }> = ({ label, frac, text, color, at }) => {
  const p = useProgress(at, 1);
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 24, margin: "18px 0" }}>
      <div style={{ width: 360, fontSize: 32, color: C.muted }}>{label}</div>
      <div style={{ width: 700, height: 56, background: C.panel, borderRadius: 12, border: `2px solid ${C.panelLine}`, overflow: "hidden" }}><div style={{ width: `${frac * 100 * p}%`, height: "100%", background: color }} /></div>
      <div style={{ fontSize: 48, fontWeight: 800, color, opacity: p }}>{text}</div>
    </div>
  );
};
export const Routing: React.FC = () => (
  <Slide title="Routing the question">
    <Narration seg={S} />
    <Appear at={beat(S, "A small decision model")} style={{ fontSize: 36, color: C.muted }}>search {"·"} count {"·"} compare {"·"} themes {"·"} quotes {"·"} out of scope</Appear>
    <div style={{ marginTop: 34 }}>
      <Appear at={beat(S, "It picked the right route")}><HB label="Router (nimble)" frac={34 / 36} text="34 / 36" color={C.teal} at={beat(S, "It picked the right route")} /></Appear>
      <Appear at={beat(S, "against thirty-one")}><HB label="Model picks the tool" frac={31 / 36} text="31 / 36" color={C.blue} at={beat(S, "against thirty-one")} /></Appear>
    </div>
    <Appear at={beat(S, "Shorter route descriptions")} style={{ display: "flex", gap: 40, marginTop: 44 }}>
      <div style={{ flex: 1, background: C.panel, border: `2px solid ${C.panelLine}`, borderRadius: 22, padding: "26px 34px", fontSize: 34, lineHeight: 1.5 }}>
        <b>Short descriptions</b><br />faster, but it gives up more often
      </div>
      <div style={{ flex: 1, background: C.panel, border: `2px solid ${C.teal}`, borderRadius: 22, padding: "26px 34px", fontSize: 34, lineHeight: 1.5 }}>
        <b>Longer descriptions (kept)</b><br />routing p95 under <b style={{ color: C.teal }}>2 s</b>
      </div>
    </Appear>
    <Appear at={beat(S, "On forty questions")} style={{ marginTop: 40, fontSize: 40 }}>
      Fresh questions written by another model: <b style={{ color: C.amber }}>about 75%</b> in scope. <span style={{ color: C.muted }}>Good, not perfect.</span>
    </Appear>
    <Footnote>36 in-scope questions I wrote {"·"} 40 in-scope questions written by qwen2.5:32b {"·"} one run each</Footnote>
  </Slide>
);
