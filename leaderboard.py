import json
import os
import time

LEADERBOARD_FILE = 'leaderboard.json'

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return {"date": today(), "scores": []}
    try:
        with open(LEADERBOARD_FILE, 'r') as f:
            data = json.load(f)
            # Auto reset if it's a new day
            if data.get("date") != today():
                return {"date": today(), "scores": []}
            return data
    except:
        return {"date": today(), "scores": []}

def today():
    return time.strftime("%Y-%m-%d")

def save_score(name, score, session_minutes):
    data = load_leaderboard()
    board = data["scores"]
    entry = {
        "name":            name,
        "score":           score,
        "session_minutes": round(session_minutes, 1),
        "timestamp":       time.strftime("%I:%M %p")
    }
    board.append(entry)
    board = sorted(board, key=lambda x: x['score'], reverse=True)
    board = board[:10]
    data["scores"] = board
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(data, f)
    return board

def get_leaderboard():
    return load_leaderboard()["scores"]

def get_rank(score):
    board = get_leaderboard()
    for i, entry in enumerate(board):
        if entry['score'] <= score:
            return i + 1
    return len(board) + 1

def reset_leaderboard():
    data = {"date": today(), "scores": []}
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(data, f)
    print("Leaderboard reset!")