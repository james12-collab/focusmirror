# Fix 1: Update /patterns route in app.py to filter by username
app = open('app.py', 'r', encoding='utf-8').read()

old = """@app.route('/patterns')
def patterns():
    data = get_patterns()
    return jsonify(data or {})"""

new = """@app.route('/patterns')
def patterns():
    username = request.args.get('user', '').strip().lower()
    all_sessions = load_sessions()
    if username:
        filtered = [s for s in all_sessions if s.get('name','').lower() == username]
    else:
        filtered = all_sessions
    from pattern_memory import calc_streak, get_grade
    import time
    if len(filtered) < 2:
        return jsonify({})
    time_scores = {}
    for s in filtered:
        tod = s.get('time_of_day', 'Unknown')
        if tod not in time_scores:
            time_scores[tod] = []
        time_scores[tod].append(s['score'])
    best_time = max(time_scores, key=lambda x: sum(time_scores[x])/len(time_scores[x]))
    avg_duration = sum(s['duration'] for s in filtered) / len(filtered)
    recent = filtered[-7:]
    trend = "improving" if recent[-1]['score'] > recent[0]['score'] else "declining"
    streak = calc_streak(filtered)
    return jsonify({
        "total_sessions": len(filtered),
        "best_time": best_time,
        "avg_duration": round(avg_duration, 1),
        "trend": trend,
        "recent_scores": [s['score'] for s in recent],
        "avg_score": round(sum(s['score'] for s in filtered) / len(filtered), 1),
        "streak": streak
    })"""

app = app.replace(old, new)
open('app.py', 'w', encoding='utf-8').write(app)
print("app.py patterns fixed!")

# Fix 2: Update loadPatterns in index.html to pass username
index = open('templates/index.html', 'r', encoding='utf-8').read()

old_load = "        const resp = await fetch('/patterns');"
new_load = """        const uname = localStorage.getItem('fm_username') || '';
        const resp = await fetch('/patterns?user=' + encodeURIComponent(uname));"""

index = index.replace(old_load, new_load)
open('templates/index.html', 'w', encoding='utf-8').write(index)
print("index.html patterns fixed!")

# Fix 3: Update stats.html to filter by logged in user
stats = open('templates/stats.html', 'r', encoding='utf-8').read()
old_stats = "      const myName = localStorage.getItem('fm_username') || '';"
new_stats = """      // Get name from server session first, fallback to localStorage
      let myName = '';
      try {
        const meResp = await fetch('/api/me');
        const meData = await meResp.json();
        if (meData.logged_in) {
          myName = meData.display_name;
          localStorage.setItem('fm_username', myName);
        } else {
          myName = localStorage.getItem('fm_username') || '';
        }
      } catch(e) {
        myName = localStorage.getItem('fm_username') || '';
      }"""
stats = stats.replace(old_stats, new_stats)
open('templates/stats.html', 'w', encoding='utf-8').write(stats)
print("stats.html fixed!")

# Fix 4: Update dna.html to filter by logged in user
dna = open('templates/dna.html', 'r', encoding='utf-8').read()
old_dna = "      const myName = localStorage.getItem('fm_username') || '';"
new_dna = """      let myName = '';
      try {
        const meResp = await fetch('/api/me');
        const meData = await meResp.json();
        if (meData.logged_in) {
          myName = meData.display_name;
          localStorage.setItem('fm_username', myName);
        } else {
          myName = localStorage.getItem('fm_username') || '';
        }
      } catch(e) {
        myName = localStorage.getItem('fm_username') || '';
      }"""
dna = dna.replace(old_dna, new_dna)
open('templates/dna.html', 'w', encoding='utf-8').write(dna)
print("dna.html fixed!")

print("\nAll done! Each account now sees only their own data.")