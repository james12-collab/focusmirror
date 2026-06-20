content = open('app.py', 'r', encoding='utf-8').read()

# Update patterns import
old_import = "from pattern_memory import save_session, get_patterns, load_sessions"
new_import = "from pattern_memory import save_session, get_user_patterns_for, load_sessions"
content = content.replace(old_import, new_import)

# Update patterns route to use user-specific function
old_patterns = """@app.route('/patterns')
def patterns():
    username = request.args.get('user', '').strip().lower()
    all_sessions = load_sessions()
    if username:
        filtered = [s for s in all_sessions if s.get('name','').lower() == username]
    else:
        filtered = all_sessions
    from pattern_memory import calc_streak
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
    time_avgs = {t: round(sum(v)/len(v), 1) for t, v in time_scores.items()}
    return jsonify({
        "total_sessions": len(filtered),
        "best_time": best_time,
        "avg_duration": round(avg_duration, 1),
        "trend": trend,
        "recent_scores": [s['score'] for s in recent],
        "avg_score": round(sum(s['score'] for s in filtered) / len(filtered), 1),
        "streak": streak,
        "time_avgs": time_avgs
    })"""

new_patterns = """@app.route('/patterns')
def patterns():
    username = request.args.get('user', '').strip().lower()
    if not username:
        return jsonify({})
    try:
        data = get_user_patterns_for(username)
        return jsonify(data or {})
    except Exception as e:
        print(f"Patterns error: {e}")
        return jsonify({})"""

content = content.replace(old_patterns, new_patterns)
open('app.py', 'w', encoding='utf-8').write(content)
print("pattern_memory fix applied!")