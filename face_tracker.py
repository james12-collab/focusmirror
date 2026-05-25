import cv2
from mediapipe.python.solutions import face_mesh as mp_face_mesh
import numpy as np

face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, min_detection_confidence=0.7)

LEFT_EYE  = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33,  160, 158, 133, 153, 144]

def eye_aspect_ratio(landmarks, indices, w, h):
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]
    v1 = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    v2 = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    hz = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    return (v1 + v2) / (2.0 * hz)

cap = cv2.VideoCapture(0)
blink_count = 0
ear_prev = 0.3

while True:
    ret, frame = cap.read()
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark
        ear = (eye_aspect_ratio(lm, LEFT_EYE, w, h) +
               eye_aspect_ratio(lm, RIGHT_EYE, w, h)) / 2

        if ear < 0.22 and ear_prev >= 0.22:
            blink_count += 1

        ear_prev = ear

        cv2.putText(frame, f"EAR: {ear:.2f}  Blinks: {blink_count}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Blink Detector", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()