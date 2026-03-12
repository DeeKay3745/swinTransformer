import cv2
import mediapipe as mp
import os

INPUT_VIDEO = "public/video.mp4"
OUTPUT_VIDEO = "public/out/facial_features_output.mp4"

os.makedirs("public/out", exist_ok=True)

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(INPUT_VIDEO)
if not cap.isOpened():
    raise RuntimeError(f"Could not open input video: {INPUT_VIDEO}")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25.0

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# mp4v is widely supported for OpenCV writing
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))

if not writer.isOpened():
    raise RuntimeError("Could not open VideoWriter for output MP4.")

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
) as face_mesh:

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        annotated = frame.copy()

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Full face mesh tessellation
                mp_drawing.draw_landmarks(
                    image=annotated,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_styles.get_default_face_mesh_tesselation_style(),
                )

                # Contours
                mp_drawing.draw_landmarks(
                    image=annotated,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_styles.get_default_face_mesh_contours_style(),
                )

                # Lip bounding box
                lip_ids = [
                    61,146,91,181,84,17,314,405,321,375,291,
                    78,95,88,178,87,14,317,402,318,324,308
                ]

                xs, ys = [], []
                h, w, _ = annotated.shape
                for idx in lip_ids:
                    x = int(face_landmarks.landmark[idx].x * w)
                    y = int(face_landmarks.landmark[idx].y * h)
                    xs.append(x)
                    ys.append(y)

                if xs and ys:
                    pad = 12
                    x1 = max(0, min(xs) - pad)
                    y1 = max(0, min(ys) - pad)
                    x2 = min(w - 1, max(xs) + pad)
                    y2 = min(h - 1, max(ys) + pad)
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)

        writer.write(annotated)

cap.release()
writer.release()
print(f"Saved to: {OUTPUT_VIDEO}")