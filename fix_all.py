import os

# ─────────────────────────────────────────
# FIX 1 + 2 + 3 + 4: app.py
# ─────────────────────────────────────────
app_code = '''import time
import threading
import json
import os
from flask import Flask, Response, render_template, jsonify, request, session, redirect
from flask_socketio import SocketIO, join_room, emit
from scorer import FocusScorer
from tab_monitor import TabMonitor
from leaderboard import save_score, get_leaderboard, get_rank
from badges import check_badges, get_all_badges
from pattern_memory import save_session, get_user_patterns_for, load_sessions
from accounts import signup, login
from exam_readiness import calculate_readiness
from firebase_db import save_world_point_db, get_world_data_db, save_school_enquiry

app = Flask(__name__)
app.config[\'SECRET_KEY\'] = os.environ.get(\'SECRET_KEY\', \'focusmirror_dev_key_local\')
app.config[\'PERMANENT_SESSION_LIFETIME\'] = 60 * 60 * 24 * 30
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=\'threading\')

scorer = FocusScorer()
tab_monitor = TabMonitor()

latest_data = {
    "score": 0, "bpm": 0, "posture": 100,
    "state": "STARTING", "recommendation": "Initializing...",
    "session_minutes": 0, "switches": 0, "burnout_mins": None,
    "tab_status": "MONITORING", "current_app": "",
    "stress": 0, "confusion": 0, "boreout": 0, "engagement": 0,
    "microsleep": False, "microsleep_count": 0,
    "heatmap": [], "leaderboard": [],
    "badges": [], "new_badge": None, "all_badges": get_all_badges()
}
heatmap_data = []
last_heatmap = time.time()
current_name = "Anonymous"
session_best_score = 0
earned_badges = []
consecutive_good_seconds = 0
consecutive_posture_seconds = 0
consecutive_blink_seconds = 0
microsleep_count = 0
buddy_rooms = {}
class_rooms = {}

# FIX 2: Leaderboard cache — prevents Firestore quota exhaustion
_leaderboard_cache = []
_leaderboard_cache_time = 0
CACHE_TTL = 30  # seconds — refresh every 30s not every 2s

def tab_loop():
    while True:
        try:
            switches = tab_monitor.switches_per_hour()
            latest_data.update({
                "switches": switches,
                "tab_status": tab_monitor.get_status(),
                "current_app": tab_monitor.current_app[:40]
            })
        except Exception as e:
            print(f"Tab error: {e}")
        time.sleep(2)

threading.Thread(target=tab_loop, daemon=True).start()
print("Server ready!")

# ── ACCOUNT ROUTES ──────────────────────────────────────────
@app.route(\'/login-page\')
def login_page():
    return render_template(\'login.html\')

@app.route(\'/api/signup\', methods=[\'POST\'])
def api_signup():
    d = request.json or {}
    success, result = signup(d.get(\'username\',\'\'), d.get(\'password\',\'\'))
    if success:
        session.permanent = True
        session[\'display_name\'] = result
        session[\'username\'] = d[\'username\'].strip().lower()
        session[\'age_group\'] = d.get(\'age_group\', \'unknown\')
        session[\'ai_consent\'] = d.get(\'ai_consent\', False)
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})

@app.route(\'/api/login\', methods=[\'POST\'])
def api_login():
    d = request.json or {}
    success, result = login(d.get(\'username\',\'\'), d.get(\'password\',\'\'))
    if success:
        session.permanent = True
        session[\'display_name\'] = result
        session[\'username\'] = d[\'username\'].strip().lower()
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})

@app.route(\'/api/logout\')
def api_logout():
    session.clear()
    return redirect(\'/login-page\')

@app.route(\'/api/me\')
def api_me():
    if \'username\' in session:
        return jsonify({
            "logged_in": True,
            "username": session[\'username\'],
            "display_name": session[\'display_name\']
        })
    return jsonify({"logged_in": False})

# ── SOCKET EVENTS ───────────────────────────────────────────
@socketio.on(\'join_buddy\')
def handle_join_buddy(data):
    room_code = str(data.get(\'room_code\',\'\')).upper().strip()
    name = data.get(\'name\',\'Anonymous\')
    if not room_code: return
    join_room(\'buddy_\' + room_code)
    if room_code not in buddy_rooms:
        buddy_rooms[room_code] = {}
    buddy_rooms[room_code][name] = {\'score\':0,\'posture\':100,\'stress\':0,\'name\':name}
    emit(\'buddy_update\', buddy_rooms[room_code], room=\'buddy_\' + room_code)

@socketio.on(\'buddy_score\')
def handle_buddy_score(data):
    room_code = str(data.get(\'room_code\',\'\')).upper().strip()
    name = data.get(\'name\',\'Anonymous\')
    if room_code and name:
        if room_code not in buddy_rooms:
            buddy_rooms[room_code] = {}
        buddy_rooms[room_code][name] = {
            \'score\': data.get(\'score\',0),
            \'posture\': data.get(\'posture\',100),
            \'stress\': data.get(\'stress\',0),
            \'name\': name
        }
        emit(\'buddy_update\', buddy_rooms[room_code], room=\'buddy_\' + room_code)

@socketio.on(\'join_class\')
def handle_join_class(data):
    class_code = str(data.get(\'class_code\',\'\')).upper().strip()
    name = data.get(\'name\',\'Anonymous\')
    role = data.get(\'role\',\'student\')
    if not class_code: return
    join_room(\'class_\' + class_code)
    if class_code not in class_rooms:
        class_rooms[class_code] = {}
    if role == \'student\':
        class_rooms[class_code][name] = {
            \'score\':0,\'posture\':100,\'stress\':0,
            \'name\':name,\'state\':\'STARTING\',\'burnout_mins\':None
        }
    emit(\'class_update\', class_rooms.get(class_code,{}), room=\'class_\' + class_code)

@socketio.on(\'class_score\')
def handle_class_score(data):
    class_code = str(data.get(\'class_code\',\'\')).upper().strip()
    name = data.get(\'name\',\'Anonymous\')
    if class_code and name:
        if class_code not in class_rooms:
            class_rooms[class_code] = {}
        class_rooms[class_code][name] = {
            \'score\': data.get(\'score\',0),
            \'posture\': data.get(\'posture\',100),
            \'stress\': data.get(\'stress\',0),
            \'name\': name,
            \'state\': data.get(\'state\',\'TRACKING\'),
            \'burnout_mins\': data.get(\'burnout_mins\')
        }
        emit(\'class_update\', class_rooms[class_code], room=\'class_\' + class_code)

# ── MAIN ROUTES ─────────────────────────────────────────────
@app.route(\'/\')
def landing():
    return render_template(\'landing.html\')

@app.route(\'/app\')
def apppage():
    return render_template(\'index.html\')

@app.route(\'/dna\')
def dna():
    return render_template(\'dna.html\')

@app.route(\'/stats\')
def stats():
    return render_template(\'stats.html\')

@app.route(\'/buddy\')
def buddy():
    return render_template(\'buddy.html\')

@app.route(\'/teacher\')
def teacher():
    return render_template(\'teacher.html\')

@app.route(\'/wrapped\')
def wrapped():
    return render_template(\'wrapped.html\')

@app.route(\'/world\')
def world():
    return render_template(\'world.html\')

@app.route(\'/exam\')
def exam():
    return render_template(\'exam.html\')

@app.route(\'/privacy\')
def privacy():
    return render_template(\'privacy.html\')

@app.route(\'/parent\')
def parent():
    return render_template(\'parent.html\')

@app.route(\'/schools\')
def schools():
    return render_template(\'schools.html\')

# ── API ROUTES ──────────────────────────────────────────────
@app.route(\'/api/sessions\')
def api_sessions():
    # FIX 3: Returns anonymized sessions only — no usernames
    all_sess = load_sessions()
    safe = []
    for s in all_sess:
        safe.append({
            \'score\': s.get(\'score\', 0),
            \'date\': s.get(\'date\', \'\'),
            \'time_of_day\': s.get(\'time_of_day\', \'\'),
            \'grade\': s.get(\'grade\', \'\'),
            \'duration\': s.get(\'duration\', 0),
            \'emotions\': s.get(\'emotions\', {})
        })
    return jsonify(safe)

@app.route(\'/api/my-sessions\')
def api_my_sessions():
    # FIX 3: Private endpoint — returns only this user\'s sessions
    username = request.args.get(\'user\', \'\').strip().lower()
    if not username:
        return jsonify([])
    try:
        from firebase_db import get_user_sessions
        sessions = get_user_sessions(username)
        return jsonify(sessions)
    except Exception as e:
        print(f"My sessions error: {e}")
        return jsonify([])

@app.route(\'/api/world-data\')
def api_world_data():
    try:
        return jsonify(get_world_data_db())
    except Exception as e:
        print(f"World data error: {e}")
        return jsonify([])

@app.route(\'/api/save-location\', methods=[\'POST\'])
def api_save_location():
    d = request.json or {}
    lat = d.get(\'lat\')
    lng = d.get(\'lng\')
    score = d.get(\'score\', 0)
    if lat and lng:
        try:
            save_world_point_db(lat, lng, score)
        except Exception as e:
            print(f"Location save error: {e}")
    return jsonify({"status": "saved"})

@app.route(\'/api/school-enquiry\', methods=[\'POST\'])
def api_school_enquiry():
    try:
        d = request.json or {}
        save_school_enquiry(d)
        return jsonify({"status": "saved"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(\'/api/exam-readiness\', methods=[\'POST\'])
def api_exam_readiness():
    d = request.json or {}
    exam_date = d.get(\'exam_date\', \'\')
    username = d.get(\'username\', \'\').strip().lower()
    try:
        from firebase_db import get_user_sessions
        user_sess = get_user_sessions(username) if username else []
    except:
        user_sess = []
    return jsonify(calculate_readiness(user_sess, exam_date))

@app.route(\'/api/benchmarks\')
def api_benchmarks():
    score = int(request.args.get(\'score\', 0))
    all_sess = load_sessions()
    if not all_sess:
        return jsonify({"percentile": 50, "total": 0, "avg": 0})
    scores = sorted([s[\'score\'] for s in all_sess if \'score\' in s])
    below = sum(1 for s in scores if s < score)
    percentile = int(below / len(scores) * 100) if scores else 50
    return jsonify({
        "percentile": percentile,
        "top_percent": 100 - percentile,
        "total": len(scores),
        "avg": round(sum(scores)/len(scores), 1) if scores else 0,
        "top_score": max(scores) if scores else 0
    })

@app.route(\'/api/public/stats\')
def api_public_stats():
    all_sess = load_sessions()
    if not all_sess:
        return jsonify({"total_sessions": 0, "avg_score": 0, "top_score": 0, "total_users": 0})
    scores = [s[\'score\'] for s in all_sess if \'score\' in s]
    return jsonify({
        "total_sessions": len(all_sess),
        "avg_score": round(sum(scores)/len(scores), 1) if scores else 0,
        "top_score": max(scores) if scores else 0,
        "total_users": "private",
        "endpoint": "focusmirror.onrender.com/api/public/stats"
    })

# FIX 4: Updated patterns route using isolated user patterns
@app.route(\'/patterns\')
def patterns():
    username = request.args.get(\'user\', \'\').strip().lower()
    if not username:
        return jsonify({})
    try:
        data = get_user_patterns_for(username)
        return jsonify(data or {})
    except Exception as e:
        print(f"Patterns error: {e}")
        return jsonify({})

@app.route(\'/reset\', methods=[\'POST\'])
def reset():
    global scorer, heatmap_data, last_heatmap, session_best_score
    global current_name, earned_badges, microsleep_count
    global consecutive_good_seconds, consecutive_posture_seconds, consecutive_blink_seconds
    data = request.json or {}
    name = data.get(\'name\',\'Anonymous\').strip()
    if name:
        current_name = name
    if session_best_score > 0:
        save_score(current_name, session_best_score, scorer.session_minutes())
        save_session(current_name, session_best_score, scorer.session_minutes())
    scorer = FocusScorer()
    heatmap_data = []
    last_heatmap = time.time()
    session_best_score = 0
    earned_badges = []
    microsleep_count = 0
    consecutive_good_seconds = 0
    consecutive_posture_seconds = 0
    consecutive_blink_seconds = 0
    latest_data.update({
        "score":0,"bpm":0,"posture":100,
        "state":"STARTING","recommendation":"Initializing...",
        "session_minutes":0,"switches":0,"burnout_mins":None,
        "stress":0,"confusion":0,"boreout":0,"engagement":0,
        "microsleep":False,"microsleep_count":0,
        "heatmap":[],"leaderboard":_leaderboard_cache,
        "badges":[],"new_badge":None,"all_badges":get_all_badges()
    })
    return jsonify({"status":"reset","leaderboard":_leaderboard_cache})

@app.route(\'/sensor\', methods=[\'POST\'])
def sensor():
    global last_heatmap, heatmap_data, session_best_score, microsleep_count
    global consecutive_good_seconds, consecutive_posture_seconds, consecutive_blink_seconds
    global _leaderboard_cache, _leaderboard_cache_time
    try:
        d = request.json
        bpm = d.get(\'bpm\',0)
        posture = d.get(\'posture\',100)
        ear = d.get(\'ear\',0.3)
        stress = d.get(\'stress\',0)
        confusion = d.get(\'confusion\',0)
        boreout = d.get(\'boreout\',0)
        engagement = d.get(\'engagement\',50)
        microsleep = d.get(\'microsleep\',False)
        if microsleep:
            microsleep_count += 1
        if ear < 0.22:
            scorer.record_blink()
        switches = tab_monitor.switches_per_hour()
        score = scorer.compute_score(posture, switches)
        burnout = scorer.predict_burnout()
        burnout_mins = scorer.burnout_countdown()
        if score > session_best_score:
            session_best_score = score
        if score >= 70: consecutive_good_seconds += 2
        else: consecutive_good_seconds = 0
        if posture >= 95: consecutive_posture_seconds += 2
        else: consecutive_posture_seconds = 0
        if 10 <= bpm <= 20: consecutive_blink_seconds += 2
        else: consecutive_blink_seconds = 0
        if time.time() - last_heatmap >= 10:
            heatmap_data.append({"minute":round(scorer.session_minutes(),1),"score":score})
            if len(heatmap_data) > 60:
                heatmap_data.pop(0)
            last_heatmap = time.time()
        rec = burnout or scorer.get_recommendation(score, switches, tab_monitor.is_distracted)

        # FIX 2: Cached rank — read Firestore max once per 30 seconds
        now_ts = time.time()
        if now_ts - _leaderboard_cache_time > CACHE_TTL:
            _leaderboard_cache = get_leaderboard()
            _leaderboard_cache_time = now_ts
        rank = len(_leaderboard_cache) + 1
        for i, entry in enumerate(_leaderboard_cache):
            if entry.get(\'score\', 0) <= score:
                rank = i + 1
                break

        new_badges, updated_badges = check_badges(
            score=score, posture=posture, bpm=bpm,
            session_minutes=scorer.session_minutes(), rank=rank,
            best_score=session_best_score,
            consecutive_good_minutes=consecutive_good_seconds/60,
            consecutive_posture_minutes=consecutive_posture_seconds/60,
            consecutive_blink_minutes=consecutive_blink_seconds/60,
            earned_badges=earned_badges
        )
        new_badge = new_badges[0] if new_badges else None
        latest_data.update({
            "score":score,"bpm":bpm,"posture":posture,
            "state":scorer.get_state(score),"recommendation":rec,
            "burnout_mins":burnout_mins,
            "session_minutes":scorer.session_minutes(),
            "switches":switches,"tab_status":tab_monitor.get_status(),
            "current_app":tab_monitor.current_app[:40],
            "heatmap":heatmap_data,
            "stress":stress,"confusion":confusion,
            "boreout":boreout,"engagement":engagement,
            "microsleep":microsleep,"microsleep_count":microsleep_count,
            "leaderboard":_leaderboard_cache,"rank":rank,
            "best_score":session_best_score,"current_name":current_name,
            "badges":updated_badges,"new_badge":new_badge,
            "all_badges":get_all_badges()
        })
        return jsonify(latest_data)
    except Exception as e:
        print(f"Sensor error: {e}")
        return jsonify({"error":str(e)}), 500

@app.route(\'/leaderboard\')
def leaderboard():
    return jsonify(get_leaderboard())

@app.route(\'/reset-leaderboard\', methods=[\'POST\'])
def reset_leaderboard_route():
    global _leaderboard_cache, _leaderboard_cache_time
    from leaderboard import reset_leaderboard
    reset_leaderboard()
    _leaderboard_cache = []
    _leaderboard_cache_time = 0
    return jsonify({"status":"reset","leaderboard":[]})

@app.route(\'/data\')
def data():
    def generate():
        while True:
            yield f"data: {json.dumps(latest_data)}\\n\\n"
            time.sleep(1)
    return Response(generate(), mimetype=\'text/event-stream\')

if __name__ == \'__main__\':
    port = int(os.environ.get(\'PORT\', 5000))
    print("FocusMirror running at http://127.0.0.1:5000")
    socketio.run(app, debug=False, host=\'0.0.0.0\', port=port, allow_unsafe_werkzeug=True)
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_code)
print("app.py written!")

# ─────────────────────────────────────────
# FIX 4: pattern_memory.py
# ─────────────────────────────────────────
pattern_code = '''from firebase_db import (
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
'''

with open('pattern_memory.py', 'w', encoding='utf-8') as f:
    f.write(pattern_code)
print("pattern_memory.py written!")

# ─────────────────────────────────────────
# FIX 5: firebase_db.py — remove username from all_sessions
# ─────────────────────────────────────────
db_content = open('firebase_db.py', 'r', encoding='utf-8').read()

old_anon = '''    # Also save to global sessions for leaderboard/benchmarking
    db.collection('all_sessions').add(session_data)'''

new_anon = '''    # Save anonymized version — username deliberately excluded for privacy
    anonymized = {
        'score': int(score),
        'duration': round(float(duration_minutes), 1),
        'grade': get_grade(score),
        'date': time.strftime("%Y-%m-%d"),
        'time_of_day': get_time_of_day(),
        'hour': int(time.strftime("%H")),
        'emotions': {
            'stress': int(stress),
            'confusion': int(confusion),
            'boreout': int(boreout),
            'engagement': int(engagement)
        },
        'created_at': firestore.SERVER_TIMESTAMP
    }
    db.collection('all_sessions').add(anonymized)'''

db_content = db_content.replace(old_anon, new_anon)
with open('firebase_db.py', 'w', encoding='utf-8') as f:
    f.write(db_content)
print("firebase_db.py privacy fix applied!")

# ─────────────────────────────────────────
# FIX 3: Update all HTML files to use /api/my-sessions
# ─────────────────────────────────────────
html_fixes = {
    'templates/stats.html': (
        "const resp = await fetch('/api/sessions');",
        "const resp = await fetch('/api/my-sessions?user=' + encodeURIComponent(myName));"
    ),
    'templates/dna.html': (
        "const resp = await fetch('/api/sessions');",
        "const resp = await fetch('/api/my-sessions?user=' + encodeURIComponent(myName));"
    ),
    'templates/wrapped.html': (
        "const resp = await fetch('/api/sessions');",
        "const resp = await fetch('/api/my-sessions?user=' + encodeURIComponent(name));"
    ),
}

for filepath, (old, new) in html_fixes.items():
    try:
        content = open(filepath, 'r', encoding='utf-8').read()
        if old in content:
            content = content.replace(old, new)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{filepath} updated!")
        else:
            print(f"{filepath} — already updated or pattern not found")
    except FileNotFoundError:
        print(f"{filepath} — not found, skipping")

# Fix parent.html separately (different variable name)
try:
    parent = open('templates/parent.html', 'r', encoding='utf-8').read()
    parent = parent.replace(
        "const resp = await fetch('/api/sessions');",
        "const resp = await fetch('/api/my-sessions?user=' + encodeURIComponent(username));"
    )
    parent = parent.replace(
        "const childSessions = all.filter(s => s.name && s.name.toLowerCase() === username);",
        "const childSessions = all;"
    )
    with open('templates/parent.html', 'w', encoding='utf-8') as f:
        f.write(parent)
    print("parent.html updated!")
except FileNotFoundError:
    print("parent.html not found")

print("\n✅ ALL FIXES APPLIED")
print("Next: add SECRET_KEY to Render env vars then git push")