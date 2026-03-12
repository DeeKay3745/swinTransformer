import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

cap = cv2.VideoCapture("./public/video.mp4")

with mp_face_mesh.FaceMesh(
        static_image_mode=False,
        max_num_faces=1,
        refine_landmarks=True) as face_mesh:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)

        if results.multi_face_landmarks:
            for face in results.multi_face_landmarks:

                h, w, _ = frame.shape

                # mouth landmarks
                lip_ids = [61,146,91,181,84,17,314,405,321,375,291]

                xs = []
                ys = []

                for id in lip_ids:
                    x = int(face.landmark[id].x * w)
                    y = int(face.landmark[id].y * h)
                    xs.append(x)
                    ys.append(y)

                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)

                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)

        cv2.imshow("lip detection",frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()