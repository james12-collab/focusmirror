code = open('app.py', 'w', encoding='utf-8')
code.write("""import time
import threading
import json
from flask import Flask, Response, render_template, jsonify, request, session, redirect
from flask_socketio import SocketIO, join_room, emit
from scorer import FocusScorer
from tab_monitor import TabMonitor
from leaderboard import save_score, get_leaderboard, get_rank
from badges import check_badges, get_all_badges
from pattern_memory import save_session, get_patterns, load_sessions
from accounts import signup, login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'focusmirror_secret_key_2024'
app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24 * 30
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

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

# ── ACCOUNT ROUTES ─────────────────────────────────
@app.route('/login-page')
def login_page():
    return render_template('login.html')

@app.route('/api/signup', methods=['POST'])
def api_signup():
    d = request.json or {}
    success, result = signup(d.get('username',''), d.get('password',''))
    if success:
        session.permanent = True
        session['display_name'] = result
        session['username'] = d['username'].strip().lower()
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})

@app.route('/api/login', methods=['POST'])
def api_login():
    d = request.json or {}
    success, result = login(d.get('username',''), d.get('password',''))
    if success:
        session.permanent = True
        session['display_name'] = result
        session['username'] = d['username'].strip().lower()
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})

@app.route('/api/logout')
def api_logout():
    session.clear()
    return redirect('/login-page')

@app.route('/api/me')
def api_me():
    if 'username' in session:
        return jsonify({
            "logged_in": True,
            "username": session['username'],
            "display_name": session['display_name']
        })
    return jsonify({"logged_in": False})

# ── SOCKET EVENTS ───────────────────────────────────
@socketio.on('join_buddy')
def handle_join_buddy(data):
    room_code = str(data.get('room_code','')).upper().strip()
    name = data.get('name','Anonymous')
    if not room_code: return
    join_room('buddy_' + room_code)
    if room_code not in buddy_rooms:
        buddy_rooms[room_code] = {}
    buddy_rooms[room_code][name] = {'score':0,'posture':100,'stress':0,'name':name}
    emit('buddy_update', buddy_rooms[room_code], room='buddy_' + room_code)

@socketio.on('buddy_score')
def handle_buddy_score(data):
    room_code = str(data.get('room_code','')).upper().strip()
    name = data.get('name','Anonymous')
    if room_code and name:
        if room_code not in buddy_rooms:
            buddy_rooms[room_code] = {}
        buddy_rooms[room_code][name] = {
            'score': data.get('score',0),
            'posture': data.get('posture',100),
            'stress': data.get('stress',0),
            'name': name
        }
        emit('buddy_update', buddy_rooms[room_code], room='buddy_' + room_code)

@socketio.on('join_class')
def handle_join_class(data):
    class_code = str(data.get('class_code','')).upper().strip()
    name = data.get('name','Anonymous')
    role = data.get('role','student')
    if not class_code: return
    join_room('class_' + class_code)
    if class_code not in class_rooms:
        class_rooms[class_code] = {}
    if role == 'student':
        class_rooms[class_code][name] = {
            'score':0,'posture':100,'stress':0,
            'name':name,'state':'STARTING','burnout_mins':None
        }
    emit('class_update', class_rooms.get(class_code,{}), room='class_' + class_code)

@socketio.on('class_score')
def handle_class_score(data):
    class_code = str(data.get('class_code','')).upper().strip()
    name = data.get('name','Anonymous')
    if class_code and name:
        if class_code not in class_rooms:
            class_rooms[class_code] = {}
        class_rooms[class_code][name] = {
            'score': data.get('score',0),
            'posture': data.get('posture',100),
            'stress': data.get('stress',0),
            'name': name,
            'state': data.get('state','TRACKING'),
            'burnout_mins': data.get('burnout_mins')
        }
        emit('class_update', class_rooms[class_code], room='class_' + class_code)

# ── MAIN ROUTES ─────────────────────────────────────
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/app')
def apppage():
    return render_template('index.html')

@app.route('/dna')
def dna():
    return render_template('dna.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/buddy')
def buddy():
    return render_template('buddy.html')

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/wrapped')
def wrapped():
    return render_template('wrapped.html')

@app.route('/api/sessions')
def api_sessions():
    return jsonify(load_sessions())

@app.route('/patterns')
def patterns():
    data = get_patterns()
    return jsonify(data or {})

@app.route('/reset', methods=['POST'])
def reset():
    global scorer, heatmap_data, last_heatmap, session_best_score
    global current_name, earned_badges, microsleep_count
    global consecutive_good_seconds, consecutive_posture_seconds, consecutive_blink_seconds
    data = request.json or {}
    name = data.get('name','Anonymous').strip()
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
        "heatmap":[],"leaderboard":get_leaderboard(),
        "badges":[],"new_badge":None,"all_badges":get_all_badges()
    })
    return jsonify({"status":"reset","leaderboard":get_leaderboard()})

@app.route('/sensor', methods=['POST'])
def sensor():
    global last_heatmap, heatmap_data, session_best_score, microsleep_count
    global consecutive_good_seconds, consecutive_posture_seconds, consecutive_blink_seconds
    try:
        d = request.json
        bpm = d.get('bpm',0)
        posture = d.get('posture',100)
        ear = d.get('ear',0.3)
        stress = d.get('stress',0)
        confusion = d.get('confusion',0)
        boreout = d.get('boreout',0)
        engagement = d.get('engagement',50)
        microsleep = d.get('microsleep',False)
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
        if score >= 70:
            consecutive_good_seconds += 2
        else:
            consecutive_good_seconds = 0
        if posture >= 95:
            consecutive_posture_seconds += 2
        else:
            consecutive_posture_seconds = 0
        if 10 <= bpm <= 20:
            consecutive_blink_seconds += 2
        else:
            consecutive_blink_seconds = 0
        if time.time() - last_heatmap >= 10:
            heatmap_data.append({"minute":round(scorer.session_minutes(),1),"score":score})
            if len(heatmap_data) > 60:
                heatmap_data.pop(0)
            last_heatmap = time.time()
        rec = burnout or scorer.get_recommendation(score, switches, tab_monitor.is_distracted)
        rank = get_rank(score)
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
            "leaderboard":get_leaderboard(),"rank":rank,
            "best_score":session_best_score,"current_name":current_name,
            "badges":updated_badges,"new_badge":new_badge,
            "all_badges":get_all_badges()
        })
        return jsonify(latest_data)
    except Exception as e:
        print(f"Sensor error: {e}")
        return jsonify({"error":str(e)}), 500

@app.route('/leaderboard')
def leaderboard():
    return jsonify(get_leaderboard())

@app.route('/reset-leaderboard', methods=['POST'])
def reset_leaderboard_route():
    from leaderboard import reset_leaderboard
    reset_leaderboard()
    return jsonify({"status":"reset","leaderboard":[]})

@app.route('/data')
def data():
    def generate():
        while True:
            yield f"data: {json.dumps(latest_data)}\\n\\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT',5000))
    print("FocusMirror running at http://127.0.0.1:5000")
    socketio.run(app, debug=False, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
""")
code.close()
print("app.py written!")