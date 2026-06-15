content = open('templates/index.html', 'r', encoding='utf-8').read()

# Remove the notes and youtube sections completely
content = content.replace(
    '<div class="youtube-section">',
    '<!-- YouTube removed -->\n  <div style="display:none">'
)
content = content.replace(
    '<div class="notes-box">',
    '<!-- Notes removed -->\n  <div style="display:none">'
)

# Add emotion detection CSS
emotion_css = '''
    .emotion-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:8px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .emotion-card { background:#111; border:1px solid #222; border-radius:12px; padding:14px; text-align:center; }
    .emotion-card .label { font-size:9px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:5px; }
    .emotion-icon { font-size:24px; margin-bottom:6px; }
    .emotion-value { font-size:24px; font-weight:600; margin-bottom:4px; }
    .emotion-bar { height:4px; background:#1a1a1a; border-radius:2px; margin-top:8px; overflow:hidden; }
    .emotion-fill { height:4px; border-radius:2px; transition:width .5s ease; }
'''

content = content.replace('</style>', emotion_css + '</style>')

# Add emotion cards after the grid
emotion_html = '''
  <div class="emotion-grid">
    <div class="emotion-card">
      <div class="label">Stress</div>
      <div class="emotion-icon">😟</div>
      <div class="emotion-value" id="stress-val">0</div>
      <div class="emotion-bar"><div class="emotion-fill" id="stress-bar" style="width:0%;background:#E24B4A"></div></div>
    </div>
    <div class="emotion-card">
      <div class="label">Confusion</div>
      <div class="emotion-icon">😕</div>
      <div class="emotion-value" id="confusion-val">0</div>
      <div class="emotion-bar"><div class="emotion-fill" id="confusion-bar" style="width:0%;background:#EF9F27"></div></div>
    </div>
    <div class="emotion-card">
      <div class="label">Boreout</div>
      <div class="emotion-icon">😐</div>
      <div class="emotion-value" id="boreout-val">0</div>
      <div class="emotion-bar"><div class="emotion-fill" id="boreout-bar" style="width:0%;background:#BA7517"></div></div>
    </div>
    <div class="emotion-card">
      <div class="label">Engagement</div>
      <div class="emotion-icon">😊</div>
      <div class="emotion-value" id="engagement-val">0</div>
      <div class="emotion-bar"><div class="emotion-fill" id="engagement-bar" style="width:0%;background:#1D9E75"></div></div>
    </div>
  </div>

'''

content = content.replace('<div class="badges-box">', emotion_html + '<div class="badges-box">')

# Add emotion update function in JS
emotion_js = '''
    function updateEmotions(stress, confusion, boreout, engagement) {
      document.getElementById('stress-val').textContent = stress;
      document.getElementById('stress-bar').style.width = stress + '%';
      document.getElementById('confusion-val').textContent = confusion;
      document.getElementById('confusion-bar').style.width = confusion + '%';
      document.getElementById('boreout-val').textContent = boreout;
      document.getElementById('boreout-bar').style.width = boreout + '%';
      document.getElementById('engagement-val').textContent = engagement;
      document.getElementById('engagement-bar').style.width = engagement + '%';
    }

'''

content = content.replace('    function updateBadges(', emotion_js + '    function updateBadges(')

# Update updateDashboard to include emotions
old_update = 'updateBadges(d.all_badges, d.badges, d.new_badge);'
new_update = '''updateBadges(d.all_badges, d.badges, d.new_badge);
      updateEmotions(d.stress, d.confusion, d.boreout, d.engagement);'''
content = content.replace(old_update, new_update)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Frontend cleaned and emotions added!")