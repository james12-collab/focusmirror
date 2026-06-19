# Update login.html to add age verification and parental consent
content = open('templates/login.html', 'r', encoding='utf-8').read()

# Add consent CSS
consent_css = """
    .consent-screen{display:none;text-align:center;}
    .consent-icon{font-size:48px;margin-bottom:16px;}
    .consent-title{font-size:18px;font-weight:700;margin-bottom:8px;}
    .consent-desc{font-size:12px;color:#555;line-height:1.7;margin-bottom:20px;}
    .consent-box{background:#1a1a1a;border:1px solid #2a2a2a;border-radius:12px;padding:16px;margin-bottom:16px;text-align:left;}
    .consent-box label{display:flex;align-items:flex-start;gap:10px;cursor:pointer;font-size:12px;color:#888;line-height:1.6;}
    .consent-box input[type=checkbox]{width:16px;height:16px;margin-top:2px;accent-color:#1D9E75;flex-shrink:0;}
    .age-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:14px;}
    .age-btn{padding:10px;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:10px;color:#666;font-size:13px;font-weight:600;cursor:pointer;transition:all .2s;text-align:center;}
    .age-btn.selected{border-color:#1D9E75;color:#1D9E75;background:#0d2e1f;}
"""
content = content.replace('    .hidden{display:none;}', '    .hidden{display:none;}\n' + consent_css)

# Add consent screen HTML before closing card div
consent_html = """
    <div id="consent-screen" class="consent-screen">
      <div class="consent-icon">🔒</div>
      <div class="consent-title">Before We Continue</div>
      <div class="consent-desc">FocusMirror collects focus metrics to help you study better. Please confirm the following before creating your account.</div>

      <div style="margin-bottom:12px;text-align:left;">
        <label style="font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;display:block;margin-bottom:8px;">Your Age Group</label>
        <div class="age-row">
          <div class="age-btn" id="age-under" onclick="selectAge('under')">Under 18</div>
          <div class="age-btn" id="age-over" onclick="selectAge('over')">18 or older</div>
        </div>
      </div>

      <div id="parental-notice" style="display:none;background:#1a0a00;border:1px solid #EF9F27;border-radius:10px;padding:12px;margin-bottom:12px;font-size:11px;color:#EF9F27;line-height:1.6;">
        ⚠ As you are under 18, please ensure a parent or guardian is aware you are using FocusMirror. By continuing you confirm that a parent or guardian has given permission for you to use this app and for your anonymized focus data to be stored.
      </div>

      <div class="consent-box">
        <label>
          <input type="checkbox" id="c1">
          I understand that FocusMirror uses my phone camera to detect blink rate and posture. No video or images are stored. Processing happens on my device only.
        </label>
      </div>
      <div class="consent-box">
        <label>
          <input type="checkbox" id="c2">
          I agree that my anonymized focus session data may be stored to build my personal study patterns. I can delete this data at any time.
        </label>
      </div>
      <div class="consent-box">
        <label>
          <input type="checkbox" id="c3" onchange="toggleAiConsent()">
          (Optional) I consent to my anonymized data being used to improve FocusMirror's AI recommendations. I can withdraw this consent at any time.
        </label>
      </div>

      <button class="btn" onclick="completeConsent()" id="consent-btn" style="opacity:0.4;cursor:not-allowed;" disabled>Create Account →</button>
      <div style="margin-top:12px;font-size:11px;color:#333;text-align:center;">
        <a href="/privacy" target="_blank" style="color:#1D9E75;text-decoration:none;">Read our full Privacy Policy</a>
      </div>
    </div>
"""
content = content.replace(
    "    <div class=\"msg\" id=\"msg\"></div>",
    consent_html + "\n    <div class=\"msg\" id=\"msg\"></div>"
)

# Update the doSignup JS to show consent screen first
old_signup_js = """  async function doSignup() {
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
  }"""

new_signup_js = """  let pendingUsername = '';
  let pendingPassword = '';
  let aiConsentGiven = false;
  let selectedAgeGroup = '';

  function selectAge(group) {
    selectedAgeGroup = group;
    document.getElementById('age-under').className = 'age-btn' + (group === 'under' ? ' selected' : '');
    document.getElementById('age-over').className = 'age-btn' + (group === 'over' ? ' selected' : '');
    document.getElementById('parental-notice').style.display = group === 'under' ? 'block' : 'none';
    checkConsentComplete();
  }

  function toggleAiConsent() {
    aiConsentGiven = document.getElementById('c3').checked;
  }

  function checkConsentComplete() {
    const c1 = document.getElementById('c1').checked;
    const c2 = document.getElementById('c2').checked;
    const ageSelected = selectedAgeGroup !== '';
    const btn = document.getElementById('consent-btn');
    if (c1 && c2 && ageSelected) {
      btn.disabled = false;
      btn.style.opacity = '1';
      btn.style.cursor = 'pointer';
    } else {
      btn.disabled = true;
      btn.style.opacity = '0.4';
      btn.style.cursor = 'not-allowed';
    }
  }

  document.addEventListener('change', function(e) {
    if (e.target.id === 'c1' || e.target.id === 'c2') checkConsentComplete();
  });

  async function completeConsent() {
    const r = await fetch('/api/signup', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        username: pendingUsername,
        password: pendingPassword,
        age_group: selectedAgeGroup,
        ai_consent: aiConsentGiven
      })
    });
    const d = await r.json();
    if (d.success) {
      showMsg('Account created! Logging in...', true);
      setTimeout(() => location.href = '/app', 700);
    } else {
      document.getElementById('consent-screen').style.display = 'none';
      document.getElementById('f-signup').style.display = 'block';
      showMsg(d.error);
    }
  }

  async function doSignup() {
    const u = document.getElementById('su').value.trim();
    const p = document.getElementById('sp').value;
    if (!u || !p) { showMsg('Fill in all fields'); return; }
    pendingUsername = u;
    pendingPassword = p;
    document.getElementById('f-signup').style.display = 'none';
    document.getElementById('msg').textContent = '';
    document.getElementById('consent-screen').style.display = 'block';
  }"""

content = content.replace(old_signup_js, new_signup_js)

open('templates/login.html', 'w', encoding='utf-8').write(content)
print("Parental consent system added to login.html!")

# Update accounts.py to store consent data
accounts_content = open('accounts.py', 'r', encoding='utf-8').read()
old_create = """    accounts[username] = {
        "username": username,
        "display_name": username.capitalize(),
        "password_hash": hashed,
        "salt": salt
    }"""
new_create = """    accounts[username] = {
        "username": username,
        "display_name": username.capitalize(),
        "password_hash": hashed,
        "salt": salt,
        "age_group": "unknown",
        "ai_consent": False,
        "created": __import__('time').strftime("%Y-%m-%d")
    }"""
accounts_content = accounts_content.replace(old_create, new_create)
open('accounts.py', 'w', encoding='utf-8').write(accounts_content)
print("accounts.py updated!")