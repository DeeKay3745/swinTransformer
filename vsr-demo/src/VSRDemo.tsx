import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

type Pt = {x: number; y: number};

const faceOval: Pt[] = [
  {x: 320, y: 90},
  {x: 260, y: 120},
  {x: 220, y: 170},
  {x: 205, y: 240},
  {x: 215, y: 320},
  {x: 240, y: 390},
  {x: 285, y: 455},
  {x: 350, y: 500},
  {x: 430, y: 515},
  {x: 510, y: 500},
  {x: 575, y: 455},
  {x: 620, y: 390},
  {x: 645, y: 320},
  {x: 655, y: 240},
  {x: 640, y: 170},
  {x: 600, y: 120},
  {x: 540, y: 90},
  {x: 430, y: 70},
];

const leftEye: Pt[] = [
  {x: 305, y: 220},
  {x: 325, y: 205},
  {x: 355, y: 200},
  {x: 385, y: 208},
  {x: 400, y: 222},
  {x: 382, y: 235},
  {x: 355, y: 240},
  {x: 325, y: 235},
];

const rightEye: Pt[] = [
  {x: 460, y: 222},
  {x: 475, y: 208},
  {x: 505, y: 200},
  {x: 535, y: 205},
  {x: 555, y: 220},
  {x: 535, y: 235},
  {x: 505, y: 240},
  {x: 478, y: 235},
];

const noseBridge: Pt[] = [
  {x: 430, y: 210},
  {x: 430, y: 250},
  {x: 430, y: 290},
  {x: 430, y: 330},
];

const noseBase: Pt[] = [
  {x: 385, y: 350},
  {x: 405, y: 365},
  {x: 430, y: 372},
  {x: 455, y: 365},
  {x: 475, y: 350},
];

const lipsOuter: Pt[] = [
  {x: 340, y: 395},
  {x: 372, y: 382},
  {x: 410, y: 376},
  {x: 450, y: 378},
  {x: 492, y: 386},
  {x: 530, y: 398},
  {x: 492, y: 418},
  {x: 450, y: 430},
  {x: 410, y: 434},
  {x: 372, y: 426},
];

const lipsInner: Pt[] = [
  {x: 372, y: 398},
  {x: 408, y: 392},
  {x: 450, y: 394},
  {x: 490, y: 401},
  {x: 450, y: 414},
  {x: 408, y: 412},
];

const browLeft: Pt[] = [
  {x: 285, y: 180},
  {x: 320, y: 165},
  {x: 360, y: 160},
  {x: 398, y: 170},
];

const browRight: Pt[] = [
  {x: 462, y: 170},
  {x: 500, y: 160},
  {x: 540, y: 165},
  {x: 575, y: 180},
];

const allPoints: Pt[] = [
  ...faceOval,
  ...leftEye,
  ...rightEye,
  ...noseBridge,
  ...noseBase,
  ...lipsOuter,
  ...lipsInner,
  ...browLeft,
  ...browRight,
];

const polyline = (pts: Pt[]) => pts.map((p) => `${p.x},${p.y}`).join(" ");

const stageBox: React.CSSProperties = {
  backgroundColor: "#eef3f8",
  border: "2px solid #d7e1ec",
  borderRadius: 20,
  padding: "24px 30px",
  minWidth: 250,
  textAlign: "center",
  boxShadow: "0 10px 24px rgba(0,0,0,0.08)",
};

const cardShadow = "0 16px 40px rgba(0,0,0,0.18)";

const MeshOverlay: React.FC<{frame: number}> = ({frame}) => {
  const pulse = 0.65 + 0.25 * Math.sin(frame / 8);
  const lipPulse = 0.8 + 0.2 * Math.sin(frame / 4);

  return (
    <svg
      width={860}
      height={700}
      viewBox="0 0 860 700"
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
      }}
    >
      <g transform="translate(90,70)">
        <polyline
          points={polyline(faceOval)}
          fill="none"
          stroke={`rgba(0,255,170,${pulse})`}
          strokeWidth={2}
        />
        <polyline
          points={polyline(leftEye)}
          fill="none"
          stroke="rgba(130,200,255,0.95)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(rightEye)}
          fill="none"
          stroke="rgba(130,200,255,0.95)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(noseBridge)}
          fill="none"
          stroke="rgba(255,255,255,0.75)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(noseBase)}
          fill="none"
          stroke="rgba(255,255,255,0.75)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(browLeft)}
          fill="none"
          stroke="rgba(255,210,120,0.9)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(browRight)}
          fill="none"
          stroke="rgba(255,210,120,0.9)"
          strokeWidth={2}
        />
        <polyline
          points={polyline(lipsOuter)}
          fill="none"
          stroke={`rgba(0,255,102,${lipPulse})`}
          strokeWidth={3}
        />
        <polyline
          points={polyline(lipsInner)}
          fill="none"
          stroke={`rgba(0,255,102,${lipPulse})`}
          strokeWidth={2}
        />

        {allPoints.map((p, i) => (
          <circle
            key={i}
            cx={p.x}
            cy={p.y}
            r={
              i >=
              faceOval.length +
                leftEye.length +
                rightEye.length +
                noseBridge.length +
                noseBase.length
                ? 3.2
                : 2.4
            }
            fill={
              i >=
              faceOval.length +
                leftEye.length +
                rightEye.length +
                noseBridge.length +
                noseBase.length
                ? "rgba(0,255,102,0.95)"
                : "rgba(210,255,245,0.9)"
            }
          />
        ))}

        <rect
          x={330}
          y={365}
          width={220}
          height={82}
          rx={14}
          fill="none"
          stroke="rgba(0,255,102,0.95)"
          strokeWidth={4}
          strokeDasharray="12 8"
        />
      </g>
    </svg>
  );
};

const FrameExtraction: React.FC<{frame: number}> = ({frame}) => {
  const {fps} = useVideoConfig();
  const prog = spring({
    frame: frame - 185,
    fps,
    config: {damping: 14, stiffness: 120},
  });

  const cards = [0, 1, 2, 3];

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: "0 80px",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 70,
          fontSize: 48,
          fontWeight: 800,
        }}
      >
        Video → Frame Sequence Extraction
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 34,
        }}
      >
        <div
          style={{
            width: 340,
            borderRadius: 24,
            overflow: "hidden",
            boxShadow: cardShadow,
            border: "2px solid #dde6ef",
            backgroundColor: "#fff",
          }}
        >
          <OffthreadVideo
            src={staticFile("video.mp4")}
            startFrom={0}
            endAt={185}
          />
        </div>

        <div
          style={{
            fontSize: 82,
            fontWeight: 900,
            color: "#4a5560",
            transform: `translateX(${interpolate(prog, [0, 1], [-20, 0])}px)`,
            opacity: prog,
          }}
        >
          →
        </div>

        <div
          style={{
            display: "flex",
            gap: 22,
            alignItems: "center",
          }}
        >
          {cards.map((c) => {
            const delay = c * 6;
            const local = spring({
              frame: frame - 195 - delay,
              fps,
              config: {damping: 12, stiffness: 140},
            });

            return (
              <div
                key={c}
                style={{
                  width: 170,
                  transform: `translateY(${interpolate(local, [0, 1], [60, 0])}px) scale(${interpolate(
                    local,
                    [0, 1],
                    [0.86, 1]
                  )})`,
                  opacity: local,
                }}
              >
                <div
                  style={{
                    borderRadius: 18,
                    overflow: "hidden",
                    boxShadow: "0 12px 26px rgba(0,0,0,0.14)",
                    border: "2px solid #dde6ef",
                    backgroundColor: "#fff",
                  }}
                >
                  <OffthreadVideo
                    src={staticFile("video.mp4")}
                    startFrom={c * 10}
                    endAt={c * 10 + 20}
                  />
                </div>
                <div
                  style={{
                    marginTop: 10,
                    textAlign: "center",
                    fontSize: 24,
                    fontWeight: 700,
                    color: "#415063",
                  }}
                >
                  Frame {c + 1}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const AttentionArrow: React.FC<{frame: number; delay?: number}> = ({
  frame,
  delay = 0,
}) => {
  const travel = ((frame + delay) % 36) / 36;

  return (
    <div
      style={{
        position: "relative",
        width: 130,
        height: 26,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 11,
          left: 8,
          width: 95,
          height: 4,
          borderRadius: 999,
          background: "linear-gradient(90deg, #93a5b5, #56687a)",
        }}
      />
      <div
        style={{
          position: "absolute",
          right: 0,
          top: 2,
          fontSize: 24,
          fontWeight: 900,
          color: "#56687a",
        }}
      >
        →
      </div>
      <div
        style={{
          position: "absolute",
          top: 7,
          left: 10 + travel * 78,
          width: 12,
          height: 12,
          borderRadius: 999,
          backgroundColor: "#00c853",
          boxShadow: "0 0 14px rgba(0,200,83,0.9)",
        }}
      />
    </div>
  );
};

const TransformerPipeline: React.FC<{frame: number}> = ({frame}) => {
  const {fps} = useVideoConfig();
  const appear = spring({
    frame: frame - 235,
    fps,
    config: {damping: 14, stiffness: 120},
  });

  const blocks = [
    "Lip Frames",
    "Swin Visual Encoder",
    "Temporal Transformer",
    "CTC / Decoder",
  ];

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
        transform: `scale(${interpolate(appear, [0, 1], [0.94, 1])})`,
        opacity: appear,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 70,
          fontSize: 48,
          fontWeight: 800,
        }}
      >
        Transformer-based VSR Inference
      </div>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 14,
          flexWrap: "nowrap",
        }}
      >
        {blocks.map((b, i) => (
          <React.Fragment key={b}>
            <div style={stageBox}>
              <div
                style={{
                  fontSize: 36,
                  fontWeight: 800,
                  color: "#233446",
                }}
              >
                {b}
              </div>
              <div
                style={{
                  marginTop: 12,
                  height: 8,
                  borderRadius: 999,
                  background:
                    i === 0
                      ? "linear-gradient(90deg,#00c853,#b9f6ca)"
                      : i === 1
                      ? "linear-gradient(90deg,#3b82f6,#93c5fd)"
                      : i === 2
                      ? "linear-gradient(90deg,#8b5cf6,#c4b5fd)"
                      : "linear-gradient(90deg,#f59e0b,#fde68a)",
                }}
              />
            </div>

            {i !== blocks.length - 1 && (
              <AttentionArrow frame={frame} delay={i * 9} />
            )}
          </React.Fragment>
        ))}
      </div>

      <div
        style={{
          position: "absolute",
          bottom: 90,
          fontSize: 30,
          color: "#46576a",
          fontWeight: 700,
          letterSpacing: 0.5,
        }}
      >
        Attention flow · temporal aggregation · sequence decoding
      </div>
    </AbsoluteFill>
  );
};

const OutputTyping: React.FC<{frame: number}> = ({frame}) => {
  const full =
    "नमस्ते, आपका स्वागत है Speech Lab @ Dhirubhai Ambani University, गांधीनगर।";
  const start = 285;
  const chars = Math.max(
    0,
    Math.min(full.length, Math.floor((frame - start) / 1.6))
  );
  const text = full.slice(0, chars);
  const cursorOn = Math.floor(frame / 10) % 2 === 0;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "center",
        alignItems: "center",
        padding: 80,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 72,
          fontSize: 48,
          fontWeight: 800,
        }}
      >
        Recognized Hindi Text
      </div>

      <div
        style={{
          width: 1280,
          minHeight: 260,
          backgroundColor: "#f7fff8",
          border: "2px solid #cfead5",
          borderRadius: 28,
          padding: "40px 46px",
          boxShadow: "0 14px 34px rgba(0,0,0,0.08)",
        }}
      >
        <div
          style={{
            fontSize: 26,
            fontWeight: 700,
            color: "#526170",
            marginBottom: 18,
          }}
        >
          Decoder Output
        </div>

        <div
          style={{
            fontSize: 56,
            fontWeight: 800,
            color: "#118a32",
            lineHeight: 1.35,
            whiteSpace: "pre-wrap",
          }}
        >
          {text}
          <span style={{opacity: cursorOn ? 1 : 0}}>|</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const VSRDemo: React.FC = () => {
  const frame = useCurrentFrame();

  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#ffffff",
        fontFamily: "Arial, Helvetica, sans-serif",
      }}
    >
      {/* Scene 1: Input avatar video */}
      <Sequence from={0} durationInFrames={185}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: 760,
              borderRadius: 24,
              overflow: "hidden",
              boxShadow: cardShadow,
              border: "2px solid #dde6ef",
              backgroundColor: "#fff",
            }}
          >
            <OffthreadVideo
              src={staticFile("video.mp4")}
              startFrom={0}
              endAt={185}
            />
          </div>

          <div
            style={{
              position: "absolute",
              top: 60,
              fontSize: 48,
              fontWeight: 800,
              opacity: titleOpacity,
            }}
          >
            Input Talking Video
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* Scene 2: MediaPipe + landmark mesh overlay */}
      <Sequence from={60} durationInFrames={125}>
        <AbsoluteFill
          style={{
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <div
            style={{
              width: 860,
              height: 700,
              position: "relative",
              borderRadius: 24,
              overflow: "hidden",
              boxShadow: cardShadow,
              border: "2px solid #dde6ef",
              backgroundColor: "#000",
            }}
          >
            <OffthreadVideo
              src={staticFile("out/facial_features_fixed.mp4")}
              style={{width: "100%", height: "100%", objectFit: "cover"}}
            />
            <MeshOverlay frame={frame} />
          </div>

          <div
            style={{
              position: "absolute",
              top: 50,
              backgroundColor: "rgba(0,0,0,0.74)",
              color: "white",
              padding: "14px 24px",
              borderRadius: 14,
              fontSize: 36,
              fontWeight: 700,
            }}
          >
            MediaPipe 468 Landmark Mesh + Lip Region Focus
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* Scene 3: Video -> frames */}
      <Sequence from={185} durationInFrames={50}>
        <FrameExtraction frame={frame} />
      </Sequence>

      {/* Scene 4: Transformer attention */}
      <Sequence from={235} durationInFrames={50}>
        <TransformerPipeline frame={frame} />
      </Sequence>

      {/* Scene 5: Output typing */}
      <Sequence from={285} durationInFrames={60}>
        <OutputTyping frame={frame} />
      </Sequence>
    </AbsoluteFill>
  );
};