from datetime import datetime, date

def calculate_readiness(sessions, exam_date_str):
    if not sessions:
        return {"readiness": 0, "grade": "F", "message": "No sessions yet!", "recommendation": "Complete at least 3 study sessions first.", "days_left": 0}
    try:
        exam_date = datetime.strptime(exam_date_str, "%Y-%m-%d").date()
        days_left = (exam_date - date.today()).days
    except:
        return {"error": "Invalid date"}
    if days_left < 0:
        return {"error": "Exam date has already passed"}
    recent = sessions[-10:]
    avg = sum(s['score'] for s in recent) / len(recent)
    if len(recent) >= 4:
        mid = len(recent) // 2
        trend = (sum(s['score'] for s in recent[mid:]) / (len(recent)-mid)) - (sum(s['score'] for s in recent[:mid]) / mid)
    else:
        trend = 0
    sesh_factor = min(len(sessions) / max(days_left/7, 1) / 5 * 20, 20)
    readiness = int(avg * 0.5 + max(0, min(20, trend+10)) + sesh_factor + min(days_left * 0.5, 10))
    readiness = max(0, min(100, readiness))
    if readiness >= 85: grade, msg = "A", "Excellent prep! Your brain is ready."
    elif readiness >= 70: grade, msg = "B", "Good prep. A few more sessions will maximize readiness."
    elif readiness >= 55: grade, msg = "C", "Average. Study more consistently."
    elif readiness >= 40: grade, msg = "D", "Below average. Increase study frequency now."
    else: grade, msg = "F", "Critical. Begin intensive study immediately."
    if days_left == 0: rec = "Exam is TODAY! Stay calm and trust your preparation."
    elif days_left == 1: rec = "Exam TOMORROW! Light revision only. Sleep by 10pm."
    elif days_left <= 3: rec = f"Only {days_left} days! Focus on weak areas only."
    elif days_left <= 7: rec = f"{days_left} days left. Do 2 focused sessions daily."
    else: rec = f"{days_left} days left. Consistent daily practice will get you to A-grade readiness."
    return {"readiness": readiness, "grade": grade, "message": msg, "recommendation": rec, "days_left": days_left, "avg_score": round(avg, 1), "sessions_count": len(sessions)}