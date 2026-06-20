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
    """Save session to Firebase under user's private subcollection"""
    username = name.strip().lower()
    save_session_db(
        username, score, duration_minutes,
        stress, confusion, boreout, engagement
    )

def load_sessions():
    """Load all sessions - anonymized for global benchmarking"""
    return get_all_sessions()

def get_patterns():
    """Legacy function - returns None. Use get_user_patterns_for(username) instead."""
    return None

def get_user_patterns_for(username):
    """
    Get study patterns for a specific user.
    Properly isolated - only returns this user's data.
    """
    if not username:
        return {}
    username = username.strip().lower()
    return get_user_patterns(username)