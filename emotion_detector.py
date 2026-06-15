import numpy as np

def detect_emotion(landmarks, w, h):
    """
    Detect emotions from face landmarks
    Returns: stress, confusion, boreout, engagement (0-100)
    """
    
    if not landmarks:
        return 0, 0, 0, 50
    
    try:
        # Eye points
        left_eye = [landmarks[362], landmarks[385], landmarks[387], landmarks[263], landmarks[373], landmarks[380]]
        right_eye = [landmarks[33], landmarks[160], landmarks[158], landmarks[133], landmarks[153], landmarks[144]]
        
        # Eyebrow points (for confusion)
        left_brow = [landmarks[70], landmarks[63]]
        right_brow = [landmarks[300], landmarks[293]]
        
        # Mouth points (for stress/boreout)
        mouth = [landmarks[61], landmarks[291], landmarks[0], landmarks[17]]
        
        # Nose (for head tilt)
        nose = landmarks[1]
        
        # Calculate stress (eye tension + jaw tightness)
        stress = 0
        # If eyes are very open = high stress
        left_eye_open = abs(left_eye[1][1] - left_eye[4][1])
        right_eye_open = abs(right_eye[1][1] - right_eye[4][1])
        if max(left_eye_open, right_eye_open) > 0.05:
            stress += 20
        # If mouth is tight/small = stress
        mouth_open = abs(mouth[0][1] - mouth[1][1])
        if mouth_open < 0.03:
            stress += 30
        stress = min(100, stress)
        
        # Calculate confusion (raised eyebrows)
        confusion = 0
        left_brow_raise = abs(left_brow[0][1] - left_brow[1][1])
        right_brow_raise = abs(right_brow[0][1] - right_brow[1][1])
        if max(left_brow_raise, right_brow_raise) > 0.08:
            confusion += 40
        # If eyes are narrowed = confusion
        if max(left_eye_open, right_eye_open) < 0.04:
            confusion += 30
        confusion = min(100, confusion)
        
        # Calculate boreout (flat affect, little movement)
        boreout = 0
        # If mouth is neutral/closed = boreout
        if mouth_open < 0.02:
            boreout += 50
        # If eyes are half-closed = fatigue
        if max(left_eye_open, right_eye_open) < 0.035:
            boreout += 30
        boreout = min(100, boreout)
        
        # Calculate engagement (opposite of boreout)
        engagement = max(0, 100 - boreout - (stress * 0.3))
        engagement = int(engagement)
        
        return int(stress), int(confusion), int(boreout), engagement
    
    except:
        return 0, 0, 0, 50