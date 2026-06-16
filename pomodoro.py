def get_pomodoro_recommendation(score):
    if score >= 80:
        return {"duration": 35, "message": "You're in the zone! Extended to 35 min."}
    elif score >= 60:
        return {"duration": 25, "message": "Good focus. Standard 25 min session."}
    elif score >= 40:
        return {"duration": 20, "message": "Focus is low. Shortened to 20 min."}
    else:
        return {"duration": 15, "message": "Brain needs rest. 15 min session."}