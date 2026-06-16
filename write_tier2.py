content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. CSS ──────────────────────────────────────────────────────────────
tier2_css = '''
    .microsleep-banner { display:none; background:#1a0a2e; border:1px solid #9B59B6; border-radius:10px; padding:10px; margin-bottom:12px; font-size:13px; color:#9B59B6; text-align:center; max-width:480px; margin-left:auto; margin-right:auto; }
    .microsleep-card { background:#111; border:1px solid #222; border-radius:12px; padding:12px 16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; display:flex; align-items:center; justify-content:space-between; }
    .microsleep-left { display:flex; align-items:center; gap:10px; }
    .microsleep-icon { font-size:22px; }
    .microsleep-label { font-size:11px; color:#666; text-transform:uppercase; letter-spacing:2px; }
    .microsleep-count { font-size:22px; font-weight:700; color:#9B59B6; }
    .voice-toggle { display:flex; align-items:center; gap:8px; }
    .voice-label { font-size:11px; color:#666; }
    .toggle-switch { position:relative; width:40px; height:22px; }
    .toggle-switch input { opacity:0; width:0; height:0; }
    .toggle-slider { position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background:#1a1a1a; border:1px solid #333; border-radius:22px; transition:.3s; }
    .toggle-slider:before { position:absolute; content:""; height:16px; width:16px; left:2px; bottom:2px; background:#555; border-radius:50%; transition:.3s; }
    input:checked + .toggle-slider { background:#0d2e1f; border-color:#1D9E75; }
    input:checked + .toggle-slider:before { transform:translateX(18px); background:#1D9E75; }
    .break-overlay { position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.92); z-index:10001; display:none; align-items:center; justify-content:center; padding:20px; }
    .break-overlay.show { display:flex; }
    .break-card { background:#111; border:1px solid #1D9E75; border-radius:20px; padding:28px; max-width:360px; width:100%; text-align:center; }
    .break-icon { font-size:56px; margin-bottom:12px; }
    .break-title { font-size:18px; font-weight:700; color:#fff; margin-bottom:6px; }
    .break-subtitle { font-size:12px; color:#666; margin-bottom:20px; }
    .break-activity { background:#0d2e1f; border:1px solid #1D9E75; border-radius:12px; padding:16px; margin-bottom:16px; }
    .break-activity-icon { font-size:36px; margin-bottom:8px; }
    .break-activity-name { font-size:16px; font-weight:700; color:#1D9E75; margin-bottom:6px; }
    .break-activity-desc { font-size:12px; color:#888; line-height:1.6; }
    .break-timer { font-size:32px; font-weight:800; color:#fff; margin-bottom:16px; }
    .break-btns { display:flex; gap:8px; }
    .break-btn-next { flex:1; padding:11px; background:#1D9E75; color:#000; border:none; border-radius:10px; font-size:13px; font-weight:700; cursor:pointer; }
    .break-btn-skip { padding:11px 16px; background:#1a1a1a; color:#666; border:1px solid #333; border-radius:10px; font-size:12px; cursor:pointer; }
'''
content = content.replace('</style>', tier2_css + '\n  </style>')

# ── 2. HTML ──────────────────────────────────────────────────────────────
# Micro-sleep banner
ms_banner = '''  <div class="microsleep-banner" id="ms-banner">
    😴 MICRO-SLEEP DETECTED — You are falling asleep. Sit up and blink hard!
  </div>

'''
content = content.replace('  <div class="burnout-banner"', ms_banner + '  <div class="burnout-banner"')

# Micro-sleep card + voice toggle (after start button)
ms_card = '''
  <div class="microsleep-card">
    <div class="microsleep-left">
      <div class="microsleep-icon">😴</div>
      <div>
        <div class="microsleep-label">Micro-Sleeps</div>
        <div class="microsleep-count" id="ms-count">0</div>
      </div>
    </div>
    <div class="voice-toggle">
      <span class="voice-label">🔊 Voice</span>
      <label class="toggle-switch">
        <input type="checkbox" id="voice-toggle" checked onchange="toggleVoice()">
        <span class="toggle-slider"></span>
      </label>
    </div>
  </div>

'''
content = content.replace(
    '  <button class="reset-btn"',
    ms_card + '  <button class="reset-btn"'
)

# Break activity overlay
break_html = '''  <div class="break-overlay" id="break-overlay">
    <div class="break-card">
      <div class="break-icon" id="brk-icon">🧘</div>
      <div class="break-title">Break Time!</div>
      <div class="break-subtitle" id="brk-subtitle">Your brain needs a reset</div>
      <div class="break-activity">
        <div class="break-activity-icon" id="brk-act-icon">🏃</div>
        <div class="break-activity-name" id="brk-act-name">Loading...</div>
        <div class="break-activity-desc" id="brk-act-desc"></div>
      </div>
      <div class="break-timer" id="brk-timer"></div>
      <div class="break-btns">
        <button class="break-btn-next" onclick="nextActivity()">Next Activity →</button>
        <button class="break-btn-skip" onclick="closeBreak()">Skip Break</button>
      </div>
    </div>
  </div>

'''
content = content.replace(
    '  <div class="report-overlay"',
    break_html + '  <div class="report-overlay"'
)

# ── 3. JAVASCRIPT ─────────────────────────────────────────────────────────
tier2_js = '''
    // ═══════════════════════════════════════════
    // VOICE ALERTS
    // ═══════════════════════════════════════════
    let voiceEnabled = true;
    let lastSpoken = {};
    const SPEAK_COOLDOWN = 60000; // 60 seconds between same message

    function toggleVoice() {
      voiceEnabled = document.getElementById('voice-toggle').checked;
    }

    function speak(text, key) {
      if (!voiceEnabled) return;
      if (!('speechSynthesis' in window)) return;
      const now = Date.now();
      if (key && lastSpoken[key] && now - lastSpoken[key] < SPEAK_COOLDOWN) return;
      if (key) lastSpoken[key] = now;
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.rate = 0.9;
      utter.pitch = 1.0;
      utter.volume = 0.8;
      window.speechSynthesis.speak(utter);
    }

    // ═══════════════════════════════════════════
    // MICRO-SLEEP DETECTION
    // ═══════════════════════════════════════════
    let earBelowThresholdFrames = 0;
    let microsleepDetected = false;
    let totalMicrosleeps = 0;
    let lastMicrosleepAlert = 0;
    const MS_THRESHOLD = 0.15;  // very closed eyes
    const MS_FRAMES = 8;        // ~3 seconds at 30fps

    function checkMicrosleep(ear) {
      if (ear < MS_THRESHOLD) {
        earBelowThresholdFrames++;
        if (earBelowThresholdFrames >= MS_FRAMES && !microsleepDetected) {
          microsleepDetected = true;
          totalMicrosleeps++;
          document.getElementById('ms-count').textContent = totalMicrosleeps;
          document.getElementById('ms-banner').style.display = 'block';
          playChime('burnout');
          speak('Wake up! Micro-sleep detected. You are falling asleep.', 'microsleep');
          setTimeout(() => {
            document.getElementById('ms-banner').style.display = 'none';
          }, 5000);
        }
      } else {
        earBelowThresholdFrames = 0;
        microsleepDetected = false;
      }
      return microsleepDetected;
    }

    // ═══════════════════════════════════════════
    // BREAK ACTIVITY SUGGESTER
    // ═══════════════════════════════════════════
    const BREAK_ACTIVITIES = [
      {
        icon: '🏃',
        name: '10 Jumping Jacks',
        desc: 'Stand up and do 10 jumping jacks. Increases blood flow to the brain by 30% instantly.',
        duration: 30
      },
      {
        icon: '💧',
        name: 'Drink Water',
        desc: 'Drink a full glass of water. Even 1% dehydration reduces cognitive performance by 10%.',
        duration: 20
      },
      {
        icon: '👁',
        name: '20-20-20 Rule',
        desc: 'Look at something 20 feet away for 20 seconds. Resets your eye muscles completely.',
        duration: 20
      },
      {
        icon: '🌬',
        name: 'Box Breathing',
        desc: 'Breathe in 4 seconds, hold 4, out 4, hold 4. Repeat 4 times. Activates your calm system.',
        duration: 64
      },
      {
        icon: '🙆',
        name: 'Neck & Shoulder Stretch',
        desc: 'Roll your neck slowly left and right, then roll your shoulders back 5 times each.',
        duration: 30
      },
      {
        icon: '🚶',
        name: 'Walk Around',
        desc: 'Walk around the room for 60 seconds. Movement reactivates the prefrontal cortex.',
        duration: 60
      },
      {
        icon: '🤲',
        name: 'Cold Water on Face',
        desc: 'Splash cold water on your face. Triggers the dive reflex — instant mental reset.',
        duration: 20
      },
      {
        icon: '😄',
        name: 'Power Smile',
        desc: 'Smile as wide as you can for 10 seconds. Releases dopamine and serotonin immediately.',
        duration: 10
      }
    ];

    let currentActivity = 0;
    let breakTimerInterval = null;
    let breakSecondsLeft = 0;
    let breakShownForScore = false;

    function showBreak(reason) {
      const act = BREAK_ACTIVITIES[currentActivity % BREAK_ACTIVITIES.length];
      document.getElementById('brk-icon').textContent = act.icon;
      document.getElementById('brk-subtitle').textContent = reason || 'Science-backed micro-break';
      document.getElementById('brk-act-icon').textContent = act.icon;
      document.getElementById('brk-act-name').textContent = act.name;
      document.getElementById('brk-act-desc').textContent = act.desc;
      breakSecondsLeft = act.duration;
      document.getElementById('brk-timer').textContent = breakSecondsLeft + 's';
      document.getElementById('break-overlay').classList.add('show');
      speak('Break time! ' + act.name + '. ' + act.desc, 'break');
      clearInterval(breakTimerInterval);
      breakTimerInterval = setInterval(() => {
        breakSecondsLeft--;
        document.getElementById('brk-timer').textContent = breakSecondsLeft + 's';
        if (breakSecondsLeft <= 0) {
          clearInterval(breakTimerInterval);
          document.getElementById('brk-timer').textContent = '✅ Done!';
        }
      }, 1000);
    }

    function nextActivity() {
      clearInterval(breakTimerInterval);
      currentActivity++;
      const act = BREAK_ACTIVITIES[currentActivity % BREAK_ACTIVITIES.length];
      document.getElementById('brk-act-icon').textContent = act.icon;
      document.getElementById('brk-act-name').textContent = act.name;
      document.getElementById('brk-act-desc').textContent = act.desc;
      breakSecondsLeft = act.duration;
      document.getElementById('brk-timer').textContent = breakSecondsLeft + 's';
      speak(act.name + '. ' + act.desc, 'break_next');
      breakTimerInterval = setInterval(() => {
        breakSecondsLeft--;
        document.getElementById('brk-timer').textContent = breakSecondsLeft + 's';
        if (breakSecondsLeft <= 0) {
          clearInterval(breakTimerInterval);
          document.getElementById('brk-timer').textContent = '✅ Done!';
        }
      }, 1000);
    }

    function closeBreak() {
      clearInterval(breakTimerInterval);
      document.getElementById('break-overlay').classList.remove('show');
      breakShownForScore = false;
      speak('Good job! Back to studying. Stay focused.', 'back');
    }

'''

content = content.replace(
    '    // SOUND ALERTS',
    tier2_js + '\n    // SOUND ALERTS'
)

# ── 4. Hook micro-sleep into detect loop ─────────────────────────────────
old_send = '''            const posture=estimatePosture(p);
            const bpm=getBPM();'''

new_send = '''            const posture=estimatePosture(p);
            const bpm=getBPM();
            const ms=checkMicrosleep(ear);'''

content = content.replace(old_send, new_send)

# Pass microsleep to /sensor
old_sensor = "body:JSON.stringify({ear,bpm,posture,expression:'Neutral',stress:0,confusion:0,zoneout:0})"
new_sensor = "body:JSON.stringify({ear,bpm,posture,expression:'Neutral',stress:0,confusion:0,zoneout:0,microsleep:ms})"
content = content.replace(old_sensor, new_sensor)

# ── 5. Voice alerts in updateDashboard ───────────────────────────────────
old_voice = "if (d.burnout_mins !== null && d.burnout_mins !== undefined && d.burnout_mins <= 5) { playChime('burnout'); }"
new_voice = """if (d.burnout_mins !== null && d.burnout_mins !== undefined && d.burnout_mins <= 5) {
        playChime('burnout');
        speak('Warning! Burnout in ' + d.burnout_mins + ' minutes. Consider taking a break.', 'burnout');
        if (!breakShownForScore) { breakShownForScore = true; showBreak('Burnout approaching — take a micro-break now'); }
      }
      if (d.score < 40 && tracking) {
        speak('Your focus score is very low. Try sitting up straight.', 'lowscore');
      }
      if (d.microsleep_count > 0) {
        document.getElementById('ms-count').textContent = d.microsleep_count;
      }"""
content = content.replace(old_voice, new_voice)

# ── 6. Voice on badge unlock ─────────────────────────────────────────────
old_badge_popup = "function showBadgePopup(badge) {"
new_badge_popup = """function showBadgePopup(badge) {
      speak('Achievement unlocked! ' + badge.name, 'badge');"""
content = content.replace(old_badge_popup, new_badge_popup, 1)

# ── 7. Voice on report card ──────────────────────────────────────────────
old_report = "document.getElementById('report-overlay').classList.add('show');"
new_report = """document.getElementById('report-overlay').classList.add('show');
      speak('Session complete! You scored ' + score + ' points with a grade of ' + grade + '. ' + insight, 'report');"""
content = content.replace(old_report, new_report, 1)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Tier 2 done — Micro-Sleep Detection, Voice Alerts, Break Activity Suggester!")