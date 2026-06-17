content = open('templates/index.html', 'r', encoding='utf-8').read()

# 1. Add CSS
social_css = '''
    .class-box { background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .class-title { font-size:11px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }
    .class-row { display:flex; gap:8px; }
    .class-input { flex:1; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:10px 14px; color:#fff; font-size:14px; font-weight:600; letter-spacing:3px; text-align:center; outline:none; }
    .class-input:focus { border-color:#1D9E75; }
    .class-btn { padding:10px 16px; background:#1D9E75; color:#000; border:none; border-radius:8px; font-size:12px; font-weight:700; cursor:pointer; }
    .class-btn.leave { background:#1a1a1a; color:#888; border:1px solid #333; }
    .class-status { font-size:11px; color:#1D9E75; margin-top:8px; min-height:16px; }
'''
content = content.replace('</style>', social_css + '\n  </style>')

# 2. Update quick nav to include new pages
old_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 Focus DNA</a>
  </div>'''

new_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 DNA</a>
    <a href="/buddy" class="quick-nav-btn">🤝 Buddy</a>
    <a href="/teacher" class="quick-nav-btn">🏫 Teacher</a>
    <a href="/wrapped" class="quick-nav-btn">🎁 Wrapped</a>
  </div>'''

content = content.replace(old_nav, new_nav)

# 3. Add Class Join box before badges
class_html = '''
  <div class="class-box">
    <div class="class-title">🏫 Join Class Session</div>
    <div class="class-row">
      <input class="class-input" id="class-code-join" placeholder="CLASS CODE" maxlength="8">
      <button class="class-btn" id="class-join-btn" onclick="joinClass()">Join</button>
    </div>
    <div class="class-status" id="class-status"></div>
  </div>

'''
content = content.replace('<div class="badges-box">', class_html + '<div class="badges-box">')

# 4. Add SocketIO script before Chart.js
content = content.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js',
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.6.1/socket.io.min.js"></script>\n  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js'
)

# 5. Add SocketIO JS
socket_js = '''
    // SOCKET.IO — Buddy + Class
    let appSocket = null;
    let buddyRoom = localStorage.getItem('fm_buddy_room') || '';
    let classRoom = '';

    function initSocket() {
      if (appSocket) return;
      appSocket = io();
    }

    function joinClass() {
      const code = document.getElementById('class-code-join').value.trim().toUpperCase();
      const name = document.getElementById('name-input').value.trim() || 'Student';
      if (!code) { alert('Enter a class code from your teacher'); return; }
      classRoom = code;
      initSocket();
      appSocket.emit('join_class', { class_code: code, name: name, role: 'student' });
      document.getElementById('class-status').textContent = '✅ Joined class: ' + code;
      document.getElementById('class-join-btn').textContent = 'Leave';
      document.getElementById('class-join-btn').className = 'class-btn leave';
      document.getElementById('class-join-btn').onclick = leaveClass;
    }

    function leaveClass() {
      classRoom = '';
      document.getElementById('class-status').textContent = '';
      document.getElementById('class-join-btn').textContent = 'Join';
      document.getElementById('class-join-btn').className = 'class-btn';
      document.getElementById('class-join-btn').onclick = joinClass;
    }

    function emitScores(score, posture, stress, state, burnoutMins) {
      if (!appSocket) return;
      const name = document.getElementById('name-input').value.trim() || 'Student';
      if (buddyRoom) {
        appSocket.emit('buddy_score', {
          room_code: buddyRoom, name, score, posture, stress
        });
      }
      if (classRoom) {
        appSocket.emit('class_score', {
          class_code: classRoom, name, score, posture, stress, state, burnout_mins: burnoutMins
        });
      }
    }

'''

content = content.replace('    let lastBadgeId = null;', socket_js + '\n    let lastBadgeId = null;')

# 6. Call emitScores in updateDashboard
content = content.replace(
    'adaptPomodoro(d.score);',
    'adaptPomodoro(d.score);\n      emitScores(d.score, d.posture, d.stress, d.state, d.burnout_mins);'
)

# 7. Init socket on page load
content = content.replace(
    '    init();',
    '    init();\n    initSocket();',
    1
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("index.html updated with social features!")