content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. CSS ───────────────────────────────────────────────────────────────
tier3_css = '''
    .streak-bar { background:linear-gradient(135deg,#1a0a00,#2e1500); border:1px solid #EF9F27; border-radius:12px; padding:14px 16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; display:flex; align-items:center; justify-content:space-between; }
    .streak-left { display:flex; align-items:center; gap:12px; }
    .streak-fire { font-size:28px; }
    .streak-info { display:flex; flex-direction:column; }
    .streak-num { font-size:24px; font-weight:800; color:#EF9F27; line-height:1; }
    .streak-label { font-size:10px; color:#888; text-transform:uppercase; letter-spacing:2px; margin-top:2px; }
    .streak-msg { font-size:11px; color:#EF9F27; }
    .pdf-btn { padding:8px 16px; background:#EF9F27; color:#000; border:none; border-radius:8px; font-size:12px; font-weight:700; cursor:pointer; transition:opacity .2s; }
    .pdf-btn:hover { opacity:0.85; }
'''
content = content.replace('</style>', tier3_css + '\n  </style>')

# ── 2. HTML: Streak bar ───────────────────────────────────────────────────
streak_html = '''
  <div class="streak-bar" id="streak-bar" style="display:none">
    <div class="streak-left">
      <div class="streak-fire">🔥</div>
      <div class="streak-info">
        <div class="streak-num" id="streak-num">0</div>
        <div class="streak-label">Day Streak</div>
        <div class="streak-msg" id="streak-msg">Keep it going!</div>
      </div>
    </div>
    <button class="pdf-btn" onclick="downloadPDF()">📄 Download Report</button>
  </div>

'''
content = content.replace(
    '  <div class="burnout-banner"',
    streak_html + '  <div class="burnout-banner"'
)

# ── 3. PDF Download JS + Streak JS ───────────────────────────────────────
tier3_js = '''
    // ═══════════════════════════════════════════
    // STREAK SYSTEM
    // ═══════════════════════════════════════════
    function updateStreak(patterns) {
      if (!patterns || !patterns.streak) return;
      const streak = patterns.streak;
      const bar = document.getElementById('streak-bar');
      const num = document.getElementById('streak-num');
      const msg = document.getElementById('streak-msg');
      bar.style.display = 'flex';
      num.textContent = streak;
      if (streak === 1) msg.textContent = 'Great start! Come back tomorrow.';
      else if (streak === 2) msg.textContent = 'Two days in a row!';
      else if (streak === 3) msg.textContent = 'Three day streak! You are building a habit.';
      else if (streak < 7) msg.textContent = streak + ' days strong. Keep it up!';
      else if (streak === 7) msg.textContent = '🏆 One full week! Incredible dedication.';
      else msg.textContent = streak + ' days! You are unstoppable.';
      if (streak >= 3) {
        speak('Amazing! You are on a ' + streak + ' day study streak!', 'streak');
      }
    }

    // ═══════════════════════════════════════════
    // PDF REPORT DOWNLOAD
    // ═══════════════════════════════════════════
    function downloadPDF() {
      const name = document.getElementById('name-input').value.trim() || 'Student';
      const score = document.getElementById('best-val').textContent || '0';
      const posture = document.getElementById('posture-val').textContent || '0';
      const session = document.getElementById('session-val').textContent || '0';
      const stress = document.getElementById('stress-val').textContent || '0';
      const confusion = document.getElementById('confusion-val').textContent || '0';
      const boreout = document.getElementById('boreout-val').textContent || '0';
      const engagement = document.getElementById('engagement-val').textContent || '0';
      const ms = document.getElementById('ms-count').textContent || '0';
      const streak = document.getElementById('streak-num').textContent || '0';
      const now = new Date().toLocaleString();

      function getGrade(s) {
        s = parseInt(s);
        if (s >= 90) return 'A+';
        if (s >= 80) return 'A';
        if (s >= 70) return 'B';
        if (s >= 60) return 'C';
        if (s >= 50) return 'D';
        return 'F';
      }

      function getInsightPDF(s, st, co, bo) {
        s = parseInt(s); st = parseInt(st); co = parseInt(co); bo = parseInt(bo);
        if (s >= 80) return 'Outstanding session. Brain was fully in the zone.';
        if (st > 60) return 'High stress detected. Try deep breathing before next session.';
        if (co > 50) return 'High confusion detected. Break topics into smaller chunks.';
        if (bo > 60) return 'Boreout detected. Switch subjects or take a short walk.';
        if (s >= 60) return 'Decent session. Remove distractions to push above 80.';
        return 'Low focus today. Rest and try again in 30 minutes.';
      }

      const grade = getGrade(score);
      const insight = getInsightPDF(score, stress, confusion, boreout);

      const gradeColors = {'A+':'#1D9E75','A':'#1D9E75','B':'#4A9EEF','C':'#EF9F27','D':'#BA7517','F':'#E24B4A'};
      const gradeColor = gradeColors[grade] || '#888';

      const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>FocusMirror Report — ${name}</title>
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body { font-family: 'Segoe UI', sans-serif; background:#fff; color:#111; padding:40px; max-width:600px; margin:0 auto; }
  .header { display:flex; justify-content:space-between; align-items:center; margin-bottom:32px; padding-bottom:20px; border-bottom:2px solid #1D9E75; }
  .logo { font-size:22px; font-weight:800; color:#1D9E75; }
  .date { font-size:12px; color:#888; }
  .hero { text-align:center; margin-bottom:32px; }
  .grade-circle { width:100px; height:100px; border-radius:50%; border:4px solid ${gradeColor}; display:flex; align-items:center; justify-content:center; margin:0 auto 16px; }
  .grade { font-size:44px; font-weight:800; color:${gradeColor}; }
  .name { font-size:20px; font-weight:700; margin-bottom:4px; }
  .subtitle { font-size:13px; color:#888; }
  .stats-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }
  .stat-box { background:#f8f8f8; border-radius:12px; padding:14px; text-align:center; border:1px solid #eee; }
  .stat-val { font-size:24px; font-weight:800; color:#1D9E75; }
  .stat-label { font-size:10px; color:#888; margin-top:4px; text-transform:uppercase; letter-spacing:1px; }
  .section-title { font-size:11px; color:#1D9E75; text-transform:uppercase; letter-spacing:3px; margin-bottom:12px; font-weight:600; }
  .emotion-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:24px; }
  .emotion-box { background:#f8f8f8; border-radius:10px; padding:12px; border:1px solid #eee; }
  .emotion-label { font-size:11px; color:#888; margin-bottom:4px; }
  .emotion-val { font-size:18px; font-weight:700; }
  .insight-box { background:#f0faf6; border:1px solid #1D9E75; border-radius:12px; padding:16px; margin-bottom:24px; }
  .insight-text { font-size:14px; color:#111; line-height:1.6; }
  .streak-box { background:#fff8f0; border:1px solid #EF9F27; border-radius:12px; padding:16px; margin-bottom:24px; text-align:center; }
  .streak-val { font-size:36px; font-weight:800; color:#EF9F27; }
  .streak-lbl { font-size:12px; color:#888; margin-top:4px; }
  .footer { text-align:center; font-size:11px; color:#ccc; padding-top:24px; border-top:1px solid #eee; }
  @media print { body { padding:20px; } }
</style>
</head>
<body>
  <div class="header">
    <div class="logo">FocusMirror</div>
    <div class="date">${now}</div>
  </div>
  <div class="hero">
    <div class="grade-circle"><div class="grade">${grade}</div></div>
    <div class="name">${name}</div>
    <div class="subtitle">Session Report Card</div>
  </div>
  <div class="section-title">Session Overview</div>
  <div class="stats-grid">
    <div class="stat-box"><div class="stat-val">${score}</div><div class="stat-label">Focus Score</div></div>
    <div class="stat-box"><div class="stat-val">${session}m</div><div class="stat-label">Duration</div></div>
    <div class="stat-box"><div class="stat-val">${posture}</div><div class="stat-label">Posture</div></div>
  </div>
  <div class="section-title">Emotion Analysis</div>
  <div class="emotion-grid">
    <div class="emotion-box"><div class="emotion-label">😟 Stress</div><div class="emotion-val" style="color:#E24B4A">${stress}</div></div>
    <div class="emotion-box"><div class="emotion-label">😕 Confusion</div><div class="emotion-val" style="color:#EF9F27">${confusion}</div></div>
    <div class="emotion-box"><div class="emotion-label">😐 Boreout</div><div class="emotion-val" style="color:#BA7517">${boreout}</div></div>
    <div class="emotion-box"><div class="emotion-label">😊 Engagement</div><div class="emotion-val" style="color:#1D9E75">${engagement}</div></div>
  </div>
  <div class="section-title">AI Insight</div>
  <div class="insight-box"><div class="insight-text">💡 ${insight}</div></div>
  <div class="section-title">Study Streak</div>
  <div class="streak-box">
    <div class="streak-val">🔥 ${streak} Days</div>
    <div class="streak-lbl">Consecutive study days</div>
  </div>
  <div class="section-title">Micro-Sleep Events</div>
  <div class="stat-box" style="margin-bottom:24px"><div class="stat-val" style="color:#9B59B6">${ms}</div><div class="stat-label">Micro-Sleeps Detected</div></div>
  <div class="footer">Generated by FocusMirror · focusmirror.onrender.com · AI Study Fatigue Detector</div>
</body>
</html>`;

      const blob = new Blob([html], {type: 'text/html'});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'FocusMirror_Report_' + name + '_' + Date.now() + '.html';
      a.click();
      URL.revokeObjectURL(url);
      speak('Report downloaded successfully!', 'pdf');
    }

'''

content = content.replace(
    '    // ═══════════════════════════════════════════\n    // VOICE ALERTS',
    tier3_js + '\n    // ═══════════════════════════════════════════\n    // VOICE ALERTS'
)

# ── 4. Update loadPatterns to call updateStreak ───────────────────────────
old_pat = "        document.getElementById('pat-avg-score').textContent = data.avg_score;"
new_pat = """        document.getElementById('pat-avg-score').textContent = data.avg_score;
        updateStreak(data);"""
content = content.replace(old_pat, new_pat)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Tier 3 done — Study Streak System + PDF Report Download!")