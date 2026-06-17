content = open('templates/index.html', 'r', encoding='utf-8').read()

# Add account bar CSS
account_css = '''
    .account-bar { display:flex; align-items:center; justify-content:space-between; max-width:480px; margin:0 auto 12px; background:#111; border:1px solid #1a1a1a; border-radius:12px; padding:10px 14px; }
    .account-info { display:flex; align-items:center; gap:10px; }
    .account-avatar { width:32px; height:32px; border-radius:50%; background:#0d2e1f; border:2px solid #1D9E75; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; color:#1D9E75; }
    .account-name { font-size:13px; font-weight:600; color:#fff; }
    .account-type { font-size:10px; color:#555; }
    .account-btns { display:flex; gap:6px; }
    .account-btn { padding:5px 12px; border-radius:8px; font-size:11px; font-weight:600; cursor:pointer; border:none; }
    .btn-login { background:#1D9E75; color:#000; }
    .btn-logout { background:#1a1a1a; color:#666; border:1px solid #333; }
'''
content = content.replace('</style>', account_css + '\n  </style>')

# Add account bar after quick nav
account_bar = '''  <div class="account-bar" id="account-bar">
    <div class="account-info">
      <div class="account-avatar" id="acc-avatar">?</div>
      <div>
        <div class="account-name" id="acc-name">Guest</div>
        <div class="account-type" id="acc-type">Not logged in</div>
      </div>
    </div>
    <div class="account-btns">
      <button class="account-btn btn-login" id="acc-login-btn" onclick="window.location='/login-page'" style="display:none">Log In</button>
      <button class="account-btn btn-logout" id="acc-logout-btn" onclick="window.location='/logout'" style="display:none">Log Out</button>
    </div>
  </div>

'''
content = content.replace('  <div class="burnout-banner"', account_bar + '  <div class="burnout-banner"')

# Add account JS
account_js = '''
    // ACCOUNT SYSTEM
    async function loadAccount() {
      try {
        const resp = await fetch('/me');
        const data = await resp.json();
        if (data.logged_in) {
          const name = data.display_name;
          document.getElementById('acc-avatar').textContent = name[0].toUpperCase();
          document.getElementById('acc-name').textContent = name;
          document.getElementById('acc-type').textContent = 'Logged in as @' + data.username;
          document.getElementById('acc-logout-btn').style.display = 'block';
          document.getElementById('acc-login-btn').style.display = 'none';
          // Auto-fill name input
          document.getElementById('name-input').value = name;
          localStorage.setItem('fm_username', name);
        } else {
          document.getElementById('acc-name').textContent = 'Guest';
          document.getElementById('acc-type').textContent = 'Not logged in';
          document.getElementById('acc-login-btn').style.display = 'block';
          document.getElementById('acc-logout-btn').style.display = 'none';
        }
      } catch(e) {
        console.log('Account load error:', e);
      }
    }

'''

content = content.replace(
    '    // SOCKET.IO — Buddy + Class',
    account_js + '\n    // SOCKET.IO — Buddy + Class'
)

# Call loadAccount on init
content = content.replace(
    '    init();\n    initSocket();',
    '    init();\n    initSocket();\n    loadAccount();'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Account bar added to index.html!")