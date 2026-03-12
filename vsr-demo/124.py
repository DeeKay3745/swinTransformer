import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# -----------------------------
# Paths
# -----------------------------
VIDEO_PATH = "./public/video.mp4"
MODEL_PATH = "face_landmarker.task"   # Download this model from MediaPipe docs
OUTPUT_PATH = "./public/out/facial_features_output.mp4"

# -----------------------------
# MediaPipe setup
# -----------------------------
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = vision.FaceLandmarker
FaceLandmarkerOptions = vision.FaceLandmarkerOptions
VisionRunningMode = vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
)

# -----------------------------
# Open video
# -----------------------------
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise RuntimeError(f"Could not open input video: {VIDEO_PATH}")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# -----------------------------
# Helper: draw selected regions
# -----------------------------
# A few useful landmark groups for rough highlighting
LIP_IDS = [
    61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291,
    78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308
]
LEFT_EYE_IDS = [33, 133, 160, 159, 158, 157, 173, 144, 145, 153, 154, 155]
RIGHT_EYE_IDS = [362, 263, 387, 386, 385, 384, 398, 373, 374, 380, 381, 382]
FACE_OVAL_IDS = [
    10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361,
    288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149,
    150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109
]

def draw_points(frame, landmarks, point_ids, color, radius=2):
    h, w, _ = frame.shape
    for idx in point_ids:
        x = int(landmarks[idx].x * w)
        y = int(landmarks[idx].y * h)
        cv2.circle(frame, (x, y), radius, color, -1)

def draw_bbox_for_ids(frame, landmarks, point_ids, color, pad=10, thickness=2):
    h, w, _ = frame.shape
    xs, ys = [], []
    for idx in point_ids:
        xs.append(int(landmarks[idx].x * w))
        ys.append(int(landmarks[idx].y * h))
    if xs and ys:
        x1, x2 = max(0, min(xs) - pad), min(w, max(xs) + pad)
        y1, y2 = max(0, min(ys) - pad), min(h, max(ys) + pad)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)

# -----------------------------
# Process video
# -----------------------------
with FaceLandmarker.create_from_options(options) as landmarker:
    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        timestamp_ms = int((frame_idx / fps) * 1000)
        result = landmarker.detect_for_video(mp_image, timestamp_ms)

        if result.face_landmarks:
            face_landmarks = result.face_landmarks[0]

            # Draw dense facial features
            draw_points(frame, face_landmarks, FACE_OVAL_IDS, (255, 255, 0), radius=2)
            draw_points(frame, face_landmarks, LEFT_EYE_IDS, (255, 0, 0), radius=2)
            draw_points(frame, face_landmarks, RIGHT_EYE_IDS, (0, 255, 0), radius=2)
            draw_points(frame, face_landmarks, LIP_IDS, (0, 0, 255), radius=2)

            # Add lip bounding box
            draw_bbox_for_ids(frame, face_landmarks, LIP_IDS, (0, 255, 0), pad=12, thickness=2)

            # Labels
            cv2.putText(frame, "MediaPipe Facial Features", (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (20, 20, 20), 2)
            cv2.putText(frame, "Lips / Eyes / Face Oval", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (50, 50, 50), 2)

        writer.write(frame)
        frame_idx += 1

cap.release()
writer.release()
print(f"Saved: {OUTPUT_PATH}")