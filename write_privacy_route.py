content = open('app.py', 'r', encoding='utf-8').read()

old_route = "@app.route('/exam')\ndef exam():\n    return render_template('exam.html')"
new_route = """@app.route('/exam')
def exam():
    return render_template('exam.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')"""

content = content.replace(old_route, new_route)

# Update signup to store consent data
old_signup = """@app.route('/api/signup', methods=['POST'])
def api_signup():
    d = request.json or {}
    success, result = signup(d.get('username',''), d.get('password',''))
    if success:
        session.permanent = True
        session['display_name'] = result
        session['username'] = d['username'].strip().lower()
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})"""

new_signup = """@app.route('/api/signup', methods=['POST'])
def api_signup():
    d = request.json or {}
    success, result = signup(d.get('username',''), d.get('password',''))
    if success:
        session.permanent = True
        session['display_name'] = result
        session['username'] = d['username'].strip().lower()
        session['age_group'] = d.get('age_group', 'unknown')
        session['ai_consent'] = d.get('ai_consent', False)
        return jsonify({"success": True, "display_name": result})
    return jsonify({"success": False, "error": result})"""

content = content.replace(old_signup, new_signup)
open('app.py', 'w', encoding='utf-8').write(content)
print("Privacy route and consent storage added!")