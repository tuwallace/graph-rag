import React from "react";
import { AbsoluteFill } from "remotion";
import { C, FONT } from "./ui";
export const Thumbnail: React.FC = () => (
  <AbsoluteFill style={{ background: C.bg, fontFamily: FONT, color: C.text, padding: "60px 70px" }}>
    <div style={{ fontSize: 96, fontWeight: 900, letterSpacing: -3, lineHeight: 1.02 }}>Graph RAG over<br /><span style={{ color: C.teal }}>500 AI interviews</span></div>
    <div style={{ display: "flex", gap: 34, marginTop: 56 }}>
      <div style={{ background: C.panel, border: `4px solid ${C.red}`, borderRadius: 22, padding: "16px 36px" }}><div style={{ fontSize: 30, color: C.muted }}>plain vector search</div><div style={{ fontSize: 84, fontWeight: 900, color: C.red }}>0 / 17</div></div>
      <div style={{ background: C.panel, border: `4px solid ${C.teal}`, borderRadius: 22, padding: "16px 36px" }}><div style={{ fontSize: 30, color: C.muted }}>graph + router</div><div style={{ fontSize: 84, fontWeight: 900, color: C.teal }}>13 / 17</div></div>
    </div>
    <div style={{ position: "absolute", left: 70, bottom: 44, fontSize: 34, color: C.amber, fontWeight: 700 }}>and how often my own checks were wrong</div>
  </AbsoluteFill>
);
