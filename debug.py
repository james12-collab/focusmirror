import traceback
try:
    import cv2
    import time
    import threading
    import json
    import numpy as np
    from flask import Flask, Response, render_template, jsonify
    from mediapipe.python.solutions import face_mesh as mp_face_mesh
    from posture import get_posture_score
    from scorer import FocusScorer
    from tab_monitor import TabMonitor
    from calibration import Calibrator
    from micro_expression import MicroExpressionDetector

    print("Testing webcam...")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    cap.set(cv2.CAP_PROP_FPS, 15)
    ret, frame = cap.read()
    print(f"Webcam opened: {cap.isOpened()}, Frame read: {ret}")
    cap.release()

    print("Testing FocusScorer...")
    scorer = FocusScorer()
    print("FocusScorer OK")

    print("Testing TabMonitor...")
    tab = TabMonitor()
    print("TabMonitor OK")

    print("Testing Calibrator...")
    cal = Calibrator()
    print("Calibrator OK")

    print("Testing MicroExpression...")
    micro = MicroExpressionDetector()
    print("MicroExpression OK")

    print("All OK! Problem is in Flask startup.")

except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()