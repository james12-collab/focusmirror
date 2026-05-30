import time
from collections import deque

class FocusScorer:
    def __init__(self):
        self.score_history  = deque(maxlen=300)
        self.blink_times    = deque(maxlen=50)
        self.session_start  = time.time()
        self.last_posture   = 100
        self.last_switches  = 0

    def record_blink(self):
        self.blink_times.append(time.time())

    def blinks_per_minute(self):
        now = time.time()
        recent = [t for t in self.blink_times if now - t < 60]
        return len(recent)

    def session_minutes(self):
        return round((time.time() - self.session_start) / 60, 1)

    def compute_score(self, posture_score, switches_per_hour=0):
        self.last_posture  = posture_score
        self.last_switches = switches_per_hour

        # Posture is most reliable signal from BlazeFace
        posture_norm = posture_score / 100

        # Switch penalty
        switch_norm = max(0, 1 - switches_per_hour / 30)

        # Blink — if 0 blinks detected, don't penalize heavily
        # BlazeFace blink detection is weak so we weight it less
        bpm = self.blinks_per_minute()
        if bpm == 0:
            blink_norm = 0.6  # neutral — don't assume fatigue just because no blinks detected
        else:
            blink_norm = max(0, 1 - abs(bpm - 15) / 15)

        # Weight posture most heavily since it's most reliable
        score = int((blink_norm * 0.20 + posture_norm * 0.55 + switch_norm * 0.25) * 100)
        self.score_history.append(score)
        return score

    def predict_burnout(self):
        if len(self.score_history) < 20:
            return None
        recent  = list(self.score_history)[-10:]
        earlier = list(self.score_history)[-20:-10]
        trend   = sum(recent) / 10 - sum(earlier) / 10
        if trend < -15:
            return "⚠ Burnout risk — score dropping fast"
        return None

    def burnout_countdown(self):
        if len(self.score_history) < 20:
            return None
        recent  = list(self.score_history)[-10:]
        earlier = list(self.score_history)[-20:-10]
        avg     = sum(recent) / 10
        if avg >= 70:
            return None
        trend = sum(recent) / 10 - sum(earlier) / 10
        if trend >= 0:
            return None
        decline_per_min = abs(trend) / 2
        if decline_per_min == 0:
            return None
        mins_left = int((avg - 30) / decline_per_min)
        if mins_left <= 0:
            return 0
        if mins_left <= 30:
            return mins_left
        return None

    def get_recommendation(self, score, switches=0, is_distracted=False):
        if is_distracted:
            return "⚠ Distraction detected — close that tab and refocus"
        if switches > 20:
            return "Too many window switches — each one costs 23 min of focus"
        if score >= 70:
            return "Peak focus — tackle hardest problems now"
        elif score >= 45:
            return "Moderate fatigue — switch to revision or reading"
        else:
            return "⛔ Take a real break. Return in 15-20 minutes"

    def get_state(self, score):
        if score >= 70:
            return "FOCUSED"
        elif score >= 45:
            return "TIRING"
        else:
            return "BURNOUT"