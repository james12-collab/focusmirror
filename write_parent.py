f = open('templates/parent.html', 'w', encoding='utf-8')
f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Parent Dashboard — FocusMirror</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:#0a0a0a;color:#fff;font-family:'Inter',sans-serif;padding-bottom:40px;}
    nav{display:flex;align-items:center;justify-content:space-between;padding:20px;max-width:600px;margin:0 auto;}
    .logo{font-size:16px;font-weight:700;color:#1D9E75;}
    .logo span{color:#fff;}
    .nl{font-size:12px;color:#666;text-decoration:none;padding:6px 12px;border-radius:20px;border:1px solid #222;}
    .page{max-width:600px;margin:0 auto;padding:0 16px;}
    .setup-card{background:#111;border:1px solid #1a1a1a;border-radius:16px;padding:28px;margin-bottom:16px;text-align:center;}
    .setup-icon{font-size:48px;margin-bottom:16px;}
    .setup-title{font-size:22px;font-weight:700;margin-bottom:8px;}
    .setup-desc{font-size:13px;color:#555;margin-bottom:24px;line-height:1.7;}
    label{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;display:block;margin-bottom:6px;text-align:left;}
    input{width:100%;background:#1a1a1a;border:1px solid #2a2a2a;border-radius:10px;padding:12px 14px;color:#fff;font-size:14px;outline:none;margin-bottom:14px;}
    input:focus{border-color:#1D9E75;}
    .btn{width:100%;padding:13px;background:#1D9E75;color:#000;border:none;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;}
    .privacy-note{background:#111;border:1px solid #1a1a1a;border-radius:10px;padding:14px;margin-bottom:16px;font-size:11px;color:#555;line-height:1.7;}
    .privacy-note b{color:#1D9E75;}
    .dash-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;}
    .child-info{display:flex;align-items:center;gap:12px;}
    .child-avatar{width:48px;height:48px;border-radius:50%;background:#0d2e1f;border:2px solid #1D9E75;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#1D9E75;}
    .child-name{font-size:18px;font-weight:700;}
    .child-sub{font-size:11px;color:#555;margin-top:2px;}
    .today-card{background:#111;border:1px solid #1a1a1a;border-radius:16px;padding:20px;margin-bottom:16px;}
    .today-label{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:16px;}
    .focus-level{display:flex;align-items:center;gap:16px;margin-bottom:16px;}
    .level-circle{width:80px;height:80px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:800;flex-shrink:0;}
    .level-high{background:#0d2e1f;border:3px solid #1D9E75;color:#1D9E75;}
    .level-medium{background:#1a1400;border:3px solid #EF9F27;color:#EF9F27;}
    .level-low{background:#2e0d0d;border:3px solid #E24B4A;color:#E24B4A;}
    .level-none{background:#1a1a1a;border:3px solid #333;color:#555;}
    .level-info h3{font-size:18px;font-weight:700;margin-bottom:4px;}
    .level-info p{font-size:12px;color:#555;line-height:1.6;}
    .stats-row{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px;}
    .stat-box{background:#1a1a1a;border-radius:12px;padding:14px;text-align:center;}
    .stat-val{font-size:22px;font-weight:700;color:#1D9E75;}
    .stat-lbl{font-size:9px;color:#555;text-transform:uppercase;letter-spacing:1px;margin-top:4px;}
    .insight-box{background:#0d2e1f;border:1px solid #1D9E75;border-radius:12px;padding:14px;margin-bottom:16px;font-size:13px;color:#1D9E75;line-height:1.6;}
    .week-section{margin-bottom:16px;}
    .week-label{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;}
    .week-bars{display:flex;gap:8px;align-items:flex-end;height:80px;}
    .day-bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;}
    .day-bar{width:100%;border-radius:4px;min-height:4px;}
    .day-label{font-size:9px;color:#444;}
    .day-level{font-size:9px;font-weight:700;}
    .streak-row{display:flex;align-items:center;gap:12px;background:#1a1200;border:1px solid #EF9F27;border-radius:12px;padding:14px;margin-bottom:16px;}
    .streak-icon{font-size:28px;}
    .streak-text h3{font-size:16px;font-weight:700;color:#EF9F27;}
    .streak-text p{font-size:11px;color:#666;margin-top:2px;}
    .transparency-box{background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:14px;margin-bottom:16px;}
    .trans-title{font-size:10px;color:#555;text-transform:uppercase;letter-spacing:2px;margin-bottom:10px;}
    .trans-row{display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #1a1a1a;font-size:12px;}
    .trans-row:last-child{border:none;}
    .trans-label{color:#666;}
    .trans-val{color:#1D9E75;font-weight:600;}
    .trans-no{color:#444;}
    .logout-btn{width:100%;padding:11px;background:transparent;color:#444;border:1px solid #1a1a1a;border-radius:12px;font-size:13px;cursor:pointer;margin-top:8px;}
    .no-data{text-align:center;padding:40px 20px;color:#333;}
    .hidden{display:none;}
    .msg{font-size:12px;text-align:center;margin-top:12px;color:#E24B4A;min-height:16px;}
  </style>
</head>
<body>
  <nav>
    <div class="logo">Focus<span>Mirror</span></div>
    <a href="/" class="nl">Home</a>
  </nav>

  <div class="page">

    <!-- SETUP -->
    <div class="setup-card" id="setup-panel">
      <div class="setup-icon">👨‍👩‍👧</div>
      <div class="setup-title">Parent Dashboard</div>
      <div class="setup-desc">View your child's daily focus summary. See how they are studying — without pressure or surveillance.</div>

      <div class="privacy-note">
        🔒 <b>Privacy first:</b> You will see general focus levels — High, Medium or Low — not specific scores. Your child knows exactly what you can see. No surprises. No surveillance.
      </div>

      <label>Your Child's Username</label>
      <input id="child-username" type="text" placeholder="Enter their FocusMirror username...">
      <label>Your Name (so your child knows who is viewing)</label>
      <input id="parent-name" type="text" placeholder="e.g. Mum, Dad, Guardian...">
      <button class="btn" onclick="loadChildData()">View Dashboard →</button>
      <div class="msg" id="setup-msg"></div>
    </div>

    <!-- DASHBOARD -->
    <div id="dashboard-panel" class="hidden">
      <div class="dash-header">
        <div class="child-info">
          <div class="child-avatar" id="child-avatar">S</div>
          <div>
            <div class="child-name" id="child-name-display">Student</div>
            <div class="child-sub">Daily Focus Summary</div>
          </div>
        </div>
        <button class="nl" onclick="leaveDashboard()">← Back</button>
      </div>

      <!-- TODAY -->
      <div class="today-card">
        <div class="today-label">Today's Focus Level</div>
        <div class="focus-level">
          <div class="level-circle" id="level-circle">--</div>
          <div class="level-info">
            <h3 id="level-name">No data yet</h3>
            <p id="level-desc">Your child has not studied yet today.</p>
          </div>
        </div>
        <div class="stats-row">
          <div class="stat-box"><div class="stat-val" id="p-sessions">0</div><div class="stat-lbl">Sessions Today</div></div>
          <div class="stat-box"><div class="stat-val" id="p-time">0m</div><div class="stat-lbl">Study Time</div></div>
          <div class="stat-box"><div class="stat-val" id="p-streak">0</div><div class="stat-lbl">Day Streak 🔥</div></div>
        </div>
        <div class="insight-box" id="p-insight">Loading insight...</div>
      </div>

      <!-- WEEK -->
      <div class="today-card">
        <div class="today-label">This Week</div>
        <div class="week-bars" id="week-bars"></div>
      </div>

      <!-- STREAK -->
      <div class="streak-row" id="streak-row" style="display:none">
        <div class="streak-icon">🔥</div>
        <div class="streak-text">
          <h3 id="streak-text-main">0 Day Streak</h3>
          <p id="streak-text-sub">Keep encouraging them!</p>
        </div>
      </div>

      <!-- TRANSPARENCY -->
      <div class="transparency-box">
        <div class="trans-title">📋 What You Can See vs What You Cannot</div>
        <div class="trans-row"><span class="trans-label">Focus Level (High/Med/Low)</span><span class="trans-val">✓ Visible</span></div>
        <div class="trans-row"><span class="trans-label">Study Duration</span><span class="trans-val">✓ Visible</span></div>
        <div class="trans-row"><span class="trans-label">Study Streak</span><span class="trans-val">✓ Visible</span></div>
        <div class="trans-row"><span class="trans-label">Exact Focus Score</span><span class="trans-no">✗ Hidden</span></div>
        <div class="trans-row"><span class="trans-label">Emotion Data</span><span class="trans-no">✗ Hidden</span></div>
        <div class="trans-row"><span class="trans-label">Camera Feed</span><span class="trans-no">✗ Never stored</span></div>
        <div class="trans-row"><span class="trans-label">Real-time Monitoring</span><span class="trans-no">✗ Daily summary only</span></div>
      </div>

      <button class="logout-btn" onclick="leaveDashboard()">View Different Child</button>
    </div>

  </div>

  <script>
    function getFocusLevel(score) {
      if (score >= 70) return { level:'HIGH', emoji:'⬆', class:'level-high', name:'High Focus', color:'#1D9E75', desc:'Your child had a strong study session today. Their brain was engaged and working well.' };
      if (score >= 45) return { level:'MED', emoji:'➡', class:'level-medium', name:'Medium Focus', color:'#EF9F27', desc:'Your child studied with moderate focus today. Consistent effort is building good habits.' };
      return { level:'LOW', emoji:'⬇', class:'level-low', name:'Low Focus', color:'#E24B4A', desc:'Your child struggled with focus today. This is normal — encourage a proper rest and try again tomorrow.' };
    }

    function calcStreak(sessions) {
      if (!sessions.length) return 0;
      const dates = [...new Set(sessions.map(s => s.date))].sort().reverse();
      const today = new Date().toISOString().split('T')[0];
      let streak = 0, prev = null;
      for (const d of dates) {
        if (!prev) { if (d === today) { streak = 1; prev = d; } else break; }
        else {
          const d1 = new Date(prev), d2 = new Date(d);
          if ((d1-d2)/86400000 === 1) { streak++; prev = d; } else break;
        }
      }
      return streak;
    }

    function getParentInsight(avgScore, sessions, streak) {
      if (!sessions.length) return 'No study sessions recorded today. Encourage them to start with just 20 minutes.';
      if (avgScore >= 80) return '🌟 Exceptional focus today! Your child is in a great study rhythm. Positive reinforcement will help maintain this.';
      if (avgScore >= 65) return '👍 Good study session today. Your child is building consistent habits. Keep the environment supportive.';
      if (avgScore >= 45) return '📚 Moderate focus today. Make sure they have a quiet study space and are not using their phone while studying.';
      if (streak >= 3) return '🔥 Even though today was tough, they have studied ' + streak + ' days in a row. Acknowledge that effort!';
      return '💙 Difficult focus day today. Check if they are getting enough sleep and eating well. Rest is part of studying.';
    }

    async function loadChildData() {
      const username = document.getElementById('child-username').value.trim().toLowerCase();
      const parentName = document.getElementById('parent-name').value.trim();
      const msg = document.getElementById('setup-msg');

      if (!username) { msg.textContent = 'Please enter your child\'s username'; return; }
      if (!parentName) { msg.textContent = 'Please enter your name'; return; }

      try {
        const resp = await fetch('/api/sessions');
        const all = await resp.json();
        const childSessions = all.filter(s => s.name && s.name.toLowerCase() === username);

        if (!childSessions.length) {
          msg.textContent = 'No account found for "' + username + '". Check the username and try again.';
          return;
        }

        // Save to localStorage
        localStorage.setItem('fm_parent_child', username);
        localStorage.setItem('fm_parent_name', parentName);

        showDashboard(username, childSessions, parentName);
      } catch(e) {
        msg.textContent = 'Connection error. Please try again.';
      }
    }

    function showDashboard(username, sessions, parentName) {
      document.getElementById('setup-panel').classList.add('hidden');
      document.getElementById('dashboard-panel').classList.remove('hidden');

      // Header
      const displayName = username.charAt(0).toUpperCase() + username.slice(1);
      document.getElementById('child-avatar').textContent = displayName[0].toUpperCase();
      document.getElementById('child-name-display').textContent = displayName;

      // Today's sessions
      const today = new Date().toISOString().split('T')[0];
      const todaySessions = sessions.filter(s => s.date === today);
      const avgToday = todaySessions.length ? Math.round(todaySessions.reduce((a,s)=>a+s.score,0)/todaySessions.length) : 0;
      const totalTimeToday = Math.round(todaySessions.reduce((a,s)=>a+(s.duration||0),0));

      // Focus level
      const streak = calcStreak(sessions);
      if (todaySessions.length) {
        const lvl = getFocusLevel(avgToday);
        const circle = document.getElementById('level-circle');
        circle.textContent = lvl.emoji;
        circle.className = 'level-circle ' + lvl.class;
        document.getElementById('level-name').textContent = lvl.name;
        document.getElementById('level-name').style.color = lvl.color;
        document.getElementById('level-desc').textContent = lvl.desc;
      } else {
        document.getElementById('level-circle').textContent = '?';
        document.getElementById('level-circle').className = 'level-circle level-none';
        document.getElementById('level-name').textContent = 'No sessions today';
        document.getElementById('level-desc').textContent = 'Your child has not studied yet today.';
      }

      document.getElementById('p-sessions').textContent = todaySessions.length;
      document.getElementById('p-time').textContent = totalTimeToday + 'm';
      document.getElementById('p-streak').textContent = streak;
      document.getElementById('p-insight').textContent = getParentInsight(avgToday, todaySessions, streak);

      // Streak row
      if (streak >= 2) {
        document.getElementById('streak-row').style.display = 'flex';
        document.getElementById('streak-text-main').textContent = streak + ' Day Streak!';
        document.getElementById('streak-text-sub').textContent = streak >= 7 ? 'One full week of studying! Incredible!' : streak >= 3 ? 'Building a great study habit!' : 'Two days in a row — great start!';
      }

      // Week bars
      const bars = document.getElementById('week-bars');
      bars.innerHTML = '';
      const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
      const now = new Date();
      for (let i = 6; i >= 0; i--) {
        const d = new Date(now);
        d.setDate(d.getDate() - i);
        const dateStr = d.toISOString().split('T')[0];
        const daySessions = sessions.filter(s => s.date === dateStr);
        const dayAvg = daySessions.length ? Math.round(daySessions.reduce((a,s)=>a+s.score,0)/daySessions.length) : 0;
        const lvl = daySessions.length ? getFocusLevel(dayAvg) : null;
        const height = daySessions.length ? Math.max(10, dayAvg * 0.7) : 4;
        const color = lvl ? lvl.color : '#1a1a1a';
        const levelText = lvl ? (dayAvg >= 70 ? 'H' : dayAvg >= 45 ? 'M' : 'L') : '';
        bars.innerHTML += '<div class="day-bar-wrap"><div class="day-bar" style="height:' + height + 'px;background:' + color + '"></div><div class="day-label">' + days[d.getDay()] + '</div><div class="day-level" style="color:' + color + '">' + levelText + '</div></div>';
      }
    }

    function leaveDashboard() {
      document.getElementById('setup-panel').classList.remove('hidden');
      document.getElementById('dashboard-panel').classList.add('hidden');
      document.getElementById('setup-msg').textContent = '';
    }

    // Auto-load if returning parent
    const savedChild = localStorage.getItem('fm_parent_child');
    const savedParent = localStorage.getItem('fm_parent_name');
    if (savedChild) document.getElementById('child-username').value = savedChild;
    if (savedParent) document.getElementById('parent-name').value = savedParent;
  </script>
</body>
</html>""")
f.close()
print("parent.html written!")