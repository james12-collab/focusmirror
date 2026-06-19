content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. SHARE CARD CSS ─────────────────────────────────────
share_css = '''
    .share-overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.92); z-index:10002; display:none; align-items:center; justify-content:center; padding:20px; flex-direction:column; }
    .share-overlay.show { display:flex; }
    .share-card-wrap { width:100%; max-width:340px; margin-bottom:16px; }
    .share-card { background:linear-gradient(135deg,#0d2e1f 0%,#0a0a2e 60%,#1a0a2e 100%); border-radius:20px; padding:28px 24px; text-align:center; border:1px solid rgba(29,158,117,0.3); }
    .sc-brand { font-size:11px; color:#1D9E75; letter-spacing:3px; font-weight:700; margin-bottom:20px; }
    .sc-grade-wrap { width:80px; height:80px; border-radius:50%; border:3px solid #1D9E75; display:flex; align-items:center; justify-content:center; margin:0 auto 12px; }
    .sc-grade { font-size:38px; font-weight:900; }
    .sc-name { font-size:16px; font-weight:700; color:#fff; margin-bottom:4px; }
    .sc-date { font-size:10px; color:rgba(255,255,255,0.3); margin-bottom:20px; }
    .sc-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-bottom:18px; }
    .sc-stat { background:rgba(255,255,255,0.05); border-radius:10px; padding:10px 6px; }
    .sc-stat-val { font-size:20px; font-weight:800; color:#1D9E75; }
    .sc-stat-lbl { font-size:9px; color:rgba(255,255,255,0.3); text-transform:uppercase; letter-spacing:1px; margin-top:2px; }
    .sc-insight { background:rgba(29,158,117,0.08); border:1px solid rgba(29,158,117,0.2); border-radius:10px; padding:10px 14px; font-size:11px; color:rgba(255,255,255,0.6); line-height:1.6; margin-bottom:16px; }
    .sc-streak { font-size:11px; color:#EF9F27; margin-bottom:12px; }
    .sc-footer { font-size:9px; color:rgba(255,255,255,0.15); letter-spacing:2px; }
    .share-actions { display:flex; flex-direction:column; gap:8px; width:100%; max-width:340px; }
    .share-action-btn { padding:12px; border-radius:12px; font-size:13px; font-weight:700; cursor:pointer; border:none; width:100%; }
    .btn-whatsapp { background:#25D366; color:#000; }
    .btn-download { background:#1D9E75; color:#000; }
    .btn-close-share { background:#1a1a1a; color:#666; border:1px solid #333; }
'''
content = content.replace('</style>', share_css + '\n  </style>')

# ── 2. SHARE OVERLAY HTML ─────────────────────────────────
share_html = '''  <div class="share-overlay" id="share-overlay">
    <div class="share-card-wrap">
      <div class="share-card" id="share-card">
        <div class="sc-brand">⚡ FOCUSMIRROR</div>
        <div class="sc-grade-wrap">
          <div class="sc-grade" id="sc-grade" style="color:#1D9E75">A</div>
        </div>
        <div class="sc-name" id="sc-name">Student</div>
        <div class="sc-date" id="sc-date"></div>
        <div class="sc-stats">
          <div class="sc-stat"><div class="sc-stat-val" id="sc-score">0</div><div class="sc-stat-lbl">Score</div></div>
          <div class="sc-stat"><div class="sc-stat-val" id="sc-time">0m</div><div class="sc-stat-lbl">Duration</div></div>
          <div class="sc-stat"><div class="sc-stat-val" id="sc-eng">0</div><div class="sc-stat-lbl">Engagement</div></div>
        </div>
        <div class="sc-insight" id="sc-insight"></div>
        <div class="sc-streak" id="sc-streak"></div>
        <div class="sc-footer">focusmirror.onrender.com · AI Study Tracker</div>
      </div>
    </div>
    <div class="share-actions">
      <button class="share-action-btn btn-whatsapp" onclick="shareToWhatsApp()">📱 Share on WhatsApp</button>
      <button class="share-action-btn btn-download" onclick="downloadCard()">📥 Save Image</button>
      <button class="share-action-btn btn-close-share" onclick="closeShareCard()">Close</button>
    </div>
  </div>

'''
content = content.replace(
    '  <div class="badge-overlay"',
    share_html + '  <div class="badge-overlay"'
)

# ── 3. SHARE CARD JS ──────────────────────────────────────
share_js = '''
    // SHAREABLE SESSION CARD
    function getGradeColor(grade) {
      const colors = {'A+':'#1D9E75','A':'#1D9E75','B':'#4A9EEF','C':'#EF9F27','D':'#BA7517','F':'#E24B4A'};
      return colors[grade] || '#888';
    }

    function generateShareCard() {
      const name = document.getElementById('name-input').value.trim() || 'Student';
      const score = parseInt(document.getElementById('best-val').textContent) || 0;
      const duration = document.getElementById('session-val').textContent || '0';
      const engagement = document.getElementById('engagement-val').textContent || '0';
      const streak = document.getElementById('streak-num') ? document.getElementById('streak-num').textContent : '0';

      function getGrade(s) {
        if (s >= 90) return 'A+';
        if (s >= 80) return 'A';
        if (s >= 70) return 'B';
        if (s >= 60) return 'C';
        if (s >= 50) return 'D';
        return 'F';
      }

      function getInsight(s) {
        if (s >= 85) return '🌟 Elite focus session. Brain was fully in the zone.';
        if (s >= 70) return '💪 Strong performance. Consistent and engaged throughout.';
        if (s >= 55) return '📈 Decent session. Remove one distraction to reach 80+.';
        if (s >= 40) return '⚡ Developing focus. Short consistent sessions beat long unfocused ones.';
        return '🔋 Rest and recover. Your next session will be stronger.';
      }

      const grade = getGrade(score);
      const color = getGradeColor(grade);
      const now = new Date().toLocaleDateString('en', {weekday:'long', day:'numeric', month:'long', year:'numeric'});

      document.getElementById('sc-grade').textContent = grade;
      document.getElementById('sc-grade').style.color = color;
      document.getElementById('sc-grade-wrap') && (document.querySelector('.sc-grade-wrap').style.borderColor = color);
      document.getElementById('sc-name').textContent = name;
      document.getElementById('sc-date').textContent = now;
      document.getElementById('sc-score').textContent = score;
      document.getElementById('sc-time').textContent = duration + 'm';
      document.getElementById('sc-eng').textContent = engagement;
      document.getElementById('sc-insight').textContent = getInsight(score);
      document.getElementById('sc-streak').textContent = streak > 0 ? '🔥 ' + streak + ' Day Study Streak' : '';

      document.getElementById('share-overlay').classList.add('show');
    }

    function closeShareCard() {
      document.getElementById('share-overlay').classList.remove('show');
    }

    function shareToWhatsApp() {
      const name = document.getElementById('name-input').value.trim() || 'Student';
      const score = document.getElementById('best-val').textContent || '0';
      const streak = document.getElementById('streak-num') ? document.getElementById('streak-num').textContent : '0';
      function getGrade(s) {
        s = parseInt(s);
        if (s >= 90) return 'A+'; if (s >= 80) return 'A';
        if (s >= 70) return 'B'; if (s >= 60) return 'C';
        if (s >= 50) return 'D'; return 'F';
      }
      const grade = getGrade(score);
      const text = `I just completed a study session on FocusMirror!%0A%0A🧠 Focus Score: ${score}/100%0A📊 Grade: ${grade}%0A🔥 Study Streak: ${streak} days%0A%0AMy AI detected my real focus — not just time spent studying.%0A%0ATry it FREE 👇%0Afocusmirror.onrender.com`;
      window.open('https://wa.me/?text=' + text, '_blank');
    }

    function downloadCard() {
      alert('Tip: Take a screenshot of this card to save it! On Android: hold power + volume down. On iPhone: power + home button.');
    }

'''

content = content.replace(
    '    // NOVA — AI MASCOT',
    share_js + '\n    // NOVA — AI MASCOT'
)

# ── 4. TRIGGER SHARE CARD FROM REPORT CARD ───────────────
old_report_btn = '<button class="report-btn" onclick="closeReport()">Save &amp; Reset →</button>'
new_report_btn = '''<div style="display:flex;gap:8px;">
        <button class="report-btn" style="flex:1" onclick="closeReport()">Save &amp; Reset →</button>
        <button class="report-btn" style="flex:1;background:#0d2e1f;color:#1D9E75;border:1px solid #1D9E75" onclick="generateShareCard()">📸 Share</button>
      </div>'''
content = content.replace(old_report_btn, new_report_btn)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Shareable session card added!")