content = open('templates/index.html', 'r', encoding='utf-8').read()

# === 1. CSS ===
new_css = '''
    .report-overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:10000; display:none; align-items:center; justify-content:center; padding:20px; }
    .report-overlay.show { display:flex; }
    .report-card { background:#111; border:1px solid #1D9E75; border-radius:20px; padding:28px; max-width:400px; width:100%; text-align:center; }
    .report-grade-wrap { width:90px; height:90px; border-radius:50%; border:3px solid #1D9E75; display:flex; align-items:center; justify-content:center; margin:0 auto 16px; }
    .report-grade { font-size:42px; font-weight:800; color:#1D9E75; }
    .report-title { font-size:18px; font-weight:700; margin-bottom:6px; }
    .report-subtitle { font-size:12px; color:#666; margin-bottom:20px; }
    .report-stats { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:20px; }
    .report-stat { background:#1a1a1a; border-radius:10px; padding:12px 8px; }
    .report-stat-val { font-size:20px; font-weight:700; color:#1D9E75; }
    .report-stat-label { font-size:10px; color:#666; margin-top:4px; }
    .report-emotions { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:16px; }
    .report-emotion { background:#1a1a1a; border-radius:8px; padding:8px; font-size:12px; color:#888; }
    .report-emotion span { color:#fff; font-weight:600; }
    .report-insight { background:#0d2e1f; border:1px solid #1D9E75; border-radius:10px; padding:12px; font-size:13px; color:#1D9E75; margin-bottom:16px; line-height:1.5; }
    .report-btn { width:100%; padding:13px; background:#1D9E75; color:#000; border:none; border-radius:12px; font-size:14px; font-weight:700; cursor:pointer; }
    .patterns-box { background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .pattern-row { display:flex; justify-content:space-between; align-items:center; padding:8px 0; border-bottom:1px solid #1a1a1a; }
    .pattern-row:last-child { border:none; }
    .pattern-label { font-size:12px; color:#666; }
    .pattern-val { font-size:13px; font-weight:600; color:#fff; }
    .pattern-bars { display:flex; gap:4px; align-items:flex-end; height:50px; margin-top:12px; }
    .pattern-bar-wrap { display:flex; flex-direction:column; align-items:center; gap:3px; flex:1; }
    .pattern-bar { width:100%; border-radius:3px; }
    .pattern-bar-label { font-size:8px; color:#444; }
'''
content = content.replace('</style>', new_css + '\n  </style>')

# === 2. REPORT CARD HTML ===
report_html = '''
  <div class="report-overlay" id="report-overlay">
    <div class="report-card">
      <div class="report-grade-wrap">
        <div class="report-grade" id="rep-grade">A</div>
      </div>
      <div class="report-title">Session Complete! 🎉</div>
      <div class="report-subtitle" id="rep-subtitle">Great focus session</div>
      <div class="report-stats">
        <div class="report-stat">
          <div class="report-stat-val" id="rep-score">0</div>
          <div class="report-stat-label">Best Score</div>
        </div>
        <div class="report-stat">
          <div class="report-stat-val" id="rep-time">0m</div>
          <div class="report-stat-label">Duration</div>
        </div>
        <div class="report-stat">
          <div class="report-stat-val" id="rep-eng">0</div>
          <div class="report-stat-label">Engagement</div>
        </div>
      </div>
      <div class="report-emotions">
        <div class="report-emotion">😟 Stress <span id="rep-stress">0</span></div>
        <div class="report-emotion">😕 Confusion <span id="rep-confusion">0</span></div>
        <div class="report-emotion">😐 Boreout <span id="rep-boreout">0</span></div>
        <div class="report-emotion">😊 Engagement <span id="rep-eng2">0</span></div>
      </div>
      <div class="report-insight" id="rep-insight">Loading insight...</div>
      <button class="report-btn" onclick="closeReport()">Save &amp; Reset →</button>
    </div>
  </div>

'''
content = content.replace('  <div class="top-bar">', report_html + '  <div class="top-bar">')

# === 3. PATTERNS HTML ===
patterns_html = '''
  <div class="patterns-box" id="patterns-box" style="display:none">
    <div class="section-label">🧠 Your Study Patterns</div>
    <div class="pattern-row">
      <span class="pattern-label">Best Focus Time</span>
      <span class="pattern-val" id="pat-best-time">--</span>
    </div>
    <div class="pattern-row">
      <span class="pattern-label">Avg Session Length</span>
      <span class="pattern-val" id="pat-avg-dur">--</span>
    </div>
    <div class="pattern-row">
      <span class="pattern-label">Focus Trend</span>
      <span class="pattern-val" id="pat-trend">--</span>
    </div>
    <div class="pattern-row">
      <span class="pattern-label">Total Sessions</span>
      <span class="pattern-val" id="pat-total">--</span>
    </div>
    <div class="pattern-row">
      <span class="pattern-label">Average Score</span>
      <span class="pattern-val" id="pat-avg-score">--</span>
    </div>
    <div class="pattern-bars" id="pat-bars"></div>
  </div>

'''
content = content.replace(
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js',
    patterns_html + '\n  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js'
)

# === 4. NEW JS ===
new_js = '''
    // SOUND ALERTS
    let lastChimeTime = 0;
    let lastScoreAlert = 0;

    function playChime(type) {
      const now = Date.now();
      if (now - lastChimeTime < 30000) return;
      lastChimeTime = now;
      try {
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const notes = type === 'burnout' ? [440, 370, 300] : [300, 370, 440];
        notes.forEach((freq, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.frequency.value = freq;
          osc.type = 'sine';
          gain.gain.setValueAtTime(0, ctx.currentTime + i * 0.3);
          gain.gain.linearRampToValueAtTime(0.3, ctx.currentTime + i * 0.3 + 0.05);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.3 + 0.4);
          osc.start(ctx.currentTime + i * 0.3);
          osc.stop(ctx.currentTime + i * 0.3 + 0.5);
        });
      } catch(e) { console.log('Audio error:', e); }
    }

    // REPORT CARD
    let pendingReset = false;

    function getGrade(score) {
      if (score >= 90) return {grade:'A+', color:'#1D9E75', msg:'Outstanding session!'};
      if (score >= 80) return {grade:'A', color:'#1D9E75', msg:'Excellent focus!'};
      if (score >= 70) return {grade:'B', color:'#4A9EEF', msg:'Good session!'};
      if (score >= 60) return {grade:'C', color:'#EF9F27', msg:'Average focus'};
      if (score >= 50) return {grade:'D', color:'#BA7517', msg:'Needs improvement'};
      return {grade:'F', color:'#E24B4A', msg:'Take a proper break'};
    }

    function getInsight(score, stress, confusion, boreout, duration) {
      if (score >= 80) return '🌟 Elite focus session! Your brain was fully in the zone.';
      if (stress > 60) return '😰 High stress detected. Try deep breathing before your next session.';
      if (confusion > 50) return '🤔 High confusion detected. Break topics into smaller chunks next time.';
      if (boreout > 60) return '😴 Boreout detected. Try switching subjects or take a 5-minute walk.';
      if (duration < 5) return '⏱ Very short session. Aim for at least 25 minutes (Pomodoro method).';
      if (score >= 60) return '💪 Decent session! Remove distractions to push your score above 80.';
      return '🔋 Low focus today. Rest, hydrate, and try again in 30 minutes.';
    }

    function showReportCard() {
      const score = parseInt(document.getElementById('best-val').textContent) || 0;
      const duration = parseFloat(document.getElementById('session-val').textContent) || 0;
      const stress = parseInt(document.getElementById('stress-val').textContent) || 0;
      const confusion = parseInt(document.getElementById('confusion-val').textContent) || 0;
      const boreout = parseInt(document.getElementById('boreout-val').textContent) || 0;
      const engagement = parseInt(document.getElementById('engagement-val').textContent) || 0;
      const {grade, color, msg} = getGrade(score);
      const insight = getInsight(score, stress, confusion, boreout, duration);
      document.getElementById('rep-grade').textContent = grade;
      document.getElementById('rep-grade').style.color = color;
      document.getElementById('rep-subtitle').textContent = msg;
      document.getElementById('rep-score').textContent = score;
      document.getElementById('rep-time').textContent = duration + 'm';
      document.getElementById('rep-eng').textContent = engagement;
      document.getElementById('rep-stress').textContent = stress;
      document.getElementById('rep-confusion').textContent = confusion;
      document.getElementById('rep-boreout').textContent = boreout;
      document.getElementById('rep-eng2').textContent = engagement;
      document.getElementById('rep-insight').textContent = insight;
      document.getElementById('report-overlay').classList.add('show');
      pendingReset = true;
    }

    async function closeReport() {
      document.getElementById('report-overlay').classList.remove('show');
      if (pendingReset) {
        pendingReset = false;
        await doReset();
        loadPatterns();
      }
    }

    // PATTERNS
    async function loadPatterns() {
      try {
        const resp = await fetch('/patterns');
        const data = await resp.json();
        if (!data || !data.total_sessions) return;
        document.getElementById('patterns-box').style.display = 'block';
        document.getElementById('pat-best-time').textContent = data.best_time || '--';
        document.getElementById('pat-avg-dur').textContent = (data.avg_duration || 0) + ' min';
        document.getElementById('pat-trend').textContent = data.trend === 'improving' ? '📈 Improving' : '📉 Declining';
        document.getElementById('pat-total').textContent = data.total_sessions + ' sessions';
        document.getElementById('pat-avg-score').textContent = data.avg_score;
        const bars = document.getElementById('pat-bars');
        bars.innerHTML = '';
        (data.recent_scores || []).forEach(score => {
          const wrap = document.createElement('div');
          wrap.className = 'pattern-bar-wrap';
          const bar = document.createElement('div');
          bar.className = 'pattern-bar';
          bar.style.height = (score * 0.45) + 'px';
          bar.style.background = score >= 70 ? '#1D9E75' : score >= 50 ? '#EF9F27' : '#E24B4A';
          const label = document.createElement('div');
          label.className = 'pattern-bar-label';
          label.textContent = score;
          wrap.appendChild(bar);
          wrap.appendChild(label);
          bars.appendChild(wrap);
        });
      } catch(e) { console.log('Pattern error:', e); }
    }

'''
content = content.replace('    let lastBadgeId = null;', new_js + '\n    let lastBadgeId = null;')

# === 5. Update resetSession ===
content = content.replace(
    'async function resetSession(){',
    'async function resetSession(){ const s=parseInt(document.getElementById("best-val").textContent)||0; if(s>0){showReportCard();}else{await doReset();} return; }\n\n    async function doReset(){',
    1
)

# === 6. Sound alerts in updateDashboard ===
content = content.replace(
    'updateEmotions(d.stress, d.confusion, d.boreout, d.engagement);',
    '''updateEmotions(d.stress, d.confusion, d.boreout, d.engagement);
      if (d.burnout_mins !== null && d.burnout_mins !== undefined && d.burnout_mins <= 5) { playChime('burnout'); }
      if (d.score >= 80 && lastScoreAlert < 80) { playChime('positive'); }
      lastScoreAlert = d.score;'''
)

# === 7. Load patterns on init ===
content = content.replace(
    '        updateLeaderboard(board,null,null);',
    '        updateLeaderboard(board,null,null);\n        loadPatterns();'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("All 3 features added - Report Card, Sound Alerts, Study Patterns!")