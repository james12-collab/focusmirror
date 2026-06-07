html = open('templates/landing.html', 'w', encoding='utf-8')
html.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FocusMirror — AI Study Fatigue Detector</title>
  <meta name="description" content="FocusMirror uses AI to track your real focus while studying. Blink rate, posture, distractions — all in real time.">
  <meta name="theme-color" content="#1D9E75">
  <link rel="manifest" href="/static/manifest.json">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    :root{--green:#1D9E75;--dark:#0a0a0a;--card:#111;--border:#1a1a1a;--text:#fff;--muted:#888;}
    body{background:var(--dark);color:var(--text);font-family:'Inter',sans-serif;overflow-x:hidden;}

    /* NAV */
    nav{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;max-width:1000px;margin:0 auto;}
    .nav-logo{font-size:18px;font-weight:700;color:var(--green);letter-spacing:-0.5px;}
    .nav-logo span{color:#fff;}
    .nav-btn{background:var(--green);color:#000;padding:8px 20px;border-radius:20px;font-size:13px;font-weight:600;text-decoration:none;transition:opacity .2s;}
    .nav-btn:hover{opacity:0.85;}

    /* HERO */
    .hero{text-align:center;padding:60px 24px 40px;max-width:600px;margin:0 auto;}
    .hero-badge{display:inline-flex;align-items:center;gap:6px;background:#0d2e1f;border:1px solid var(--green);color:var(--green);padding:5px 14px;border-radius:20px;font-size:12px;font-weight:500;margin-bottom:24px;}
    .hero-badge-dot{width:6px;height:6px;border-radius:50%;background:var(--green);animation:pulse 2s infinite;}
    @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.5;transform:scale(1.4)}}
    .hero h1{font-size:clamp(32px,8vw,52px);font-weight:800;line-height:1.1;margin-bottom:20px;letter-spacing:-1px;}
    .hero h1 span{color:var(--green);}
    .hero p{font-size:16px;color:var(--muted);line-height:1.7;margin-bottom:36px;}
    .hero-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}
    .btn-primary{background:var(--green);color:#000;padding:14px 28px;border-radius:12px;font-size:15px;font-weight:700;text-decoration:none;transition:all .2s;display:inline-flex;align-items:center;gap:8px;}
    .btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(29,158,117,0.3);}
    .btn-secondary{background:transparent;color:#fff;padding:14px 28px;border-radius:12px;font-size:15px;font-weight:600;text-decoration:none;border:1px solid #333;transition:all .2s;}
    .btn-secondary:hover{border-color:#555;background:#111;}

    /* STATS */
    .stats{display:flex;justify-content:center;gap:40px;padding:40px 24px;border-top:1px solid var(--border);border-bottom:1px solid var(--border);max-width:600px;margin:0 auto;flex-wrap:wrap;}
    .stat{text-align:center;}
    .stat-num{font-size:28px;font-weight:800;color:var(--green);}
    .stat-label{font-size:12px;color:var(--muted);margin-top:4px;}

    /* HOW IT WORKS */
    .section{padding:60px 24px;max-width:800px;margin:0 auto;}
    .section-tag{font-size:11px;color:var(--green);text-transform:uppercase;letter-spacing:3px;margin-bottom:12px;}
    .section h2{font-size:clamp(24px,5vw,36px);font-weight:700;margin-bottom:40px;letter-spacing:-0.5px;}
    .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;}
    .step{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;}
    .step-num{font-size:11px;color:var(--green);font-weight:600;letter-spacing:2px;margin-bottom:12px;}
    .step-icon{font-size:32px;margin-bottom:12px;}
    .step h3{font-size:16px;font-weight:600;margin-bottom:8px;}
    .step p{font-size:13px;color:var(--muted);line-height:1.6;}

    /* FEATURES */
    .features{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;}
    .feature{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:20px;transition:border-color .2s;}
    .feature:hover{border-color:var(--green);}
    .feature-icon{font-size:28px;margin-bottom:12px;}
    .feature h3{font-size:14px;font-weight:600;margin-bottom:6px;}
    .feature p{font-size:12px;color:var(--muted);line-height:1.6;}

    /* DEMO SCREEN */
    .demo{padding:60px 24px;max-width:500px;margin:0 auto;text-align:center;}
    .demo-screen{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:24px;margin:32px 0;text-align:left;}
    .demo-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid var(--border);}
    .demo-row:last-child{border:none;}
    .demo-label{font-size:12px;color:var(--muted);}
    .demo-val{font-size:18px;font-weight:700;}
    .demo-bar{height:4px;background:#1a1a1a;border-radius:2px;margin-top:6px;overflow:hidden;}
    .demo-fill{height:4px;border-radius:2px;transition:width 2s ease;}

    /* CTA */
    .cta{text-align:center;padding:60px 24px;background:linear-gradient(180deg,transparent,#0d2e1f22);border-top:1px solid var(--border);}
    .cta h2{font-size:clamp(24px,5vw,36px);font-weight:700;margin-bottom:16px;letter-spacing:-0.5px;}
    .cta p{font-size:15px;color:var(--muted);margin-bottom:32px;}

    /* FOOTER */
    footer{text-align:center;padding:24px;font-size:12px;color:#333;border-top:1px solid var(--border);}
    footer span{color:var(--green);}
  </style>
</head>
<body>

  <nav>
    <div class="nav-logo">Focus<span>Mirror</span></div>
    <a href="/app" class="nav-btn">Try Free →</a>
  </nav>

  <div class="hero">
    <div class="hero-badge">
      <div class="hero-badge-dot"></div>
      AI-Powered • Free • No signup required
    </div>
    <h1>Your brain has a<br><span>Focus Score.</span><br>Do you know yours?</h1>
    <p>FocusMirror uses your phone camera to track blink rate, posture and distractions in real time — and tells you exactly when your brain is done for the day.</p>
    <div class="hero-btns">
      <a href="/app" class="btn-primary">🧠 Start Tracking Free</a>
      <a href="#how" class="btn-secondary">How it works</a>
    </div>
  </div>

  <div class="stats">
    <div class="stat"><div class="stat-num">0.5s</div><div class="stat-label">Update frequency</div></div>
    <div class="stat"><div class="stat-num">3</div><div class="stat-label">Signals tracked</div></div>
    <div class="stat"><div class="stat-num">100%</div><div class="stat-label">Free forever</div></div>
    <div class="stat"><div class="stat-num">0</div><div class="stat-label">Signups needed</div></div>
  </div>

  <div class="section" id="how">
    <div class="section-tag">How it works</div>
    <h2>Three signals.<br>One honest score.</h2>
    <div class="steps">
      <div class="step">
        <div class="step-num">STEP 01</div>
        <div class="step-icon">📷</div>
        <h3>Open on your phone</h3>
        <p>No app download. No signup. Just open the link and allow camera access.</p>
      </div>
      <div class="step">
        <div class="step-num">STEP 02</div>
        <div class="step-icon">🎯</div>
        <h3>Calibrate in 3 seconds</h3>
        <p>Sit normally for 3 seconds. FocusMirror learns your personal baseline.</p>
      </div>
      <div class="step">
        <div class="step-num">STEP 03</div>
        <div class="step-icon">📊</div>
        <h3>Study as normal</h3>
        <p>The AI tracks your focus score, posture and blink rate every 2 seconds.</p>
      </div>
      <div class="step">
        <div class="step-num">STEP 04</div>
        <div class="step-icon">⚠</div>
        <h3>Get warned before burnout</h3>
        <p>FocusMirror predicts cognitive fatigue before you feel it — and tells you exactly when to take a break.</p>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-tag">Features</div>
    <h2>Everything your<br>brain needs.</h2>
    <div class="features">
      <div class="feature">
        <div class="feature-icon">👁</div>
        <h3>Blink Rate Tracking</h3>
        <p>Normal is 12-20 blinks/min. Below 8 means fatigue. We track it constantly.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🪑</div>
        <h3>Posture Detection</h3>
        <p>Slouching reduces oxygen to the brain by 30%. We catch it the moment it happens.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">📱</div>
        <h3>Distraction Tracking</h3>
        <p>Every tab switch costs 23 minutes of focus. We count every one.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🔥</div>
        <h3>Burnout Prediction</h3>
        <p>Using trend analysis, we warn you minutes before cognitive burnout hits.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🏆</div>
        <h3>Live Leaderboard</h3>
        <p>Compete with others for the highest focus score. Resets daily.</p>
      </div>
      <div class="feature">
        <div class="feature-icon">🎖</div>
        <h3>Achievement Badges</h3>
        <p>Unlock badges for focus milestones. Gamified studying that actually works.</p>
      </div>
    </div>
  </div>

  <div class="cta">
    <h2>Ready to see your<br>real focus score?</h2>
    <p>No download. No signup. Just open and start. 100% free.</p>
    <a href="/app" class="btn-primary" style="font-size:16px;padding:16px 36px;">🧠 Start Tracking Free</a>
    <p style="margin-top:16px;font-size:12px;color:#333;">Built by a student. For students. 🎓</p>
  </div>

  <footer>
    Made with ❤ by a student | <span>focusmirror.onrender.com</span>
  </footer>

  <script>
    // Animate demo bars
    const fills = document.querySelectorAll('.demo-fill');
    fills.forEach(f => {
      const target = f.getAttribute('data-target');
      setTimeout(() => f.style.width = target, 500);
    });
  </script>

</body>
</html>""")
html.close()
print("landing.html written!")