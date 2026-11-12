import React from "react";
import { Slide, Appear, Footnote, Narration, beat, useProgress, C } from "./ui";

const S = "seg4";
const Seg: React.FC<{ w: number; color: string; label: string; at: number }> = ({ w, color, label, at }) => {
  const p = useProgress(at, 1);
  return <div style={{ width: `${w * 100 * p}%`, background: color, height: "100%", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 34, fontWeight: 800, color: C.bg, overflow: "hidden", whiteSpace: "nowrap" }}>{p > 0.9 ? label : ""}</div>;
};
export const Extraction: React.FC = () => (
  <Slide title="How good is the extraction?">
    <Narration seg={S} />
    <Appear at={beat(S, "I asked a bigger model")} style={{ fontSize: 34, color: C.muted, marginTop: 6 }}>90 extracted facts checked by qwen2.5:32b (30 AI uses, 30 tasks, 30 concerns)</Appear>
    <div style={{ marginTop: 40, display: "flex", height: 130, borderRadius: 20, overflow: "hidden", border: `2px solid ${C.panelLine}`, background: C.panel }}>
      <Seg w={70 / 90} color={C.teal} label="correct 78%" at={beat(S, "Seventy-eight percent")} />
      <Seg w={11 / 90} color={C.amber} label="12%" at={beat(S, "ninety percent")} />
      <Seg w={9 / 90} color={C.red} label="10%" at={beat(S, "ninety percent") + 0.4} />
    </div>
    <Appear at={beat(S, "ninety percent")} style={{ fontSize: 36, color: C.muted, marginTop: 14 }}>
      <span style={{ color: C.amber }}>amber</span> = only a wish or a prediction. Correct or hypothetical: <b style={{ color: C.text }}>90%</b>
    </Appear>
    <div style={{ display: "flex", gap: 40, marginTop: 50 }}>
      <Appear at={beat(S, "Concerns were the weak spot")} style={{ flex: 1 }}>
        <div style={{ background: C.panel, borderRadius: 22, padding: "28px 36px", border: `2px solid ${C.panelLine}`, fontSize: 36, lineHeight: 1.6 }}>
          Correct by kind<br />AI uses <b style={{ color: C.teal }}>87%</b> {"·"} tasks <b style={{ color: C.teal }}>83%</b> {"·"} concerns <b style={{ color: C.red }}>63%</b>
        </div>
      </Appear>
      <Appear at={beat(S, "And recall was worse")} style={{ flex: 1 }}>
        <div style={{ background: C.panel, borderRadius: 22, padding: "28px 36px", border: `2px solid ${C.red}`, fontSize: 36, lineHeight: 1.6 }}>
          Recall (10 transcripts)<br /><b style={{ color: C.red, fontSize: 64 }}>about a third</b> <span style={{ color: C.muted }}>of what people said</span>
        </div>
      </Appear>
    </div>
    <Appear at={beat(S, "So counts here are lower bounds")} style={{ fontSize: 44, marginTop: 40 }}>So every count is a <b style={{ color: C.amber }}>lower bound</b>.</Appear>
    <Footnote>Judged by a larger model, labels confirmed by me {"·"} one run {"·"} 500 interviews</Footnote>
  </Slide>
);
