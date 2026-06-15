content = open('templates/index.html', 'r', encoding='utf-8').read()

# Add notes CSS before closing </style>
notes_css = '''
    .notes-box { background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .notes-title { font-size:11px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }
    .notes-textarea { width:100%; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:12px; color:#fff; font-family:'Segoe UI',sans-serif; font-size:13px; resize:vertical; min-height:100px; outline:none; }
    .notes-textarea:focus { border-color:#1D9E75; }
    .notes-textarea::placeholder { color:#444; }
    .notes-buttons { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:12px; }
    .notes-btn { padding:10px; background:#1a1a1a; border:1px solid #333; color:#888; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer; transition:all .2s; }
    .notes-btn:hover { border-color:#1D9E75; color:#1D9E75; }
    .notes-btn.loading { opacity:0.5; cursor:not-allowed; }
    .notes-output-box { background:#0d2e1f; border:1px solid #1D9E75; border-radius:8px; padding:12px; margin-top:12px; font-size:13px; line-height:1.6; color:#fff; max-height:200px; overflow-y:auto; }
    .notes-output-label { font-size:9px; color:#1D9E75; text-transform:uppercase; letter-spacing:2px; margin-bottom:8px; }
    .notes-output-empty { color:#444; font-style:italic; }
'''

content = content.replace('</style>', notes_css + '</style>')

# Add HTML before badges box
notes_html = '''
  <div class="notes-box">
    <div class="notes-title">📝 AI Note Tracker</div>
    <textarea class="notes-textarea" id="notes-input" placeholder="Paste your notes here... then click a button to process"></textarea>
    <div class="notes-buttons">
      <button class="notes-btn" onclick="processNotes('basic')">📝 Basic</button>
      <button class="notes-btn" onclick="processNotes('summarized')">⚡ Summarized</button>
      <button class="notes-btn" onclick="processNotes('detailed')">📊 Detailed</button>
    </div>
    <div class="notes-output-box">
      <div class="notes-output-label" id="notes-output-label"></div>
      <div id="notes-output" class="notes-output-empty">Output will appear here...</div>
    </div>
  </div>

'''

content = content.replace('<div class="badges-box">', notes_html + '<div class="badges-box">')

# Add notes JS before init()
notes_js = '''
    async function processNotes(mode) {
      const textarea = document.getElementById('notes-input');
      const output = document.getElementById('notes-output');
      const label = document.getElementById('notes-output-label');
      const text = textarea.value.trim();
      
      if (!text) {
        alert('Please enter some notes first!');
        return;
      }
      
      const buttons = document.querySelectorAll('.notes-btn');
      buttons.forEach(b => b.classList.add('loading'));
      
      output.textContent = 'Processing...';
      output.className = '';
      
      try {
        const resp = await fetch('/process-notes', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({text, mode})
        });
        const data = await resp.json();
        
        if (data.error) {
          output.textContent = 'Error: ' + data.error;
          output.className = 'notes-output-empty';
        } else {
          const modeNames = {
            'basic': '📝 Key Points (Basic)',
            'summarized': '⚡ One-Line Summary',
            'detailed': '📊 Detailed Breakdown'
          };
          label.textContent = modeNames[mode];
          output.innerHTML = data.result.replace(/\\n/g, '<br>');
          output.className = '';
        }
      } catch(e) {
        output.textContent = 'Error: ' + e.message;
        output.className = 'notes-output-empty';
      } finally {
        buttons.forEach(b => b.classList.remove('loading'));
      }
    }

'''

content = content.replace('    async function init(){', notes_js + '\n    async function init(){')

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Notes tracker added!")