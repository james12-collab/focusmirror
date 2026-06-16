# Update index.html to save name to localStorage
index = open('templates/index.html', 'r', encoding='utf-8').read()

# Save name to localStorage when tracking starts
old_start = '''function startTracking(){
      const name=document.getElementById('name-input').value.trim();
      if(!name){alert('Please enter your name first!');return;}
      tracking=true;startBtn.disabled=true;startBtn.textContent='Tracking...';
    }'''

new_start = '''function startTracking(){
      const name=document.getElementById('name-input').value.trim();
      if(!name){alert('Please enter your name first!');return;}
      localStorage.setItem('fm_username', name);
      tracking=true;startBtn.disabled=true;startBtn.textContent='Tracking...';
    }'''

index = index.replace(old_start, new_start)

# Load name from localStorage on page load
old_init = '    init();'
new_init = '''    // Load saved name
    const savedName = localStorage.getItem('fm_username');
    if (savedName) {
      document.getElementById('name-input').value = savedName;
    }
    init();'''

index = index.replace(old_init, new_init, 1)

open('templates/index.html', 'w', encoding='utf-8').write(index)
print("index.html updated!")

# ─────────────────────────────────────────
# Update stats.html
# ─────────────────────────────────────────
stats = open('templates/stats.html', 'r', encoding='utf-8').read()

old_stats_load = '    async function loadStats() {\n      const resp = await fetch(\'/api/sessions\');\n      const sessions = await resp.json();'

new_stats_load = '''    async function loadStats() {
      const myName = localStorage.getItem('fm_username') || '';
      const resp = await fetch('/api/sessions');
      let sessions = await resp.json();

      // Show username at top
      if (myName) {
        document.getElementById('stats-username').textContent = myName + "'s Stats";
      }

      // Filter by name if name is set
      if (myName) {
        sessions = sessions.filter(s => s.name && s.name.toLowerCase() === myName.toLowerCase());
      }'''

stats = stats.replace(old_stats_load, new_stats_load)

# Add username heading to stats.html
old_stats_tag = '      <div class="section-tag" style="margin-top:8px">Overview</div>'
new_stats_tag = '''      <div style="font-size:18px;font-weight:700;color:#fff;margin:16px 0 4px" id="stats-username">My Stats</div>
      <div class="section-tag" style="margin-top:8px">Overview</div>'''

stats = stats.replace(old_stats_tag, new_stats_tag)

open('templates/stats.html', 'w', encoding='utf-8').write(stats)
print("stats.html updated!")

# ─────────────────────────────────────────
# Update dna.html
# ─────────────────────────────────────────
dna = open('templates/dna.html', 'r', encoding='utf-8').read()

old_dna_load = '    async function loadDNA() {\n      const resp = await fetch(\'/api/sessions\');\n      const sessions = await resp.json();'

new_dna_load = '''    async function loadDNA() {
      const myName = localStorage.getItem('fm_username') || '';
      const resp = await fetch('/api/sessions');
      let sessions = await resp.json();

      // Filter by name
      if (myName) {
        sessions = sessions.filter(s => s.name && s.name.toLowerCase() === myName.toLowerCase());
        document.getElementById('dna-username').textContent = myName + "'s Focus DNA";
      }'''

dna = dna.replace(old_dna_load, new_dna_load)

# Add username heading to dna.html
old_dna_hero = '      <div class="dna-hero">'
new_dna_hero = '''      <div style="font-size:18px;font-weight:700;color:#fff;margin:16px 0 4px;text-align:center" id="dna-username">My Focus DNA</div>
      <div class="dna-hero">'''

dna = dna.replace(old_dna_hero, new_dna_hero, 1)

open('templates/dna.html', 'w', encoding='utf-8').write(dna)
print("dna.html updated!")

print("\nAll done! Name-based filtering added to Stats and DNA pages.")