content = open('templates/index.html', 'r', encoding='utf-8').read()

# ── 1. MASCOT CSS ─────────────────────────────────────────
mascot_css = '''
    .mascot-wrap { max-width:480px; margin:0 auto 12px; display:flex; align-items:center; gap:14px; background:#111; border:1px solid #1a1a1a; border-radius:16px; padding:14px 16px; }
    .mascot-face { width:64px; height:64px; flex-shrink:0; position:relative; }
    .mascot-face svg { width:64px; height:64px; }
    .mascot-bubble { flex:1; }
    .mascot-name { font-size:9px; color:#555; text-transform:uppercase; letter-spacing:2px; margin-bottom:4px; }
    .mascot-msg { font-size:13px; color:#fff; line-height:1.5; font-weight:500; }
    .mascot-mood { font-size:10px; margin-top:4px; }
    .mascot-mood.great { color:#1D9E75; }
    .mascot-mood.good { color:#4A9EEF; }
    .mascot-mood.warn { color:#EF9F27; }
    .mascot-mood.danger { color:#E24B4A; }
    @keyframes mascot-bounce { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-4px)} }
    @keyframes mascot-shake { 0%,100%{transform:rotate(0)} 25%{transform:rotate(-5deg)} 75%{transform:rotate(5deg)} }
    @keyframes mascot-pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.05)} }
    .bounce { animation:mascot-bounce 1s infinite; }
    .shake { animation:mascot-shake 0.5s infinite; }
    .pulse { animation:mascot-pulse 2s infinite; }
'''
content = content.replace('</style>', mascot_css + '\n  </style>')

# ── 2. MASCOT HTML ────────────────────────────────────────
mascot_html = '''  <div class="mascot-wrap" id="mascot-wrap">
    <div class="mascot-face" id="mascot-face">
      <svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" id="mascot-svg">
        <!-- Body -->
        <circle cx="32" cy="32" r="28" fill="#1D9E75" id="m-body"/>
        <!-- Eyes -->
        <ellipse cx="22" cy="26" rx="5" ry="6" fill="white" id="m-leye-white"/>
        <circle cx="23" cy="27" r="3" fill="#0a0a0a" id="m-leye"/>
        <ellipse cx="42" cy="26" rx="5" ry="6" fill="white" id="m-reye-white"/>
        <circle cx="43" cy="27" r="3" fill="#0a0a0a" id="m-reye"/>
        <!-- Eyebrows -->
        <path d="M17 19 Q22 16 27 19" stroke="#0a0a0a" stroke-width="2.5" fill="none" stroke-linecap="round" id="m-lbrow"/>
        <path d="M37 19 Q42 16 47 19" stroke="#0a0a0a" stroke-width="2.5" fill="none" stroke-linecap="round" id="m-rbrow"/>
        <!-- Mouth -->
        <path d="M22 42 Q32 50 42 42" stroke="#0a0a0a" stroke-width="2.5" fill="none" stroke-linecap="round" id="m-mouth"/>
        <!-- Cheeks -->
        <circle cx="16" cy="36" r="5" fill="rgba(255,255,255,0.2)" id="m-lcheek"/>
        <circle cx="48" cy="36" r="5" fill="rgba(255,255,255,0.2)" id="m-rcheek"/>
      </svg>
    </div>
    <div class="mascot-bubble">
      <div class="mascot-name">NOVA — Your Focus Companion</div>
      <div class="mascot-msg" id="mascot-msg">Hi! Enter your name and start tracking. I will be with you every step of the way! 🌟</div>
      <div class="mascot-mood" id="mascot-mood"></div>
    </div>
  </div>

'''
content = content.replace(
    '  <div class="pom-card"',
    mascot_html + '  <div class="pom-card"'
)

# ── 3. MASCOT JS ──────────────────────────────────────────
mascot_js = '''
    // NOVA — AI MASCOT
    const MASCOT_MESSAGES = {
      starting: [
        "Hi! I am Nova. Let us study smarter together! 🌟",
        "Ready to discover your real focus? Let us go! 🚀",
        "I will be watching your focus so you can focus on studying! 👁"
      ],
      great: [
        "You are absolutely crushing it right now! 🔥",
        "This is elite focus! Your brain is fully in the zone! ⚡",
        "Incredible! This is what peak performance looks like! 🏆",
        "I have never seen focus like this! You are unstoppable! 💪",
        "Your brain is operating at maximum capacity. Keep going! 🧠"
      ],
      good: [
        "Solid focus! You are doing really well! 😊",
        "Good momentum! Keep this up and your score will climb! 📈",
        "Nice work! Your brain is engaged and working well! 👍",
        "Consistent focus is the secret weapon. You have it! 🎯"
      ],
      warn: [
        "Hey, I notice your focus dropping a little. Sit up straight! 🪑",
        "Your energy is dipping. Take 3 deep breaths with me. 🌬",
        "Focus score dropping. Remove any distractions around you! 📱",
        "You can do better than this! I believe in you! Come on! 💫"
      ],
      danger: [
        "Your brain is really struggling right now. That is okay! 🤗",
        "Low focus detected. Maybe take a 5 minute break? ☕",
        "I am worried about you. Your focus is very low. Rest first! 💤",
        "Your brain is sending SOS signals. Please take a break! 🆘"
      ],
      burnout: [
        "STOP. Your brain has hit its limit. Take a break NOW! ⛔",
        "Burnout incoming! No amount of willpower fixes this. Rest! 🛑",
        "I care about you too much to let you continue. Break time! ❤"
      ],
      microsleep: [
        "You almost fell asleep! Your body is telling you something! 😴",
        "Micro-sleep detected! Your brain desperately needs rest! 🛌",
        "You fell asleep for a second! Please take a proper break! 💤"
      ],
      milestone: [
        "NEW PERSONAL BEST! I am so proud of you! 🎉",
        "You just hit a milestone! This is incredible progress! 🌟",
        "Badge unlocked! You are building amazing study habits! 🏅"
      ]
    };

    let lastMascotState = '';
    let lastMascotMsg = '';
    let mascotMsgIndex = 0;

    function getMascotState(score, burnoutMins, microsleep) {
      if (microsleep) return 'microsleep';
      if (burnoutMins !== null && burnoutMins !== undefined && burnoutMins <= 3) return 'burnout';
      if (score === 0) return 'starting';
      if (score >= 80) return 'great';
      if (score >= 60) return 'good';
      if (score >= 40) return 'warn';
      return 'danger';
    }

    function updateMascot(score, burnoutMins, microsleep, newBadge) {
      const face = document.getElementById('mascot-face');
      const msg = document.getElementById('mascot-msg');
      const mood = document.getElementById('mascot-mood');
      const body = document.getElementById('m-body');
      const mouth = document.getElementById('m-mouth');
      const lbrow = document.getElementById('m-lbrow');
      const rbrow = document.getElementById('m-rbrow');
      const leye = document.getElementById('m-leye');
      const reye = document.getElementById('m-reye');

      let state = getMascotState(score, burnoutMins, microsleep);
      if (newBadge) state = 'milestone';

      // Only update message when state changes or every 30 seconds
      if (state !== lastMascotState) {
        lastMascotState = state;
        mascotMsgIndex = 0;
        const messages = MASCOT_MESSAGES[state] || MASCOT_MESSAGES.starting;
        const newMsg = messages[Math.floor(Math.random() * messages.length)];
        msg.textContent = newMsg;
      }

      // Update face based on state
      face.className = 'mascot-face';
      if (state === 'great' || state === 'milestone') {
        body.setAttribute('fill', '#1D9E75');
        mouth.setAttribute('d', 'M20 40 Q32 52 44 40');
        lbrow.setAttribute('d', 'M17 17 Q22 13 27 17');
        rbrow.setAttribute('d', 'M37 17 Q42 13 47 17');
        leye.setAttribute('cy', '25');
        reye.setAttribute('cy', '25');
        mood.className = 'mascot-mood great';
        mood.textContent = '😄 Nova is thrilled!';
        face.classList.add('bounce');
      } else if (state === 'good') {
        body.setAttribute('fill', '#1D9E75');
        mouth.setAttribute('d', 'M22 42 Q32 50 42 42');
        lbrow.setAttribute('d', 'M17 19 Q22 16 27 19');
        rbrow.setAttribute('d', 'M37 19 Q42 16 47 19');
        leye.setAttribute('cy', '27');
        reye.setAttribute('cy', '27');
        mood.className = 'mascot-mood good';
        mood.textContent = '😊 Nova is happy!';
        face.classList.add('pulse');
      } else if (state === 'warn') {
        body.setAttribute('fill', '#BA7517');
        mouth.setAttribute('d', 'M24 44 Q32 40 40 44');
        lbrow.setAttribute('d', 'M17 21 Q22 19 27 21');
        rbrow.setAttribute('d', 'M37 21 Q42 19 47 21');
        leye.setAttribute('cy', '27');
        reye.setAttribute('cy', '27');
        mood.className = 'mascot-mood warn';
        mood.textContent = '😟 Nova is concerned';
        face.classList.add('pulse');
      } else if (state === 'danger' || state === 'burnout' || state === 'microsleep') {
        body.setAttribute('fill', '#E24B4A');
        mouth.setAttribute('d', 'M22 46 Q32 40 42 46');
        lbrow.setAttribute('d', 'M17 23 Q22 20 27 22');
        rbrow.setAttribute('d', 'M37 22 Q42 20 47 23');
        leye.setAttribute('cy', '28');
        reye.setAttribute('cy', '28');
        mood.className = 'mascot-mood danger';
        mood.textContent = '😰 Nova is worried!';
        face.classList.add('shake');
      } else {
        body.setAttribute('fill', '#1D9E75');
        mouth.setAttribute('d', 'M22 42 Q32 50 42 42');
        lbrow.setAttribute('d', 'M17 19 Q22 16 27 19');
        rbrow.setAttribute('d', 'M37 19 Q42 16 47 19');
        leye.setAttribute('cy', '27');
        reye.setAttribute('cy', '27');
        mood.className = 'mascot-mood good';
        mood.textContent = '';
        face.classList.add('pulse');
      }
    }

'''

content = content.replace(
    '    // ADAPTIVE POMODORO',
    mascot_js + '\n    // ADAPTIVE POMODORO'
)

# ── 4. CALL MASCOT IN updateDashboard ────────────────────
content = content.replace(
    'adaptPomodoro(d.score);',
    'adaptPomodoro(d.score);\n      updateMascot(d.score, d.burnout_mins, d.microsleep, d.new_badge);'
)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Nova mascot added!")