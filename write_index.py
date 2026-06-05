html = open('templates/index.html', 'r', encoding='utf-8')
content = html.read()
html.close()

# Add theme toggle button after h1
content = content.replace(
    '<h1>FocusMirror</h1>',
    '''<div style="display:flex;align-items:center;justify-content:space-between;max-width:480px;margin:0 auto 12px;">
  <h1 style="margin-bottom:0;">FocusMirror</h1>
  <button onclick="toggleTheme()" id="theme-btn" style="background:#1a1a1a;border:1px solid #333;color:#888;padding:6px 14px;border-radius:20px;font-size:12px;cursor:pointer;">☀ Light</button>
</div>'''
)

# Add light mode CSS and toggle function before </style>
content = content.replace(
    '</style>',
    '''
    body.light { background:#f5f5f5; color:#111; }
    body.light .card { background:#fff; border-color:#ddd; }
    body.light .name-box { background:#fff; border-color:#ddd; }
    body.light .name-input { background:#f0f0f0; border-color:#ccc; color:#111; }
    body.light .alert-box { background:#fff; border-color:#ddd; }
    body.light .bars { background:#fff; border-color:#ddd; }
    body.light .graph-box { background:#fff; border-color:#ddd; }
    body.light .heatmap-box { background:#fff; border-color:#ddd; }
    body.light .leaderboard-box { background:#fff; border-color:#ddd; }
    body.light .status { background:#fff; }
    body.light .bar-track { background:#e0e0e0; }
    body.light .lb-row { border-color:#eee; }
    body.light .reset-btn { background:#f0f0f0; color:#555; border-color:#ddd; }
    </style>'''
)

# Add toggle function before </script>
content = content.replace(
    "if('serviceWorker' in navigator)",
    '''function toggleTheme() {
      const body = document.body;
      const btn = document.getElementById('theme-btn');
      if (body.classList.contains('light')) {
        body.classList.remove('light');
        btn.textContent = '☀ Light';
        localStorage.setItem('theme', 'dark');
      } else {
        body.classList.add('light');
        btn.textContent = '🌙 Dark';
        localStorage.setItem('theme', 'light');
      }
    }
    // Load saved theme
    if (localStorage.getItem('theme') === 'light') {
      document.body.classList.add('light');
      document.getElementById('theme-btn').textContent = '🌙 Dark';
    }

    if('serviceWorker' in navigator)'''
)

html = open('templates/index.html', 'w', encoding='utf-8')
html.write(content)
html.close()
print("Theme toggle added!")