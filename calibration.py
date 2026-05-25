import time
import cv2
import numpy as np
from collections import deque
from mediapipe.python.solutions import face_mesh as mp_face_mesh
from posture import get_posture_score

LEFT_EYE  = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33,  160, 158, 133, 153, 144]

def eye_aspect_ratio(landmarks, indices, w, h):
    pts = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in indices]
    v1 = np.linalg.norm(np.array(pts[1]) - np.array(pts[5]))
    v2 = np.linalg.norm(np.array(pts[2]) - np.array(pts[4]))
    hz = np.linalg.norm(np.array(pts[0]) - np.array(pts[3]))
    return (v1 + v2) / (2.0 * hz)

class Calibrator:
    def __init__(self):
        self.is_calibrated   = False
        self.is_calibrating  = False
        self.progress        = 0        # 0-100
        self.baseline_blink  = 15       # default
        self.baseline_posture = 100     # default
        self.ear_threshold   = 0.22     # default
        self.status_message  = "Not calibrated — using defaults"

    def start_calibration(self, cap, face_mesh):
        self.is_calibrating = True
        self.status_message = "Calibrating... sit normally"
        self.progress       = 0

        ear_values    = []
        posture_values = []
        blink_times   = []
        ear_prev      = 0.3
        duration      = 60  # seconds
        start         = time.time()

        while time.time() - start < duration:
            ret, frame = cap.read()
            if not ret:
                continue

            elapsed  = time.time() - start
            self.progress = int((elapsed / duration) * 100)

            h, w = frame.shape[:2]
            rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:
                lm  = results.multi_face_landmarks[0].landmark
                ear = (eye_aspect_ratio(lm, LEFT_EYE, w, h) +
                       eye_aspect_ratio(lm, RIGHT_EYE, w, h)) / 2
                ear_values.append(ear)

                if ear < 0.22 and ear_prev >= 0.22:
                    blink_times.append(time.time())
                ear_prev = ear

            posture = get_posture_score(frame)
            posture_values.append(posture)

            # Draw progress on frame
            remaining = int(duration - elapsed)
            cv2.putText(frame, f"Calibrating: {self.progress}%", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 150), 2)
            cv2.putText(frame, f"Sit normally! {remaining}s left", (10, 65),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

            # Draw progress bar
            bar_w = int((self.progress / 100) * (w - 40))
            cv2.rectangle(frame, (20, h-40), (w-20, h-20), (50,50,50), -1)
            cv2.rectangle(frame, (20, h-40), (20+bar_w, h-20), (0,255,150), -1)

            cv2.imshow("FocusMirror Calibration", frame)
            cv2.waitKey(1)

        cv2.destroyAllWindows()

        # Calculate baselines
        if ear_values:
            self.ear_threshold   = np.percentile(ear_values, 20)
            self.baseline_blink  = len(blink_times)  # blinks in 60s = per minute
        if posture_values:
            self.baseline_posture = np.mean(posture_values)

        self.is_calibrated  = True
        self.is_calibrating = False
        self.progress       = 100
        self.status_message = (f"Calibrated! Blink baseline: {self.baseline_blink}/min | "
                               f"Posture baseline: {int(self.baseline_posture)}")
        print(f"[Calibration done] {self.status_message}")

    def get_info(self):
        return {
            "is_calibrated":    self.is_calibrated,
            "is_calibrating":   self.is_calibrating,
            "progress":         self.progress,
            "status_message":   self.status_message,
            "baseline_blink":   self.baseline_blink,
            "baseline_posture": int(self.baseline_posture)
        }