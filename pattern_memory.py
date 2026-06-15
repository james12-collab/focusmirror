import json
import os
import time

SESSIONS_FILE = 'sessions.json'

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return []
    try:
        with open(SESSIONS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def get_grade(score):
    if score >= 90: return "A+"
    elif score >= 80: return "A"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    elif score >= 50: return "D"
    else: return "F"

def save_session(name, score, duration_minutes):
    sessions = load_sessions()
    hour = int(time.strftime("%H"))
    if hour < 6: time_of_day = "Late Night"
    elif hour < 12: time_of_day = "Morning"
    elif hour < 17: time_of_day = "Afternoon"
    elif hour < 21: time_of_day = "Evening"
    else: time_of_day = "Night"
    session = {
        "name": name,
        "score": score,
        "duration": round(duration_minutes, 1),
        "date": time.strftime("%Y-%m-%d"),
        "time": time.strftime("%I:%M %p"),
        "time_of_day": time_of_day,
        "hour": hour,
        "grade": get_grade(score)
    }
    sessions.append(session)
    sessions = sessions[-100:]
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f)

def get_patterns():
    sessions = load_sessions()
    if len(sessions) < 2:
        return None
    time_scores = {}
    for s in sessions:
        tod = s.get('time_of_day', 'Unknown')
        if tod not in time_scores:
            time_scores[tod] = []
        time_scores[tod].append(s['score'])
    best_time = max(time_scores, key=lambda x: sum(time_scores[x])/len(time_scores[x]))
    avg_duration = sum(s['duration'] for s in sessions) / len(sessions)
    recent = sessions[-7:]
    if len(recent) >= 2:
        trend = "improving" if recent[-1]['score'] > recent[0]['score'] else "declining"
    else:
        trend = "not enough data"
    return {
        "total_sessions": len(sessions),
        "best_time": best_time,
        "avg_duration": round(avg_duration, 1),
        "trend": trend,
        "recent_scores": [s['score'] for s in recent],
        "avg_score": round(sum(s['score'] for s in sessions) / len(sessions), 1)
    }