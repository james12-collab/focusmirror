content = open('templates/index.html', 'r', encoding='utf-8').read()

# Add YouTube CSS
youtube_css = '''
    .youtube-section { background:#111; border:1px solid #222; border-radius:12px; padding:16px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .youtube-title { font-size:11px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:12px; }
    .youtube-input-group { display:flex; gap:8px; }
    .youtube-input { flex:1; background:#1a1a1a; border:1px solid #333; border-radius:8px; padding:10px 14px; color:#fff; font-size:13px; outline:none; }
    .youtube-input:focus { border-color:#1D9E75; }
    .youtube-input::placeholder { color:#444; }
    .youtube-btn { padding:10px 16px; background:#1D9E75; color:#000; border:none; border-radius:8px; font-size:12px; font-weight:600; cursor:pointer; transition:opacity .2s; }
    .youtube-btn:hover { opacity:0.85; }
    .youtube-btn.loading { opacity:0.5; cursor:not-allowed; }
    .youtube-transcript-box { background:#0d2e1f; border:1px solid #1D9E75; border-radius:8px; padding:12px; margin-top:12px; font-size:12px; line-height:1.5; color:#fff; max-height:150px; overflow-y:auto; }
'''

content = content.replace('</style>', youtube_css + '</style>')

# Add YouTube HTML before notes box
youtube_html = '''
  <div class="youtube-section">
    <div class="youtube-title">🎥 YouTube Note Extractor</div>
    <div class="youtube-input-group">
      <input class="youtube-input" id="youtube-url" type="text" placeholder="Paste YouTube URL...">
      <button class="youtube-btn" onclick="extractYouTubeTranscript()">Extract</button>
    </div>
    <div class="youtube-transcript-box" id="youtube-transcript" style="display:none;"></div>
  </div>

'''

content = content.replace('<div class="notes-box">', youtube_html + '<div class="notes-box">')

# Add YouTube JS
youtube_js = '''
    async function extractYouTubeTranscript() {
      const input = document.getElementById('youtube-url');
      const url = input.value.trim();
      const transcriptBox = document.getElementById('youtube-transcript');
      const btn = event.target;
      
      if (!url) {
        alert('Please enter a YouTube URL');
        return;
      }
      
      btn.classList.add('loading');
      btn.disabled = true;
      transcriptBox.textContent = 'Extracting transcript...';
      transcriptBox.style.display = 'block';
      
      try {
        const resp = await fetch('/youtube-transcript', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({url})
        });
        const data = await resp.json();
        
        if (data.error) {
          transcriptBox.textContent = 'Error: ' + data.error;
        } else if (data.text) {
          transcriptBox.innerHTML = data.text.substring(0, 500) + '...';
          document.getElementById('notes-input').value = data.text;
          alert('✅ Transcript loaded! Now select a processing mode.');
        }
      } catch(e) {
        transcriptBox.textContent = 'Error: ' + e.message;
      } finally {
        btn.classList.remove('loading');
        btn.disabled = false;
      }
    }

'''

content = content.replace('    async function processNotes(mode) {', youtube_js + '\n    async function processNotes(mode) {')

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("YouTube extractor added!")