import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=3,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Lip landmark indexes
LIP_INDEXES = [
    61,146,91,181,84,17,314,405,321,375,
    291,308,324,318,402,317,14,87,178,88,95,
    78,95,88,178,87,14,317,402,318,324,
    308,415,310,311,312,13,82,81,80,191
]

# Load video
cap = cv2.VideoCapture("./lipdetection/PixVerse_V5.6_Image_Text_360P_generate_a_video.mp4")

# Get video properties
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Output video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("lip_output.mp4", fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    h, w, _ = frame.shape

    # Black output frame
    output = np.zeros_like(frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lip_points = []

            for idx in LIP_INDEXES:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                lip_points.append([x, y])

            lip_points = np.array(lip_points)

            # Bounding box
            x_min, y_min = np.min(lip_points, axis=0)
            x_max, y_max = np.max(lip_points, axis=0)

            padding = 15
            x_min = max(0, x_min - padding)
            y_min = max(0, y_min - padding)
            x_max = min(w, x_max + padding)
            y_max = min(h, y_max + padding)

            # Copy lip rectangle
            output[y_min:y_max, x_min:x_max] = frame[y_min:y_max, x_min:x_max]

    out.write(output)

    cv2.imshow("Lip Rectangle Video", output)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
out.release()
cv2.destroyAllWindows()