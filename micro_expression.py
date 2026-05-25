import cv2
import numpy as np
from mediapipe.python.solutions import face_mesh as mp_face_mesh

class MicroExpressionDetector:
    def __init__(self):
        # Landmark indices for key facial regions
        self.BROW_LEFT   = [70, 63, 105, 66, 107]
        self.BROW_RIGHT  = [336, 296, 334, 293, 300]
        self.MOUTH       = [61, 291, 13, 14, 17, 0]
        self.JAW         = [152, 148, 176, 149, 150]

        self.history     = []
        self.expression  = "Neutral"
        self.stress      = 0
        self.confusion   = 0
        self.zoneout     = 0
        self.prev_landmarks = None

    def _dist(self, p1, p2):
        return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

    def analyze(self, landmarks, w, h):
        pts = {i: (int(landmarks[i].x * w), int(landmarks[i].y * h))
               for i in self.BROW_LEFT + self.BROW_RIGHT + self.MOUTH + self.JAW}

        # Brow furrow — stress/concentration signal
        left_brow_height  = np.mean([pts[i][1] for i in self.BROW_LEFT])
        right_brow_height = np.mean([pts[i][1] for i in self.BROW_RIGHT])
        brow_avg          = (left_brow_height + right_brow_height) / 2
        brow_asymmetry    = abs(left_brow_height - right_brow_height)

        # Mouth tension — stress signal
        mouth_width  = self._dist(pts[61], pts[291])
        mouth_height = self._dist(pts[13], pts[14])
        mouth_ratio  = mouth_height / (mouth_width + 1e-6)

        # Jaw drop — confusion/surprise
        jaw_drop = pts[152][1] - pts[17][1]

        # Micro-movement — zone out detection
        current_lm = np.array([(landmarks[i].x, landmarks[i].y)
                                for i in range(468)])
        if self.prev_landmarks is not None:
            movement = np.mean(np.abs(current_lm - self.prev_landmarks))
            self.zoneout = max(0, min(100, int((1 - movement * 5000) * 100)))
        self.prev_landmarks = current_lm

        # Score each expression 0-100
        self.stress    = min(100, int(brow_asymmetry * 3 + (1 - mouth_ratio * 10) * 30))
        self.confusion = min(100, int(jaw_drop * 0.3 + brow_asymmetry * 2))

        # Determine dominant expression
        scores = {
            "Stressed":   self.stress,
            "Confused":   self.confusion,
            "Zoned out":  self.zoneout,
        }
        dominant = max(scores, key=scores.get)

        if scores[dominant] > 60:
            self.expression = dominant
        elif scores[dominant] > 30:
            self.expression = f"Slightly {dominant.lower()}"
        else:
            self.expression = "Neutral / Focused"

        self.history.append(self.expression)
        if len(self.history) > 100:
            self.history.pop(0)

        return self.expression

    def get_info(self):
        return {
            "expression": self.expression,
            "stress":     self.stress,
            "confusion":  self.confusion,
            "zoneout":    self.zoneout
        }