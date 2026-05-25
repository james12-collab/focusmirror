import cv2
from mediapipe.python.solutions import pose as mp_pose

pose = mp_pose.Pose(min_detection_confidence=0.6)

def get_posture_score(frame):
    import cv2
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if not results.pose_landmarks:
        return 100

    lm = results.pose_landmarks.landmark

    left_shoulder  = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    nose           = lm[mp_pose.PoseLandmark.NOSE]

    shoulder_mid_y = (left_shoulder.y + right_shoulder.y) / 2
    head_forward   = nose.y - shoulder_mid_y
    shoulder_tilt  = abs(left_shoulder.y - right_shoulder.y)

    score = 100
    if head_forward > 0.15:  score -= 30
    if shoulder_tilt > 0.05: score -= 20

    return max(0, score)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        score = get_posture_score(frame)
        cv2.putText(frame, f"Posture Score: {score}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Posture Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()