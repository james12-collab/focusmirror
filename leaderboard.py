import json
import os
import time

LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_score(name, score, session_minutes):
    board = load_leaderboard()
    entry = {
        "name":            name,
        "score":           score,
        "session_minutes": round(session_minutes, 1),
        "timestamp":       time.strftime("%d %b, %I:%M %p")
    }
    board.append(entry)
    board = sorted(board, key=lambda x: x['score'], reverse=True)
    board = board[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(board, f)
    return board

def get_leaderboard():
    return load_leaderboard()

def get_rank(score):
    board = load_leaderboard()
    for i, entry in enumerate(board):
        if entry['score'] <= score:
            return i + 1
    return len(board) + 1