import React from "react";
import { Composition } from "remotion";
import { W, H, FPS, clipSeconds } from "./ui";
import { Hook } from "./Hook";
import { Pipeline } from "./Pipeline";
import { Extraction } from "./Extraction";
import { Backfire } from "./Backfire";
import { Routing } from "./Routing";
import { Takeaways } from "./Takeaways";
import { Thumbnail } from "./Thumbnail";
import { Seg3, Seg7, Seg8 } from "./LiveSegs";

// Each clip is as long as its narration audio (+2 s) -- see ../narration/build_narration.py and ../../script.md.
const CLIPS = [
  { id: "Hook", c: Hook, seg: "seg1" }, { id: "Pipeline", c: Pipeline, seg: "seg2" }, { id: "Seg3", c: Seg3, seg: "seg3" },
  { id: "Extraction", c: Extraction, seg: "seg4" }, { id: "Backfire", c: Backfire, seg: "seg5" }, { id: "Routing", c: Routing, seg: "seg6" },
  { id: "Seg7", c: Seg7, seg: "seg7" }, { id: "Seg8", c: Seg8, seg: "seg8" }, { id: "Takeaways", c: Takeaways, seg: "seg9" },
];
export const Root: React.FC = () => (
  <>
    {CLIPS.map((k) => <Composition key={k.id} id={k.id} component={k.c} durationInFrames={Math.ceil(clipSeconds(k.seg) * FPS)} fps={FPS} width={W} height={H} />)}
    <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={FPS} width={1280} height={720} />
  </>
);
