import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
)

# Lip landmark indices
OUTER_LIPS = [61,146,91,181,84,17,314,405,321,375,
              291,308,324,318,402,317,14,87,178,88,95]

INNER_LIPS = [78,95,88,178,87,14,317,402,318,324,
              308,415,310,311,312,13,82,81,80,191]

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape

            # Draw outer lips
            for idx in OUTER_LIPS:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            # Draw inner lips
            for idx in INNER_LIPS:
                x = int(face_landmarks.landmark[idx].x * w)
                y = int(face_landmarks.landmark[idx].y * h)
                cv2.circle(frame, (x, y), 2, (255, 0, 0), -1)

    cv2.imshow("Lip Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()