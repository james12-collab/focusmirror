content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. STREAK FREEZE CSS ──────────────────────────────────
freeze_css = '''
    .freeze-btn { padding:6px 12px; background:rgba(74,158,239,0.1); color:#4A9EEF; border:1px solid #4A9EEF; border-radius:8px; font-size:11px; font-weight:700; cursor:pointer; transition:all .2s; }
    .freeze-btn:hover { background:rgba(74,158,239,0.2); }
    .freeze-btn.used { background:#1a1a1a; color:#333; border-color:#2a2a2a; cursor:not-allowed; }
    .freeze-popup { position:fixed; bottom:24px; left:50%; transform:translateX(-50%); z-index:10003; background:#111; border:1px solid #4A9EEF; border-radius:14px; padding:14px 20px; text-align:center; display:none; max-width:300px; width:90%; }
    .freeze-popup.show { display:block; animation:slideUp .3s ease; }
    @keyframes slideUp { from{transform:translateX(-50%) translateY(20px);opacity:0} to{transform:translateX(-50%) translateY(0);opacity:1} }
    .freeze-popup-title { font-size:14px; font-weight:700; color:#4A9EEF; margin-bottom:6px; }
    .freeze-popup-desc { font-size:11px; color:#666; line-height:1.6; }
'''
content = content.replace('</style>', freeze_css + '\n  </style>')

# ── 2. ADD FREEZE BUTTON TO STREAK BAR ───────────────────
old_streak_bar = '''    <button class="pdf-btn" onclick="downloadPDF()">📄 Download Report</button>'''
new_streak_bar = '''    <div style="display:flex;gap:8px;align-items:center;">
      <button class="freeze-btn" id="freeze-btn" onclick="freezeStreak()">❄ Freeze</button>
      <button class="pdf-btn" onclick="downloadPDF()">📄 Download Report</button>
    </div>'''
content = content.replace(old_streak_bar, new_streak_bar)

# ── 3. ADD FREEZE POPUP ───────────────────────────────────
freeze_popup = '''  <div class="freeze-popup" id="freeze-popup">
    <div class="freeze-popup-title">❄ Streak Frozen!</div>
    <div class="freeze-popup-desc">Your streak is safe for today. Rest well. Come back tomorrow stronger. 💪</div>
  </div>

'''
content = content.replace(
    '  <div class="share-overlay"',
    freeze_popup + '  <div class="share-overlay"'
)

# ── 4. FREEZE JS ──────────────────────────────────────────
freeze_js = '''
    // STREAK FREEZE
    const FREEZE_KEY = 'fm_streak_freeze';

    function getFreezeData() {
      try {
        const d = JSON.parse(localStorage.getItem(FREEZE_KEY) || '{}');
        const weekStart = getWeekStart();
        if (d.week !== weekStart) {
          return { week: weekStart, used: false, frozen_date: null };
        }
        return d;
      } catch(e) {
        return { week: getWeekStart(), used: false, frozen_date: null };
      }
    }

    function freezeStreak() {
      const data = getFreezeData();
      const btn = document.getElementById('freeze-btn');

      if (data.used) {
        alert('You have already used your streak freeze this week. Come back next week!');
        return;
      }

      if (!confirm('Use your weekly streak freeze? This will protect your streak for today even if you do not complete a session.')) return;

      data.used = true;
      data.frozen_date = new Date().toISOString().split('T')[0];
      localStorage.setItem(FREEZE_KEY, JSON.stringify(data));

      btn.textContent = '❄ Frozen!';
      btn.className = 'freeze-btn used';

      const popup = document.getElementById('freeze-popup');
      popup.classList.add('show');
      setTimeout(() => popup.classList.remove('show'), 4000);

      speak('Streak frozen! Your progress is safe for today. Rest well.', 'freeze');
    }

    function checkFreezeStatus() {
      const data = getFreezeData();
      const btn = document.getElementById('freeze-btn');
      if (!btn) return;
      if (data.used) {
        btn.textContent = '❄ Used';
        btn.className = 'freeze-btn used';
      }
    }

'''

content = content.replace(
    '    // SHAREABLE SESSION CARD',
    freeze_js + '\n    // SHAREABLE SESSION CARD'
)

# ── 5. CALL checkFreezeStatus ON INIT ────────────────────
content = content.replace(
    '    init();\n    initSocket();\n    loadAccount();\n    loadSchedule();\n    checkMidnightLock();',
    '    init();\n    initSocket();\n    loadAccount();\n    loadSchedule();\n    checkMidnightLock();\n    checkFreezeStatus();'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Streak freeze added!")