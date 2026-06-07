ALL_BADGES = [
    {
        "id": "first_session",
        "icon": "🔥",
        "name": "First Session",
        "desc": "Completed your first FocusMirror session"
    },
    {
        "id": "focus_master",
        "icon": "💪",
        "name": "Focus Master",
        "desc": "Achieved a focus score of 80 or above"
    },
    {
        "id": "posture_pro",
        "icon": "🧘",
        "name": "Posture Pro",
        "desc": "Maintained perfect posture for 5 minutes"
    },
    {
        "id": "blink_champion",
        "icon": "👁",
        "name": "Blink Champion",
        "desc": "Maintained healthy blink rate for 2 minutes"
    },
    {
        "id": "top_of_board",
        "icon": "🏆",
        "name": "Top of the Board",
        "desc": "Reached #1 on the leaderboard"
    },
    {
        "id": "speed_runner",
        "icon": "⚡",
        "name": "Speed Runner",
        "desc": "Got a score within 30 seconds of starting"
    },
    {
        "id": "consistency_king",
        "icon": "🎯",
        "name": "Consistency King",
        "desc": "Stayed above 70 focus score for 3 minutes"
    },
    {
        "id": "perfect_session",
        "icon": "🌟",
        "name": "Perfect Session",
        "desc": "Ended a session with score above 85"
    }
]

def get_all_badges():
    return ALL_BADGES

def check_badges(score, posture, bpm, session_minutes, rank, 
                 best_score, consecutive_good_minutes,
                 consecutive_posture_minutes, consecutive_blink_minutes,
                 earned_badges):
    newly_earned = []

    def earn(badge_id):
        if badge_id not in earned_badges:
            earned_badges.append(badge_id)
            badge = next((b for b in ALL_BADGES if b['id'] == badge_id), None)
            if badge:
                newly_earned.append(badge)

    # First session — earned after 1 minute
    if session_minutes >= 1:
        earn('first_session')

    # Focus master — score 80+
    if score >= 80:
        earn('focus_master')

    # Posture pro — 100% posture for 5 minutes
    if consecutive_posture_minutes >= 5:
        earn('posture_pro')

    # Blink champion — healthy blink for 2 minutes
    if consecutive_blink_minutes >= 2:
        earn('blink_champion')

    # Top of the board
    if rank == 1:
        earn('top_of_board')

    # Speed runner — score within 30 seconds
    if session_minutes <= 0.5 and score > 0:
        earn('speed_runner')

    # Consistency king — above 70 for 3 minutes
    if consecutive_good_minutes >= 3:
        earn('consistency_king')

    # Perfect session — best score above 85
    if best_score >= 85:
        earn('perfect_session')

    return newly_earned, earned_badges