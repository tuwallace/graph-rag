import React from "react";
import { Slide, Appear, Narration, beat, C } from "./ui";

const S = "seg2";
const STEPS: [string, string, string][] = [
  ["Transcript", "500 of 1,250 AI-led interviews", "The data is"],
  ["Extract", "qwen3 8B finds tasks, AI uses, concerns + a quote", "A local model reads"],
  ["Verify", "nimble checks the quote supports the claim", "A second small model"],
  ["Merge", "similar names become one concept", "Similar names are merged"],
  ["Neo4j graph", "interviews, segments, concepts", "everything goes into Neo4j"],
  ["Router", "picks one of a few fixed queries", "When you ask a question"],
  ["Typed query", "counts, compares, quotes, themes", "No model writes database code"],
];
export const Pipeline: React.FC = () => (
  <Slide title="From interview transcript to answer">
    <Narration seg={S} />
    <div style={{ display: "flex", alignItems: "flex-start", gap: 14, marginTop: 40 }}>
      {STEPS.map(([t, d, phrase], i) => (
        <React.Fragment key={t}>
          <Appear at={beat(S, phrase)} style={{ width: 232 }}>
            <div style={{ background: C.panel, border: `2px solid ${i === 4 ? C.teal : C.panelLine}`, borderRadius: 18, padding: "24px 12px", textAlign: "center", fontSize: 32, fontWeight: 700, minHeight: 96, display: "flex", alignItems: "center", justifyContent: "center" }}>{t}</div>
            <div style={{ fontSize: 23, color: C.muted, textAlign: "center", marginTop: 14, lineHeight: 1.3 }}>{d}</div>
          </Appear>
          {i < STEPS.length - 1 && <Appear at={beat(S, STEPS[i + 1][2]) - 0.1} style={{ fontSize: 40, color: C.muted, marginTop: 26 }}>{"→"}</Appear>}
        </React.Fragment>
      ))}
    </div>
    <Appear at={beat(S, "One important limit")} dur={1} style={{ marginTop: 90, background: C.panel, border: `2px solid ${C.amber}`, borderRadius: 22, padding: "30px 44px", fontSize: 40, lineHeight: 1.35 }}>
      <span style={{ color: C.amber, fontWeight: 800 }}>Limit: </span>AI-led interviews, volunteers, 500 of 1,250. Every count describes <b>this sample</b>, not workers in general.
    </Appear>
  </Slide>
);
