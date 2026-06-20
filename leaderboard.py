from firebase_db import (
    save_score_db, get_leaderboard_db,
    reset_leaderboard_db, get_rank_db
)

def save_score(name, score, session_minutes):
    save_score_db(name, score, session_minutes)

def get_leaderboard():
    return get_leaderboard_db()

def get_rank(score):
    return get_rank_db(score)

def reset_leaderboard():
    reset_leaderboard_db()