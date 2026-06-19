content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. MIDNIGHT LOCK CSS ─────────────────────────────────
midnight_css = '''
    .midnight-overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:#0a0a0a; z-index:99999; display:none; align-items:center; justify-content:center; padding:20px; flex-direction:column; text-align:center; }
    .midnight-overlay.show { display:flex; }
    .midnight-icon { font-size:80px; margin-bottom:24px; }
    .midnight-title { font-size:24px; font-weight:800; color:#fff; margin-bottom:12px; }
    .midnight-desc { font-size:14px; color:#555; line-height:1.8; margin-bottom:32px; max-width:320px; }
    .midnight-time { font-size:48px; font-weight:800; color:#1D9E75; margin-bottom:8px; }
    .midnight-time-label { font-size:11px; color:#333; text-transform:uppercase; letter-spacing:2px; margin-bottom:32px; }
    .midnight-fact { background:#111; border:1px solid #1a1a1a; border-radius:12px; padding:14px 20px; margin-bottom:24px; font-size:12px; color:#666; line-height:1.7; max-width:320px; }
    .midnight-fact b { color:#1D9E75; }
    .midnight-override { font-size:11px; color:#333; cursor:pointer; text-decoration:underline; margin-top:12px; }
    .midnight-override.used { color:#222; cursor:not-allowed; text-decoration:none; }
    .suggestion-tag { font-size:10px; color:#444; font-style:italic; margin-top:6px; display:block; }
'''
content = content.replace('</style>', midnight_css + '\n  </style>')

# ── 2. MIDNIGHT LOCK HTML ────────────────────────────────
midnight_html = '''  <div class="midnight-overlay" id="midnight-overlay">
    <div class="midnight-icon">🌙</div>
    <div class="midnight-time" id="midnight-clock">00:00</div>
    <div class="midnight-time-label">It is past midnight</div>
    <div class="midnight-title">Time to Sleep</div>
    <div class="midnight-desc">FocusMirror has stopped your session to protect your sleep. Your brain needs rest to consolidate everything you studied today.</div>
    <div class="midnight-fact">
      <b>Science says:</b> Students who sleep less than 7 hours perform 40% worse on complex problem solving the next day — regardless of how many hours they studied. Sleep is not wasted time. It is when learning becomes permanent.
    </div>
    <div style="font-size:13px;color:#1D9E75;margin-bottom:8px" id="override-status">You have 1 weekly override remaining</div>
    <div class="midnight-override" id="override-btn" onclick="useMidnightOverride()">I understand the risk — use my weekly override</div>
  </div>

'''
content = content.replace(
    '  <div class="acc-bar">',
    midnight_html + '  <div class="acc-bar">'
)

# ── 3. MIDNIGHT LOCK + DISCLAIMER JS ────────────────────
midnight_js = '''
    // MIDNIGHT LOCK
    const MIDNIGHT_KEY = 'fm_midnight_override';

    function getOverrideData() {
      try {
        const d = JSON.parse(localStorage.getItem(MIDNIGHT_KEY) || '{}');
        const today = new Date().toISOString().split('T')[0];
        const weekStart = getWeekStart();
        if (d.week !== weekStart) {
          return { week: weekStart, used: false };
        }
        return d;
      } catch(e) {
        return { week: getWeekStart(), used: false };
      }
    }

    function getWeekStart() {
      const d = new Date();
      d.setHours(0,0,0,0);
      d.setDate(d.getDate() - d.getDay());
      return d.toISOString().split('T')[0];
    }

    function checkMidnightLock() {
      const hour = new Date().getHours();
      const minute = new Date().getMinutes();
      const timeStr = String(hour).padStart(2,'0') + ':' + String(minute).padStart(2,'0');
      document.getElementById('midnight-clock').textContent = timeStr;

      if (hour >= 0 && hour < 5) {
        const overrideData = getOverrideData();
        const overlay = document.getElementById('midnight-overlay');
        const overrideBtn = document.getElementById('override-btn');
        const overrideStatus = document.getElementById('override-status');

        if (overrideData.used) {
          overlay.classList.add('show');
          tracking = false;
          overrideBtn.textContent = 'Weekly override already used. Please sleep.';
          overrideBtn.className = 'midnight-override used';
          overrideStatus.textContent = 'No overrides remaining this week';
          speak('It is past midnight. You have already used your weekly override. Please sleep now. Your brain needs rest.', 'midnight');
        } else {
          overlay.classList.add('show');
          tracking = false;
          overrideStatus.textContent = 'You have 1 weekly override remaining';
          speak('It is past midnight. FocusMirror is stopping your session to protect your sleep.', 'midnight');
        }
      }
    }

    function useMidnightOverride() {
      const overrideData = getOverrideData();
      if (overrideData.used) return;
      if (!confirm('Are you sure? This is your only override this week. FocusMirror strongly recommends sleeping now.')) return;
      overrideData.used = true;
      localStorage.setItem(MIDNIGHT_KEY, JSON.stringify(overrideData));
      document.getElementById('midnight-overlay').classList.remove('show');
      speak('Override activated. You have 30 minutes. FocusMirror will remind you to sleep again soon.', 'override');
      setTimeout(() => {
        speak('30 minutes have passed. Please stop now and sleep. Your brain will thank you tomorrow.', 'sleep_reminder');
      }, 30 * 60 * 1000);
    }

    // Check midnight lock every minute
    setInterval(checkMidnightLock, 60000);

    // SUGGESTION DISCLAIMER
    function addDisclaimer(text) {
      if (!text) return text;
      return text;
    }

'''

content = content.replace(
    '    // GLOBAL BENCHMARKING',
    midnight_js + '\n    // GLOBAL BENCHMARKING'
)

# ── 4. ADD DISCLAIMER TO RECOMMENDATION DISPLAY ──────────
old_rec = "document.getElementById('rec-text').textContent=d.recommendation;"
new_rec = """document.getElementById('rec-text').textContent=d.recommendation;
      document.getElementById('rec-disclaimer').style.display = d.recommendation ? 'block' : 'none';"""
content = content.replace(old_rec, new_rec)

# Add disclaimer span after rec-text
old_alert = '<div class="message" id="rec-text">Enter your name and press Start Tracking</div>'
new_alert = '''<div class="message" id="rec-text">Enter your name and press Start Tracking</div>
      <span class="suggestion-tag" id="rec-disclaimer" style="display:none">This is a suggestion. You know yourself best.</span>'''
content = content.replace(old_alert, new_alert)

# ── 5. CHECK MIDNIGHT ON INIT ────────────────────────────
content = content.replace(
    '    init();\n    initSocket();\n    loadAccount();\n    loadSchedule();',
    '    init();\n    initSocket();\n    loadAccount();\n    loadSchedule();\n    checkMidnightLock();'
)

# ── 6. ADD PRIVACY LINK TO FOOTER ───────────────────────
content = content.replace(
    '</body>\n</html>',
    '''  <div style="text-align:center;padding:20px;font-size:11px;color:#333;max-width:480px;margin:0 auto;">
    <a href="/privacy" style="color:#1D9E75;text-decoration:none;">Privacy Policy</a> ·
    <a href="/app" style="color:#333;text-decoration:none;">focusmirror.onrender.com</a>
  </div>
</body>
</html>'''
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Midnight lock and suggestion disclaimer added!")