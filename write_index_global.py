content = open('templates/index.html', 'r', encoding='utf-8').read()

# 1. Update quick nav
old_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 DNA</a>
    <a href="/buddy" class="quick-nav-btn">🤝 Buddy</a>
    <a href="/teacher" class="quick-nav-btn">🏫 Teacher</a>
    <a href="/wrapped" class="quick-nav-btn">🎁 Wrapped</a>
  </div>'''

new_nav = '''  <div class="quick-nav">
    <a href="/" class="quick-nav-btn">🏠 Home</a>
    <a href="/stats" class="quick-nav-btn">📊 Stats</a>
    <a href="/dna" class="quick-nav-btn">🧬 DNA</a>
    <a href="/buddy" class="quick-nav-btn">🤝 Buddy</a>
    <a href="/teacher" class="quick-nav-btn">🏫 Teacher</a>
    <a href="/wrapped" class="quick-nav-btn">🎁 Wrapped</a>
    <a href="/world" class="quick-nav-btn">🌍 World</a>
    <a href="/exam" class="quick-nav-btn">📅 Exam</a>
  </div>'''

content = content.replace(old_nav, new_nav)

# 2. Add CSS for global features
global_css = '''
    .benchmark-card { background:#111; border:1px solid #222; border-radius:12px; padding:14px 16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; display:flex; align-items:center; justify-content:space-between; }
    .bench-left { display:flex; align-items:center; gap:12px; }
    .bench-icon { font-size:24px; }
    .bench-label { font-size:10px; color:#555; text-transform:uppercase; letter-spacing:2px; }
    .bench-val { font-size:20px; font-weight:800; color:#1D9E75; }
    .bench-right { text-align:right; font-size:11px; color:#444; line-height:1.6; }
    .sched-card { background:#111; border:1px solid #222; border-radius:12px; padding:14px 16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .sched-title { font-size:10px; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }
    .sched-row { display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid #1a1a1a; }
    .sched-row:last-child { border:none; }
    .sched-time { font-size:12px; color:#888; }
    .sched-score { font-size:13px; font-weight:700; }
    .sched-bar { height:4px; background:#1a1a1a; border-radius:2px; margin-top:6px; overflow:hidden; }
    .sched-fill { height:4px; border-radius:2px; }
'''
content = content.replace('</style>', global_css + '\n  </style>')

# 3. Add benchmarking card after emotion grid
bench_html = '''
  <div class="benchmark-card" id="bench-card" style="display:none">
    <div class="bench-left">
      <div class="bench-icon">🌍</div>
      <div>
        <div class="bench-label">Global Rank</div>
        <div class="bench-val" id="bench-val">--</div>
      </div>
    </div>
    <div class="bench-right" id="bench-right">Calculating...</div>
  </div>

  <div class="sched-card" id="sched-card" style="display:none">
    <div class="sched-title">🕐 Your Predicted Best Study Times</div>
    <div id="sched-rows">Loading...</div>
  </div>

'''
content = content.replace('<div class="class-box">', bench_html + '<div class="class-box">')

# 4. Add global JS
global_js = '''
    // GLOBAL BENCHMARKING
    let lastBenchScore = -1;
    async function updateBenchmark(score) {
      if (score === lastBenchScore || score === 0) return;
      lastBenchScore = score;
      try {
        const r = await fetch('/api/benchmarks?score=' + score);
        const d = await r.json();
        if (!d.total) return;
        const card = document.getElementById('bench-card');
        card.style.display = 'flex';
        document.getElementById('bench-val').textContent = 'Top ' + (100 - d.percentile) + '%';
        document.getElementById('bench-right').innerHTML =
          'Better than <b style="color:#1D9E75">' + d.percentile + '%</b> of students<br>' +
          'Global avg: ' + d.avg + ' | Total: ' + d.total;
      } catch(e) {}
    }

    // PREDICTIVE SCHEDULING
    async function loadSchedule() {
      const uname = localStorage.getItem('fm_username') || '';
      try {
        const r = await fetch('/patterns?user=' + encodeURIComponent(uname));
        const d = await r.json();
        if (!d.time_avgs) return;
        const sched = document.getElementById('sched-card');
        const rows = document.getElementById('sched-rows');
        const order = ['Morning','Afternoon','Evening','Night','Late Night'];
        const emojis = {'Morning':'🌅','Afternoon':'⚡','Evening':'🌙','Night':'🦉','Late Night':'🌟'};
        const avgs = d.time_avgs;
        const sorted = order.filter(t => avgs[t]).sort((a,b) => avgs[b] - avgs[a]);
        if (!sorted.length) return;
        sched.style.display = 'block';
        rows.innerHTML = sorted.map((t,i) => {
          const score = avgs[t];
          const color = score >= 70 ? '#1D9E75' : score >= 45 ? '#EF9F27' : '#E24B4A';
          const badge = i === 0 ? ' 🔥 Best' : '';
          return '<div class="sched-row">' +
            '<span class="sched-time">' + (emojis[t]||'') + ' ' + t + badge + '</span>' +
            '<span class="sched-score" style="color:' + color + '">' + score + '</span>' +
            '</div>' +
            '<div class="sched-bar"><div class="sched-fill" style="width:' + score + '%;background:' + color + '"></div></div>';
        }).join('');
      } catch(e) {}
    }

    // LOCATION SHARING FOR WORLD MAP
    function shareLocation(score) {
      if (!navigator.geolocation) return;
      navigator.geolocation.getCurrentPosition(pos => {
        fetch('/api/save-location', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            lat: pos.coords.latitude,
            lng: pos.coords.longitude,
            score: score
          })
        }).catch(() => {});
      }, () => {});
    }

'''

content = content.replace(
    '    // ACCOUNT SYSTEM',
    global_js + '\n    // ACCOUNT SYSTEM'
)

# 5. Call benchmark in updateDashboard
content = content.replace(
    'adaptPomodoro(d.score);',
    'adaptPomodoro(d.score);\n      updateBenchmark(d.score);'
)

# 6. Call schedule and share location on init
content = content.replace(
    '    init();\n    initSocket();\n    loadAccount();',
    '    init();\n    initSocket();\n    loadAccount();\n    loadSchedule();'
)

# 7. Share location when session is saved
content = content.replace(
    'async function doReset(){',
    'async function doReset(){\n      const bestForLoc = parseInt(document.getElementById("best-val").textContent)||0;\n      if(bestForLoc>0) shareLocation(bestForLoc);'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("index.html updated with global features!")