import {
AbsoluteFill,
Series,
useCurrentFrame,
interpolate
} from "remotion";

const tokenStyle: React.CSSProperties = {
padding: "10px 16px",
borderRadius: 10,
border: "2px solid #d6dee8",
background: "#eef3f8",
fontWeight: 600
};

const block: React.CSSProperties = {
padding: "16px 28px",
borderRadius: 14,
border: "2px solid #d6dee8",
background: "#ffffff",
fontWeight: 600
};

/* Hindi typing component */

const HindiTyping: React.FC = () => {

const frame = useCurrentFrame();

const text =
"नमस्ते, आपका स्वागत है स्पीच लैब @ धीरूभाई अंबानी यूनिवर्सिटी, गांधीनगर में।";

const chars = Math.floor(frame / 2);

const typed = text.slice(0, chars);

return (

<div
style={{
fontSize:52,
fontWeight:700,
color:"#1b8f3c",
width:1200,
textAlign:"center",
lineHeight:1.6
}}
>
{typed}
</div>

);

};

export const VSRDemo = () => {

const frame = useCurrentFrame();

const attention = interpolate(frame,[0,120],[0,1]);

return (

<AbsoluteFill
style={{
background:"#ffffff",
fontFamily:"Arial"
}}
>

<Series>

{/* TITLE */}

<Series.Sequence durationInFrames={60}>

<AbsoluteFill
style={{
justifyContent:"center",
alignItems:"center"
}}
>

<div
style={{
fontSize:60,
fontWeight:700
}}
>
Transformer-based Visual Speech Recognition
</div>

</AbsoluteFill>

</Series.Sequence>


{/* TOKEN INPUT */}

<Series.Sequence durationInFrames={60}>

<AbsoluteFill
style={{
justifyContent:"center",
alignItems:"center"
}}
>

<div
style={{
display:"flex",
gap:20
}}
>

<div style={tokenStyle}>Frame₁</div>
<div style={tokenStyle}>Frame₂</div>
<div style={tokenStyle}>Frame₃</div>
<div style={tokenStyle}>Frame₄</div>
<div style={tokenStyle}>Frame₅</div>

</div>

</AbsoluteFill>

</Series.Sequence>


{/* TRANSFORMER PIPELINE */}

<Series.Sequence durationInFrames={60}>

<AbsoluteFill
style={{
justifyContent:"center",
alignItems:"center"
}}
>

<div
style={{
display:"flex",
gap:40,
alignItems:"center"
}}
>

<div style={block}>Encoder</div>

<div style={{fontSize:40}}>→</div>

<div style={block}>Multi-Head Attention</div>

<div style={{fontSize:40}}>→</div>

<div style={block}>Decoder</div>

</div>

</AbsoluteFill>

</Series.Sequence>


{/* MULTI HEAD ATTENTION VISUALIZATION */}

<Series.Sequence durationInFrames={60}>

<AbsoluteFill
style={{
justifyContent:"center",
alignItems:"center"
}}
>

<div
style={{
display:"grid",
gridTemplateColumns:"repeat(4,150px)",
gap:25
}}
>

{Array.from({length:8}).map((_,i)=>{

return (

<div
key={i}
style={{
border:"2px solid #d6dee8",
borderRadius:12,
padding:14,
textAlign:"center"
}}
>

<div
style={{
marginBottom:10,
fontWeight:600
}}
>
Head {i+1}
</div>

<div
style={{
height:60,
background:`rgba(76,175,80,${Math.random()*attention})`,
borderRadius:8
}}
/>

</div>

);

})}

</div>

</AbsoluteFill>

</Series.Sequence>


{/* HINDI OUTPUT */}

<Series.Sequence durationInFrames={180}>

<AbsoluteFill
style={{
justifyContent:"center",
alignItems:"center"
}}
>

<HindiTyping />

</AbsoluteFill>

</Series.Sequence>

</Series>

</AbsoluteFill>

);

};