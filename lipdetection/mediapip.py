import cv2

# use the new tasks-based MediaPipe API (v0.10+)
from mediapipe.tasks.python import vision

# drawing utilities are provided by the vision module
mp_drawing = vision.drawing_utils
mp_drawing_styles = vision.drawing_styles
mp_drawing_specs = mp_drawing.DrawingSpec(color=(0,255,0), thickness=1)

# simple webcam loop – this script demonstrates access to the camera.
# replace the loop body with detection code once you have a .task model.
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    cv2.imshow("My video capture", cv2.flip(image, 1))
    if cv2.waitKey(100) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# To perform face detection/landmarking, load a model with
# vision.FaceDetector.create_from_options or
# vision.FaceLandmarker.create_from_options using a .task file.