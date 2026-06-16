content = open('templates/index.html', 'r', encoding='utf-8').read()

# 1. Add CSS
pom_css = '''
    .quick-nav { display:flex; gap:8px; max-width:480px; margin:0 auto 12px; }
    .quick-nav-btn { flex:1; padding:8px; background:#111; border:1px solid #222; border-radius:10px; color:#666; font-size:11px; font-weight:600; text-decoration:none; text-align:center; transition:all .2s; }
    .quick-nav-btn:hover { border-color:#1D9E75; color:#1D9E75; }
    .pom-card { background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; text-align:center; transition:border-color .3s; }
    .pom-card.active { border-color:#1D9E75; }
    .pom-card.warning { border-color:#EF9F27; }
    .pom-card.danger { border-color:#E24B4A; }
    .pom-mode { font-size:9px; text-transform:uppercase; letter-spacing:3px; color:#666; margin-bottom:10px; }
    .pom-ring-wrap { position:relative; width:100px; height:100px; margin:0 auto 10px; }
    .pom-time { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-size:20px; font-weight:700; color:#fff; }
    .pom-adaptive { font-size:11px; color:#1D9E75; min-height:16px; margin-bottom:12px; }
    .pom-btns { display:flex; gap:8px; justify-content:center; }
    .pom-btn { padding:8px 20px; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer; border:none; }
    .pom-start { background:#1D9E75; color:#000; }
    .pom-reset { background:#1a1a1a; color:#666; border:1px solid #333; }
'''
content = content.replace('</style>', pom_css + '\n  </style>')

# 2. Add Quick Nav after top-bar
nav_html = '''
  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 Focus DNA</a>
  </div>

'''
content = content.replace('  <div class="burnout-banner"', nav_html + '  <div class="burnout-banner"')

# 3. Add Pomodoro Widget before grid
pom_html = '''
  <div class="pom-card" id="pom-card">
    <div class="pom-mode" id="pom-mode">🍅 ADAPTIVE POMODORO</div>
    <div class="pom-ring-wrap">
      <svg width="100" height="100" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="42" fill="none" stroke="#1a1a1a" stroke-width="7"/>
        <circle cx="50" cy="50" r="42" fill="none" stroke="#1D9E75" stroke-width="7"
                stroke-linecap="round" stroke-dasharray="263.9" stroke-dashoffset="0"
                transform="rotate(-90 50 50)" id="pom-ring"/>
      </svg>
      <div class="pom-time" id="pom-display">25:00</div>
    </div>
    <div class="pom-adaptive" id="pom-msg">Start a session to begin your Pomodoro</div>
    <div class="pom-btns">
      <button class="pom-btn pom-start" id="pom-start-btn" onclick="togglePomodoro()">▶ Start</button>
      <button class="pom-btn pom-reset" onclick="resetPomodoro()">↺ Reset</button>
    </div>
  </div>

'''
content = content.replace('  <div class="grid">', pom_html + '  <div class="grid">')

# 4. Add Pomodoro JS before lastBadgeId
pom_js = '''
    // ADAPTIVE POMODORO
    const POM_CIRC = 263.9;
    let pomRunning = false;
    let pomMode = 'focus'; // 'focus' or 'break'
    let pomTotal = 25 * 60;
    let pomLeft = 25 * 60;
    let pomInterval = null;
    let pomExtended = false;
    let lowScoreStreak = 0;
    let highScoreStreak = 0;

    function pomFormat(secs) {
      const m = Math.floor(secs/60).toString().padStart(2,'0');
      const s = (secs%60).toString().padStart(2,'0');
      return m + ':' + s;
    }

    function updatePomRing() {
      const pct = pomLeft / pomTotal;
      const offset = POM_CIRC * (1 - pct);
      document.getElementById('pom-ring').setAttribute('stroke-dashoffset', offset);
      document.getElementById('pom-display').textContent = pomFormat(pomLeft);
      const color = pomMode === 'break' ? '#4A9EEF' : (pct > 0.5 ? '#1D9E75' : pct > 0.25 ? '#EF9F27' : '#E24B4A');
      document.getElementById('pom-ring').setAttribute('stroke', color);
    }

    function togglePomodoro() {
      const btn = document.getElementById('pom-start-btn');
      if (pomRunning) {
        clearInterval(pomInterval);
        pomRunning = false;
        btn.textContent = '▶ Start';
        document.getElementById('pom-card').className = 'pom-card';
      } else {
        pomRunning = true;
        btn.textContent = '⏸ Pause';
        document.getElementById('pom-card').classList.add('active');
        pomInterval = setInterval(() => {
          pomLeft--;
          updatePomRing();
          if (pomLeft <= 0) {
            clearInterval(pomInterval);
            pomRunning = false;
            btn.textContent = '▶ Start';
            if (pomMode === 'focus') {
              pomMode = 'break';
              pomTotal = 5 * 60;
              pomLeft = 5 * 60;
              pomExtended = false;
              lowScoreStreak = 0;
              highScoreStreak = 0;
              document.getElementById('pom-mode').textContent = '☕ BREAK TIME';
              document.getElementById('pom-msg').textContent = 'Great work! Take a 5 minute break.';
              playChime('positive');
            } else {
              pomMode = 'focus';
              pomTotal = 25 * 60;
              pomLeft = 25 * 60;
              document.getElementById('pom-mode').textContent = '🍅 FOCUS SESSION';
              document.getElementById('pom-msg').textContent = 'Break over. Back to work!';
              playChime('burnout');
            }
            updatePomRing();
          }
        }, 1000);
      }
    }

    function resetPomodoro() {
      clearInterval(pomInterval);
      pomRunning = false;
      pomMode = 'focus';
      pomTotal = 25 * 60;
      pomLeft = 25 * 60;
      pomExtended = false;
      lowScoreStreak = 0;
      highScoreStreak = 0;
      document.getElementById('pom-start-btn').textContent = '▶ Start';
      document.getElementById('pom-mode').textContent = '🍅 ADAPTIVE POMODORO';
      document.getElementById('pom-msg').textContent = 'Start a session to begin your Pomodoro';
      document.getElementById('pom-card').className = 'pom-card';
      updatePomRing();
    }

    function adaptPomodoro(score) {
      if (!pomRunning || pomMode !== 'focus') return;
      if (score < 45) {
        lowScoreStreak++;
        highScoreStreak = 0;
        if (lowScoreStreak >= 5) {
          document.getElementById('pom-msg').textContent = '⚠ Focus dropping — consider taking an early break';
          document.getElementById('pom-card').className = 'pom-card danger';
        }
      } else if (score >= 80) {
        highScoreStreak++;
        lowScoreStreak = 0;
        if (highScoreStreak >= 10 && !pomExtended && pomLeft < 10 * 60) {
          pomTotal += 10 * 60;
          pomLeft += 10 * 60;
          pomExtended = true;
          document.getElementById('pom-msg').textContent = '🔥 You are in the zone! +10 min extended';
          document.getElementById('pom-card').className = 'pom-card active';
        } else if (!pomExtended) {
          document.getElementById('pom-msg').textContent = '🔥 Excellent focus! Keep it up';
          document.getElementById('pom-card').className = 'pom-card active';
        }
      } else {
        lowScoreStreak = 0;
        highScoreStreak = 0;
        document.getElementById('pom-msg').textContent = 'Focus score: ' + score + ' — Stay on track!';
        document.getElementById('pom-card').className = 'pom-card';
      }
    }

'''
content = content.replace('    let lastBadgeId = null;', pom_js + '\n    let lastBadgeId = null;')

# 5. Add adaptPomodoro call in updateDashboard
content = content.replace(
    'lastScoreAlert = d.score;',
    'lastScoreAlert = d.score;\n      adaptPomodoro(d.score);'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Tier 1 features added — Pomodoro, DNA page, Stats Dashboard!")