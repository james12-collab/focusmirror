f = open('templates/login.html', 'w', encoding='utf-8')
f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FocusMirror — Login</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:#0a0a0a;color:#fff;font-family:'Inter',sans-serif;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px;}
    .wrap{width:100%;max-width:360px;}
    .logo{font-size:24px;font-weight:800;color:#1D9E75;text-align:center;margin-bottom:4px;}
    .logo span{color:#fff;}
    .sub{font-size:12px;color:#444;text-align:center;margin-bottom:32px;}
    .card{background:#111;border:1px solid #1a1a1a;border-radius:20px;padding:28px;}
    .tabs{display:grid;grid-template-columns:1fr 1fr;gap:4px;background:#0a0a0a;border-radius:10px;padding:4px;margin-bottom:24px;}
    .tab{padding:10px;text-align:center;border-radius:8px;font-size:13px;font-weight:600;cursor:pointer;color:#444;transition:all .2s;}
    .tab.active{background:#1a1a1a;color:#fff;}
    label{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;display:block;margin-bottom:6px;}
    input{width:100%;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:10px;padding:12px 14px;color:#fff;font-size:14px;outline:none;margin-bottom:14px;}
    input:focus{border-color:#1D9E75;}
    .btn{width:100%;padding:13px;background:#1D9E75;color:#000;border:none;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;transition:opacity .2s;}
    .btn:hover{opacity:.85;}
    .msg{font-size:12px;text-align:center;margin-top:14px;min-height:18px;}
    .msg.err{color:#E24B4A;}
    .msg.ok{color:#1D9E75;}
    .divider{height:1px;background:#1a1a1a;margin:20px 0;}
    .guest{width:100%;padding:11px;background:transparent;color:#444;border:1px solid #1a1a1a;border-radius:12px;font-size:13px;cursor:pointer;transition:all .2s;}
    .guest:hover{border-color:#333;color:#666;}
    .hidden{display:none;}
  </style>
</head>
<body>
<div class="wrap">
  <div class="logo">Focus<span>Mirror</span></div>
  <div class="sub">AI Study Fatigue Detector</div>
  <div class="card">
    <div class="tabs">
      <div class="tab active" id="t-login" onclick="tab('login')">Log In</div>
      <div class="tab" id="t-signup" onclick="tab('signup')">Sign Up</div>
    </div>

    <div id="f-login">
      <label>Username</label>
      <input id="lu" type="text" placeholder="Your username...">
      <label>Password</label>
      <input id="lp" type="password" placeholder="Your password...">
      <button class="btn" onclick="doLogin()">Log In →</button>
    </div>

    <div id="f-signup" class="hidden">
      <label>Username</label>
      <input id="su" type="text" placeholder="Choose a username...">
      <label>Password</label>
      <input id="sp" type="password" placeholder="Min 4 characters...">
      <button class="btn" onclick="doSignup()">Create Account →</button>
    </div>

    <div class="msg" id="msg"></div>
    <div class="divider"></div>
    <button class="guest" onclick="location.href='/app'">Continue as Guest</button>
  </div>
</div>

<script>
  function tab(t) {
    document.getElementById('f-login').classList.toggle('hidden', t !== 'login');
    document.getElementById('f-signup').classList.toggle('hidden', t !== 'signup');
    document.getElementById('t-login').className = 'tab' + (t === 'login' ? ' active' : '');
    document.getElementById('t-signup').className = 'tab' + (t === 'signup' ? ' active' : '');
    document.getElementById('msg').textContent = '';
  }

  function showMsg(text, ok) {
    const el = document.getElementById('msg');
    el.textContent = text;
    el.className = 'msg ' + (ok ? 'ok' : 'err');
  }

  async function doLogin() {
    const u = document.getElementById('lu').value.trim();
    const p = document.getElementById('lp').value;
    if (!u || !p) { showMsg('Fill in all fields'); return; }
    const r = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({username: u, password: p})
    });
    const d = await r.json();
    if (d.success) {
      showMsg('Welcome back, ' + d.display_name + '!', true);
      setTimeout(() => location.href = '/app', 700);
    } else {
      showMsg(d.error);
    }
  }

  async function doSignup() {
    const u = document.getElementById('su').value.trim();
    const p = document.getElementById('sp').value;
    if (!u || !p) { showMsg('Fill in all fields'); return; }
    const r = await fetch('/api/signup', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({username: u, password: p})
    });
    const d = await r.json();
    if (d.success) {
      showMsg('Account created! Logging in...', true);
      setTimeout(() => location.href = '/app', 700);
    } else {
      showMsg(d.error);
    }
  }

  document.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
      if (!document.getElementById('f-login').classList.contains('hidden')) doLogin();
      else doSignup();
    }
  });
</script>
</body>
</html>""")
f.close()
print("login.html written!")