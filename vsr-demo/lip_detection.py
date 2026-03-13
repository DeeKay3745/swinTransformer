import cv2
import mediapipe as mp

input_video = "public/final.mp4"
output_video = "public/lip_detect.avi"

mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture(input_video)

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

with mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True
) as face_mesh:

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:

            face = results.multi_face_landmarks[0]

            lip_ids = [
                61,146,91,181,84,17,314,405,321,375,
                291,308,324,318,402,317,14,87,178,88,95
            ]

            xs = []
            ys = []

            for i in lip_ids:
                x = int(face.landmark[i].x * width)
                y = int(face.landmark[i].y * height)
                xs.append(x)
                ys.append(y)

            x1 = min(xs)
            x2 = max(xs)
            y1 = min(ys)
            y2 = max(ys)

            cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)

        out.write(frame)

cap.release()
out.release()

print("Lip detection video created")