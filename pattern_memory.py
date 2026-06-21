from firebase_db import (
    save_session_db,
    get_all_sessions,
    get_user_sessions,
    get_user_patterns,
    calc_streak
)
import time

def save_session(name, score, duration_minutes,
                 stress=0, confusion=0, boreout=0, engagement=50):
    username = name.strip().lower()
    save_session_db(
        username, score, duration_minutes,
        stress, confusion, boreout, engagement
    )

def load_sessions():
    """Returns anonymized global sessions for benchmarking"""
    return get_all_sessions()

def get_patterns():
    """Deprecated — use get_user_patterns_for(username)"""
    return None

def get_user_patterns_for(username):
    """
    Returns study patterns for a specific user only.
    Complete data isolation guaranteed.
    """
    if not username:
        return {}
    return get_user_patterns(username.strip().lower())
