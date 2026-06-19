# Add parent and schools routes to app.py
content = open('app.py', 'r', encoding='utf-8').read()

old_route = """@app.route('/privacy')
def privacy():
    return render_template('privacy.html')"""

new_route = """@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/parent')
def parent():
    return render_template('parent.html')

@app.route('/schools')
def schools():
    return render_template('schools.html')"""

content = content.replace(old_route, new_route)
open('app.py', 'w', encoding='utf-8').write(content)
print("app.py routes updated!")

# Update landing.html to add schools link
landing = open('templates/landing.html', 'r', encoding='utf-8').read()
old_nav_btn = '<a href="/app" class="nav-btn">Try Free →</a>'
new_nav_btn = '<div style="display:flex;gap:8px;"><a href="/schools" style="background:transparent;color:#666;padding:8px 16px;border-radius:20px;font-size:13px;border:1px solid #333;text-decoration:none;">For Schools</a><a href="/app" class="nav-btn">Try Free →</a></div>'
landing = landing.replace(old_nav_btn, new_nav_btn)
open('templates/landing.html', 'w', encoding='utf-8').write(landing)
print("landing.html updated!")

# Update index.html quick nav to include parent and schools
index = open('templates/index.html', 'r', encoding='utf-8').read()
old_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 DNA</a>
    <a href="/buddy" class="quick-nav-btn">🤝 Buddy</a>
    <a href="/teacher" class="quick-nav-btn">🏫 Teacher</a>
    <a href="/wrapped" class="quick-nav-btn">🎁 Wrapped</a>
    <a href="/world" class="quick-nav-btn">🌍 World</a>
    <a href="/exam" class="quick-nav-btn">📅 Exam</a>
  </div>'''

new_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 DNA</a>
    <a href="/buddy" class="quick-nav-btn">🤝 Buddy</a>
    <a href="/teacher" class="quick-nav-btn">🏫 Teacher</a>
    <a href="/parent" class="quick-nav-btn">👨‍👩‍👧 Parent</a>
    <a href="/wrapped" class="quick-nav-btn">🎁 Wrapped</a>
    <a href="/world" class="quick-nav-btn">🌍 World</a>
    <a href="/exam" class="quick-nav-btn">📅 Exam</a>
    <a href="/schools" class="quick-nav-btn">🏫 Schools</a>
    <a href="/privacy" class="quick-nav-btn">🔒 Privacy</a>
  </div>'''

index = index.replace(old_nav, new_nav)
open('templates/index.html', 'w', encoding='utf-8').write(index)
print("index.html nav updated!")