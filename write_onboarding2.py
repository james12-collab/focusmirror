content = open('templates/index.html', 'r', encoding='utf-8').read()

# Check if onboarding overlay already exists
if 'onboarding-overlay' in content:
    print("Onboarding already in file - checking position...")
    # Make sure it's right after <body>
    if '<body>\n  <div class="onboarding-overlay"' in content:
        print("Position is correct!")
    else:
        print("Position is wrong - fixing...")
        # Remove existing onboarding overlay
        import re
        content = re.sub(r'<div class="onboarding-overlay".*?</div>\s*\n\s*<h1>', '<h1>', content, flags=re.DOTALL)
        # Add it back in right place
        content = content.replace('<body>\n  <h1>', '<body>\n  <div class="onboarding-overlay" id="onboarding" style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0a0a0a;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;">\n    <div style="text-align:center;max-width:380px;width:100%;">\n      <div style="font-size:72px;margin-bottom:24px;">🧠</div>\n      <div style="font-size:24px;font-weight:600;color:#1D9E75;margin-bottom:16px;">Meet FocusMirror</div>\n      <div style="font-size:15px;color:#888;line-height:1.8;margin-bottom:32px;">You sit down to study for <strong style=\\"color:#fff\\">3 hours.</strong><br>But your brain checked out after <strong style=\\"color:#fff\\">20 minutes.</strong><br><br>FocusMirror tracks your <strong style=\\"color:#fff\\">real focus</strong> in real time.</div>\n      <button onclick="document.getElementById(\'onboarding\').style.display=\'none\';localStorage.setItem(\'onboarding_done\',\'1\')" style="width:100%;padding:14px;background:#1D9E75;color:#000;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;">Get Started 🎯</button>\n    </div>\n  </div>\n  <h1>')
        open('templates/index.html', 'w', encoding='utf-8').write(content)
        print("Fixed!")
else:
    print("Adding onboarding...")
    content = content.replace('<body>\n  <h1>', '<body>\n  <div class="onboarding-overlay" id="onboarding" style="position:fixed;top:0;left:0;width:100%;height:100%;background:#0a0a0a;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;">\n    <div style="text-align:center;max-width:380px;width:100%;">\n      <div style="font-size:72px;margin-bottom:24px;">🧠</div>\n      <div style="font-size:24px;font-weight:600;color:#1D9E75;margin-bottom:16px;">Meet FocusMirror</div>\n      <div style="font-size:15px;color:#888;line-height:1.8;margin-bottom:32px;">You sit down to study for <strong style=\\"color:#fff\\">3 hours.</strong><br>But your brain checked out after <strong style=\\"color:#fff\\">20 minutes.</strong><br><br>FocusMirror tracks your <strong style=\\"color:#fff\\">real focus</strong> in real time.</div>\n      <button onclick="document.getElementById(\'onboarding\').style.display=\'none\';localStorage.setItem(\'onboarding_done\',\'1\')" style="width:100%;padding:14px;background:#1D9E75;color:#000;border:none;border-radius:12px;font-size:15px;font-weight:700;cursor:pointer;">Get Started 🎯</button>\n    </div>\n  </div>\n  <h1>')
    open('templates/index.html', 'w', encoding='utf-8').write(content)
    print("Done!")