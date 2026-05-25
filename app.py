import time
import threading
import json
from flask import Flask, Response, render_template, jsonify, request
from scorer import FocusScorer
from tab_monitor import TabMonitor

app = Flask(__name__)
scorer = FocusScorer()
tab_monitor = TabMonitor()

latest_data = {
    "score": 0, "bpm": 0, "posture": 100,
    "state": "STARTING", "recommendation": "Initializing...",
    "session_minutes": 0, "switches": 0, "burnout_mins": None,
    "tab_status": "MONITORING", "current_app": "",
    "expression": "Detecting...", "stress": 0, "confusion": 0,
    "zoneout": 0, "heatmap": []
}
heatmap_data = []
last_heatmap = time.time()

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

@app.route('/sensor', methods=['POST'])
def sensor():
    global last_heatmap, heatmap_data
    try:
        d = request.json
        bpm = d.get('bpm', 0)
        posture = d.get('posture', 100)
        ear = d.get('ear', 0.3)
        expression = d.get('expression', 'Neutral')
        stress = d.get('stress', 0)
        confusion = d.get('confusion', 0)
        zoneout = d.get('zoneout', 0)

        if ear < 0.22:
            scorer.record_blink()

        switches = tab_monitor.switches_per_hour()
        score = scorer.compute_score(posture, switches)
        burnout = scorer.predict_burnout()
        burnout_mins = scorer.burnout_countdown()

        if time.time() - last_heatmap >= 10:
            heatmap_data.append({
                "minute": round(scorer.session_minutes(), 1),
                "score": score
            })
            if len(heatmap_data) > 60:
                heatmap_data.pop(0)
            last_heatmap = time.time()

        rec = burnout or scorer.get_recommendation(score, switches, tab_monitor.is_distracted)

        latest_data.update({
            "score": score,
            "bpm": bpm,
            "posture": posture,
            "state": scorer.get_state(score),
            "recommendation": rec,
            "burnout_mins": burnout_mins,
            "session_minutes": scorer.session_minutes(),
            "switches": switches,
            "tab_status": tab_monitor.get_status(),
            "current_app": tab_monitor.current_app[:40],
            "heatmap": heatmap_data,
            "expression": expression,
            "stress": stress,
            "confusion": confusion,
            "zoneout": zoneout
        })

        return jsonify(latest_data)
    except Exception as e:
        print(f"Sensor error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/data')
def data():
    def generate():
        while True:
            yield f"data: {json.dumps(latest_data)}\n\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("FocusMirror running at http://127.0.0.1:5000")
    import os
port = int(os.environ.get('PORT', 5000))
app.run(debug=False, threaded=True, host='0.0.0.0', port=port)
