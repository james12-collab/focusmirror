f = open('templates/wrapped.html', 'w', encoding='utf-8')
f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Focus Wrapped — FocusMirror</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:#0a0a0a;color:#fff;font-family:'Inter',sans-serif;padding:20px;display:flex;flex-direction:column;align-items:center;}
    nav{width:100%;max-width:420px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;}
    .logo{font-size:16px;font-weight:700;color:#1D9E75;}
    .logo span{color:#fff;}
    .nl{font-size:12px;color:#666;text-decoration:none;padding:6px 12px;border-radius:20px;border:1px solid #222;}
    .wrap-card{width:100%;max-width:400px;background:linear-gradient(160deg,#0d2e1f,#0a0a2e 50%,#1a0a2e);border-radius:24px;padding:32px 24px;margin-bottom:16px;border:1px solid rgba(29,158,117,0.3);}
    .month{font-size:10px;color:rgba(255,255,255,0.4);text-transform:uppercase;letter-spacing:4px;margin-bottom:6px;}
    .brand{font-size:12px;font-weight:700;color:#1D9E75;letter-spacing:3px;margin-bottom:28px;}
    .pers-section{text-align:center;margin-bottom:28px;}
    .pers-icon{font-size:64px;margin-bottom:12px;}
    .pers-type{font-size:26px;font-weight:900;margin-bottom:8px;}
    .pers-desc{font-size:12px;color:rgba(255,255,255,0.4);line-height:1.6;max-width:260px;margin:0 auto;}
    .div{height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.08),transparent);margin:22px 0;}
    .stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px;text-align:center;}
    .snum{font-size:36px;font-weight:900;color:#1D9E75;line-height:1;}
    .slbl{font-size:9px;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:2px;margin-top:4px;}
    .streak-box{text-align:center;padding:18px;background:rgba(239,159,39,0.07);border:1px solid rgba(239,159,39,0.2);border-radius:14px;margin-bottom:20px;}
    .sfire{font-size:36px;margin-bottom:6px;}
    .snum2{font-size:48px;font-weight:900;color:#EF9F27;line-height:1;}
    .slbl2{font-size:11px;color:rgba(255,255,255,0.3);margin-top:4px;}
    .hl{display:flex;justify-content:space-between;align-items:center;background:rgba(29,158,117,0.06);border:1px solid rgba(29,158,117,0.15);border-radius:10px;padding:10px 14px;margin-bottom:10px;}
    .hl-l{font-size:11px;color:rgba(255,255,255,0.4);}
    .hl-v{font-size:13px;font-weight:700;color:#1D9E75;}
    .footer{font-size:10px;color:rgba(255,255,255,0.15);text-align:center;margin-top:20px;}
    .actions{width:100%;max-width:400px;display:flex;flex-direction:column;gap:8px;}
    .btn{padding:13px;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;border:none;width:100%;}
    .btn-green{background:#1D9E75;color:#000;}
    .btn-dark{background:#111;color:#888;border:1px solid #222;}
    .nodata{text-align:center;padding:60px 20px;color:#555;max-width:400px;}
    .nodata-icon{font-size:48px;margin-bottom:16px;}
    .go{display:inline-block;margin-top:20px;padding:12px 28px;background:#1D9E75;color:#000;border-radius:12px;font-weight:700;text-decoration:none;font-size:13px;}
  </style>
</head>
<body>
  <nav>
    <div class="logo">Focus<span>Mirror</span></div>
    <a href="/app" class="nl">← App</a>
  </nav>

  <div class="nodata" id="nodata" style="display:none">
    <div class="nodata-icon">🎁</div>
    <h2 style="color:#fff;font-size:18px;margin-bottom:8px">No Wrapped Yet</h2>
    <p>Complete at least 3 study sessions this month to unlock your Focus Wrapped.</p>
    <a href="/app" class="go">Start Studying →</a>
  </div>

  <div class="wrap-card" id="wcard" style="display:none">
    <div class="month" id="wmonth"></div>
    <div class="brand">⚡ FOCUS WRAPPED</div>
    <div class="pers-section">
      <div class="pers-icon" id="wicon">🌙</div>
      <div class="pers-type" id="wtype">Loading...</div>
      <div class="pers-desc" id="wdesc"></div>
    </div>
    <div class="div"></div>
    <div class="stats-grid">
      <div><div class="snum" id="wsess">0</div><div class="slbl">Sessions</div></div>
      <div><div class="snum" id="whours">0h</div><div class="slbl">Study Time</div></div>
      <div><div class="snum" id="wbest">0</div><div class="slbl">Best Score</div></div>
      <div><div class="snum" id="wavg">0</div><div class="slbl">Avg Score</div></div>
    </div>
    <div class="div"></div>
    <div class="streak-box">
      <div class="sfire">🔥</div>
      <div class="snum2" id="wstreak">0</div>
      <div class="slbl2">Day Streak</div>
    </div>
    <div class="hl"><span class="hl-l">🕐 Peak Study Time</span><span class="hl-v" id="wpeak">--</span></div>
    <div class="hl"><span class="hl-l">🏆 Best Grade</span><span class="hl-v" id="wgrade">--</span></div>
    <div class="hl"><span class="hl-l">📅 Most Productive Day</span><span class="hl-v" id="wday">--</span></div>
    <div class="footer">focusmirror.onrender.com · AI Study Tracker</div>
  </div>

  <div class="actions" id="actions" style="display:none">
    <button class="btn btn-green" onclick="downloadWrapped()">📥 Save as Image</button>
    <button class="btn btn-dark" onclick="window.print()">🖨 Print / PDF</button>
  </div>

  <script>
    const PERS = {
      'Morning':    {icon:'🌅',type:'Morning Warrior',   desc:'Your brain peaks at dawn. Early sessions are your superpower.'},
      'Afternoon':  {icon:'⚡',type:'Afternoon Grinder', desc:'Post-lunch is your power zone. Rare and powerful.'},
      'Evening':    {icon:'🌙',type:'Evening Scholar',   desc:'When others wind down, you rise. Evening is your domain.'},
      'Night':      {icon:'🦉',type:'Night Owl',         desc:'The world sleeps, you focus. Late night is when you shine.'},
      'Late Night': {icon:'🌟',type:'Midnight Mind',     desc:'Burning the midnight oil. Pure dedication.'}
    };

    function grade(s){if(s>=90)return'A+';if(s>=80)return'A';if(s>=70)return'B';if(s>=60)return'C';if(s>=50)return'D';return'F';}

    function streak(sessions){
      const dates=[...new Set(sessions.map(s=>s.date))].sort().reverse();
      const today=new Date().toISOString().split('T')[0];
      let str=0,prev=null;
      for(const d of dates){
        if(!prev){if(d===today){str=1;prev=d;}else break;}
        else{const d1=new Date(prev),d2=new Date(d);if((d1-d2)/86400000===1){str++;prev=d;}else break;}
      }
      return str;
    }

    function dayName(dateStr){
      return new Date(dateStr).toLocaleDateString('en',{weekday:'long'});
    }

    async function load(){
      const name=localStorage.getItem('fm_username')||'';
      const resp=await fetch('/api/sessions');
      let all=await resp.json();
      if(name)all=all.filter(s=>s.name&&s.name.toLowerCase()===name.toLowerCase());
      const now=new Date();
      const sessions=all.filter(s=>{
        if(!s.date)return false;
        const d=new Date(s.date);
        return d.getMonth()===now.getMonth()&&d.getFullYear()===now.getFullYear();
      });
      if(sessions.length<3){document.getElementById('nodata').style.display='block';return;}
      document.getElementById('wcard').style.display='block';
      document.getElementById('actions').style.display='flex';
      document.getElementById('wmonth').textContent=now.toLocaleDateString('en',{month:'long',year:'numeric'}).toUpperCase();

      // Best time of day
      const ts={};
      sessions.forEach(s=>{const t=s.time_of_day||'Evening';if(!ts[t])ts[t]=[];ts[t].push(s.score);});
      let bestTime='Evening',bestAvg=0;
      Object.entries(ts).forEach(([t,arr])=>{const a=arr.reduce((x,y)=>x+y)/arr.length;if(a>bestAvg){bestAvg=a;bestTime=t;}});
      const pers=PERS[bestTime]||{icon:'⚖',type:'Balanced Learner',desc:'You focus consistently at all hours.'};
      document.getElementById('wicon').textContent=pers.icon;
      document.getElementById('wtype').textContent=pers.type;
      document.getElementById('wdesc').textContent=pers.desc;

      // Stats
      const scores=sessions.map(s=>s.score);
      const avg=Math.round(scores.reduce((a,b)=>a+b,0)/scores.length);
      const best=Math.max(...scores);
      const totalMins=sessions.reduce((a,s)=>a+(s.duration||0),0);
      const hours=(totalMins/60).toFixed(1);
      document.getElementById('wsess').textContent=sessions.length;
      document.getElementById('whours').textContent=hours+'h';
      document.getElementById('wbest').textContent=best;
      document.getElementById('wavg').textContent=avg;
      document.getElementById('wstreak').textContent=streak(sessions);
      document.getElementById('wpeak').textContent=bestTime;
      document.getElementById('wgrade').textContent=grade(best);

      // Most productive day
      const dayScores={};
      sessions.forEach(s=>{const d=dayName(s.date);if(!dayScores[d])dayScores[d]=[];dayScores[d].push(s.score);});
      let bestDay='--',bestDayAvg=0;
      Object.entries(dayScores).forEach(([d,arr])=>{const a=arr.reduce((x,y)=>x+y)/arr.length;if(a>bestDayAvg){bestDayAvg=a;bestDay=d;}});
      document.getElementById('wday').textContent=bestDay;
    }

    function downloadWrapped(){
      const el=document.getElementById('wcard');
      alert('Tip: Take a screenshot of this card to share on Instagram or WhatsApp!');
    }

    load();
  </script>
</body>
</html>""")
f.close()
print("wrapped.html written!")