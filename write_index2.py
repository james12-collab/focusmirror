content = open('templates/index.html', 'r', encoding='utf-8').read()

# Add reset leaderboard button and JS
old = '<div class="lb-header">'
new = '''<div style="max-width:480px;margin:0 auto 8px;text-align:right;">
    <button onclick="resetLeaderboard()" style="background:#2e0d0d;border:1px solid #E24B4A;color:#E24B4A;padding:5px 14px;border-radius:20px;font-size:11px;cursor:pointer;">🗑 Reset Leaderboard</button>
  </div>
  <div class="lb-header">'''
content = content.replace(old, new, 1)

# Add resetLeaderboard JS function
old = 'async function resetSession(){'
new = '''async function resetLeaderboard(){
      if(!confirm('Reset the leaderboard? This cannot be undone.')) return;
      await fetch('/reset-leaderboard', {method:'POST'});
      document.getElementById('leaderboard-list').innerHTML = '<div class="lb-empty">Leaderboard reset! Be the first to score!</div>';
      document.getElementById('rank-badge').textContent = 'Your rank: --';
    }

    async function resetSession(){'''
content = content.replace(old, new, 1)

open('templates/index.html', 'w', encoding='utf-8').write(content)
print("Leaderboard reset button added!")