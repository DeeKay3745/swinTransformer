import React from "react";
import {Composition} from "remotion";
import {VSRDemo} from "./VSRDemo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VSRDemo"
        component={VSRDemo}
        durationInFrames={450}
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};