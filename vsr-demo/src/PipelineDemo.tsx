import {
AbsoluteFill,
useCurrentFrame,
interpolate
} from "remotion";

const block: React.CSSProperties = {
padding:"18px 30px",
borderRadius:14,
border:"2px solid #d6dee8",
background:"#eef3f8",
fontWeight:600,
fontSize:26,
minWidth:210,
textAlign:"center",
boxShadow:"0 8px 18px rgba(0,0,0,0.15)"
};

export const PipelineDemo = () => {

const frame = useCurrentFrame();

/* pipeline appearance */

const p1 = interpolate(frame,[0,20],[0,1]);
const p2 = interpolate(frame,[20,40],[0,1]);
const p3 = interpolate(frame,[40,60],[0,1]);
const p4 = interpolate(frame,[60,80],[0,1]);
const p5 = interpolate(frame,[80,100],[0,1]);

/* typing animation */

const text =
"नमस्ते, आपका स्वागत है स्पीच लैब @ धीरूभाई अंबानी यूनिवर्सिटी, गांधीनगर में।";

const chars = Math.max(0,Math.floor((frame-160)/2));
const typed = text.slice(0,chars);

return (

<AbsoluteFill
style={{
background:"#ffffff",
fontFamily:"Arial",
justifyContent:"center",
alignItems:"center"
}}
>

{/* ARCHITECTURE BOX */}

<div
style={{
border:"3px solid #4a6fa5",
borderRadius:18,
padding:"45px 60px",
width:1500,
background:"#f9fbff",
boxShadow:"0 20px 40px rgba(0,0,0,0.15)",
textAlign:"center"
}}
>

{/* TITLE */}

<div
style={{
fontSize:32,
fontWeight:700,
marginBottom:35,
color:"#4a6fa5"
}}
>
Model Architecture
</div>

{/* PIPELINE */}

<div
style={{
display:"flex",
gap:30,
justifyContent:"center",
alignItems:"center"
}}
>

<div style={{...block,opacity:p1}}>
Lip Frames
</div>

<div style={{fontSize:40,opacity:p2}}>→</div>

<div style={{...block,opacity:p2}}>
Visual Encoder
</div>

<div style={{fontSize:40,opacity:p3}}>→</div>

<div style={{...block,opacity:p3}}>
Transformer Attention
</div>

<div style={{fontSize:40,opacity:p4}}>→</div>

<div style={{...block,opacity:p4}}>
Decoder
</div>

<div style={{fontSize:40,opacity:p5}}>→</div>

<div style={{
...block,
opacity:p5,
color:"#1b8f3c"
}}>
Text Prediction
</div>

</div>

</div>

{/* ARROW */}

<div
style={{
fontSize:70,
marginTop:30,
opacity:interpolate(frame,[120,150],[0,1])
}}
>
↓
</div>

{/* OUTPUT BOX */}

<div
style={{
marginTop:20,
opacity:interpolate(frame,[150,180],[0,1]),
padding:"35px 45px",
border:"3px solid #1b8f3c",
borderRadius:18,
background:"#f6fff8",
width:1200,
textAlign:"center",
boxShadow:"0 20px 40px rgba(0,0,0,0.18)"
}}
>

<div
style={{
fontSize:26,
fontWeight:700,
marginBottom:14,
color:"#1b8f3c"
}}
>
Output
</div>

<div
style={{
fontSize:42,
fontWeight:600,
lineHeight:1.6
}}
>

{typed}

</div>

</div>

</AbsoluteFill>

);

};