import {Composition} from "remotion";
import {PipelineDemo} from "./PipelineDemo";

export const RemotionRoot = () => {

return (

<Composition
id="PipelineDemo"
component={PipelineDemo}
durationInFrames={345}
fps={30}
width={1920}
height={1080}
/>

);

};