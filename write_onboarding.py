html = open('templates/index.html', 'r', encoding='utf-8')
content = html.read()
html.close()

onboarding_css = '''
    .onboarding-overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:#0a0a0a; z-index:1000; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:30px; }
    .onboarding-slide { display:none; flex-direction:column; align-items:center; justify-content:center; text-align:center; max-width:380px; width:100%; }
    .onboarding-slide.active { display:flex; }
    .onboarding-icon { font-size:72px; margin-bottom:24px; }
    .onboarding-title { font-size:24px; font-weight:600; color:#1D9E75; margin-bottom:16px; letter-spacing:1px; }
    .onboarding-desc { font-size:15px; color:#888; line-height:1.8; margin-bottom:32px; }
    .onboarding-desc strong { color:#fff; }
    .onboarding-dots { display:flex; gap:8px; margin-bottom:32px; }
    .onboarding-dot { width:8px; height:8px; border-radius:50%; background:#333; transition:background .3s; }
    .onboarding-dot.active { background:#1D9E75; width:24px; border-radius:4px; }
    .onboarding-next { width:100%; padding:14px; background:#1D9E75; color:#000; border:none; border-radius:12px; font-size:15px; font-weight:700; cursor:pointer; letter-spacing:1px; }
    .onboarding-skip { margin-top:16px; font-size:12px; color:#444; cursor:pointer; text-decoration:underline; }
    .onboarding-features { display:flex; flex-direction:column; gap:12px; width:100%; margin-bottom:24px; }
    .onboarding-feature { display:flex; align-items:center; gap:12px; background:#111; border:1px solid #222; border-radius:10px; padding:12px 16px; text-align:left; }
    .onboarding-feature-icon { font-size:24px; width:40px; text-align:center; }
    .onboarding-feature-text { font-size:13px; color:#888; line-height:1.4; }
    .onboarding-feature-text strong { color:#fff; display:block; margin-bottom:2px; }
'''

onboarding_html = '''
  <div class="onboarding-overlay" id="onboarding">

    <!-- Slide 1 -->
    <div class="onboarding-slide active" id="slide-1">
      <div class="onboarding-icon">🧠</div>
      <div class="onboarding-title">Meet FocusMirror</div>
      <div class="onboarding-desc">
        You sit down to study for <strong>3 hours.</strong><br>
        But your brain checked out after <strong>20 minutes.</strong><br><br>
        FocusMirror uses your camera to track your <strong>real focus</strong> — in real time.
      </div>
      <div class="onboarding-dots">
        <div class="onboarding-dot active"></div>
        <div class="onboarding-dot"></div>
        <div class="onboarding-dot"></div>
      </div>
      <button class="onboarding-next" onclick="nextSlide(2)">Next →</button>
      <div class="onboarding-skip" onclick="skipOnboarding()">Skip</div>
    </div>

    <!-- Slide 2 -->
    <div class="onboarding-slide" id="slide-2">
      <div class="onboarding-icon">👁</div>
      <div class="onboarding-title">How It Works</div>
      <div class="onboarding-features">
        <div class="onboarding-feature">
          <div class="onboarding-feature-icon">😴</div>
          <div class="onboarding-feature-text">
            <strong>Blink Rate</strong>
            Low blinks = eye fatigue. We track it every second.
          </div>
        </div>
        <div class="onboarding-feature">
          <div class="onboarding-feature-icon">🪑</div>
          <div class="onboarding-feature-text">
            <strong>Posture Detection</strong>
            Slouching drains energy. We catch it instantly.
          </div>
        </div>
        <div class="onboarding-feature">
          <div class="onboarding-feature-icon">📱</div>
          <div class="onboarding-feature-text">
            <strong>Distraction Tracking</strong>
            Tab switching and phone use detected automatically.
          </div>
        </div>
        <div class="onboarding-feature">
          <div class="onboarding-feature-icon">⚠</div>
          <div class="onboarding-feature-text">
            <strong>Burnout Prediction</strong>
            We warn you before your brain gives up.
          </div>
        </div>
      </div>
      <div class="onboarding-dots">
        <div class="onboarding-dot"></div>
        <div class="onboarding-dot active"></div>
        <div class="onboarding-dot"></div>
      </div>
      <button class="onboarding-next" onclick="nextSlide(3)">Next →</button>
      <div class="onboarding-skip" onclick="skipOnboarding()">Skip</div>
    </div>

    <!-- Slide 3 -->
    <div class="onboarding-slide" id="slide-3">
      <div class="onboarding-icon">🚀</div>
      <div class="onboarding-title">Ready to Start?</div>
      <div class="onboarding-desc">
        Allow camera access when asked.<br><br>
        Enter your name, press <strong>Start Tracking</strong> and sit normally for <strong>3 seconds</strong> while it calibrates.<br><br>
        Then study as you normally would. <strong>FocusMirror does the rest.</strong>
      </div>
      <div class="onboarding-dots">
        <div class="onboarding-dot"></div>
        <div class="onboarding-dot"></div>
        <div class="onboarding-dot active"></div>
      </div>
      <button class="onboarding-next" onclick="skipOnboarding()" style="background:#1D9E75;">
        Let's Go! 🎯
      </button>
    </div>

  </div>
'''

onboarding_js = '''
    function nextSlide(num) {
      document.querySelectorAll('.onboarding-slide').forEach(s => s.classList.remove('active'));
      document.getElementById('slide-' + num).classList.add('active');
    }

    function skipOnboarding() {
      document.getElementById('onboarding').style.display = 'none';
      localStorage.setItem('onboarding_done', '1');
    }

    // Check if onboarding already done
    if (localStorage.getItem('onboarding_done') === '1') {
      document.getElementById('onboarding').style.display = 'none';
    }

'''

# Insert CSS
content = content.replace('</style>', onboarding_css + '</style>')

# Insert HTML after <body>
content = content.replace('<body>\n  <h1>', '<body>\n' + onboarding_html + '\n  <h1>')

# Insert JS before serviceWorker check
content = content.replace("if('serviceWorker' in navigator)", onboarding_js + "if('serviceWorker' in navigator)")

html = open('templates/index.html', 'w', encoding='utf-8')
html.write(content)
html.close()
print("Onboarding added!")