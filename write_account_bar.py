content = open('templates/index.html', 'r', encoding='utf-8').read()

# Add CSS
css = '''
    .acc-bar { max-width:480px; margin:0 auto 12px; background:#111; border:1px solid #1a1a1a; border-radius:12px; padding:10px 14px; display:flex; align-items:center; justify-content:space-between; }
    .acc-left { display:flex; align-items:center; gap:10px; }
    .acc-avatar { width:34px; height:34px; border-radius:50%; background:#0d2e1f; border:2px solid #1D9E75; display:flex; align-items:center; justify-content:center; font-size:15px; font-weight:800; color:#1D9E75; flex-shrink:0; }
    .acc-name { font-size:13px; font-weight:600; }
    .acc-sub { font-size:10px; color:#444; margin-top:1px; }
    .acc-login-btn { padding:6px 14px; background:#1D9E75; color:#000; border:none; border-radius:8px; font-size:11px; font-weight:700; cursor:pointer; }
    .acc-logout-btn { padding:6px 14px; background:#1a1a1a; color:#555; border:1px solid #2a2a2a; border-radius:8px; font-size:11px; font-weight:600; cursor:pointer; }
'''
content = content.replace('</style>', css + '\n  </style>')

# Add account bar after quick nav
bar_html = '''  <div class="acc-bar">
    <div class="acc-left">
      <div class="acc-avatar" id="acc-av">?</div>
      <div>
        <div class="acc-name" id="acc-name">Guest</div>
        <div class="acc-sub" id="acc-sub">Not logged in</div>
      </div>
    </div>
    <div id="acc-action">
      <button class="acc-login-btn" onclick="location.href='/login-page'">Log In</button>
    </div>
  </div>

'''
content = content.replace(
    '  <div class="burnout-banner"',
    bar_html + '  <div class="burnout-banner"'
)

# Add JS
js = '''
    async function loadAccount() {
      try {
        const r = await fetch('/api/me');
        const d = await r.json();
        if (d.logged_in) {
          document.getElementById('acc-av').textContent = d.display_name[0].toUpperCase();
          document.getElementById('acc-name').textContent = d.display_name;
          document.getElementById('acc-sub').textContent = '@' + d.username;
          document.getElementById('acc-action').innerHTML = '<button class="acc-logout-btn" onclick="location.href=\\'/api/logout\\'">Log Out</button>';
          // Auto fill name
          document.getElementById('name-input').value = d.display_name;
          localStorage.setItem('fm_username', d.display_name);
        } else {
          document.getElementById('acc-name').textContent = 'Guest';
          document.getElementById('acc-sub').textContent = 'Not logged in';
        }
      } catch(e) { console.log('Account error:', e); }
    }

'''

content = content.replace(
    '    // SOCKET.IO',
    js + '\n    // SOCKET.IO'
)

# Call on init
content = content.replace(
    '    init();\n    initSocket();',
    '    init();\n    initSocket();\n    loadAccount();'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Account bar added!")