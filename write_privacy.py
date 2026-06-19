f = open('templates/privacy.html', 'w', encoding='utf-8')
f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy Policy — FocusMirror</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    body{background:#0a0a0a;color:#fff;font-family:'Inter',sans-serif;padding-bottom:60px;}
    nav{display:flex;align-items:center;justify-content:space-between;padding:20px 24px;max-width:700px;margin:0 auto;}
    .logo{font-size:16px;font-weight:700;color:#1D9E75;}
    .logo span{color:#fff;}
    .nl{font-size:12px;color:#666;text-decoration:none;padding:6px 12px;border-radius:20px;border:1px solid #222;}
    .page{max-width:700px;margin:0 auto;padding:0 24px;}
    .hero{padding:32px 0 40px;}
    .hero h1{font-size:32px;font-weight:800;margin-bottom:8px;}
    .hero p{font-size:13px;color:#555;line-height:1.6;}
    .last-updated{font-size:11px;color:#333;margin-top:8px;}
    .section{margin-bottom:36px;}
    .section h2{font-size:16px;font-weight:700;color:#1D9E75;margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid #1a1a1a;}
    .section p{font-size:13px;color:#888;line-height:1.8;margin-bottom:10px;}
    .section ul{padding-left:20px;}
    .section ul li{font-size:13px;color:#888;line-height:1.8;margin-bottom:6px;}
    .highlight{background:#0d2e1f;border:1px solid #1D9E75;border-radius:12px;padding:16px 20px;margin-bottom:16px;}
    .highlight p{color:#1D9E75;font-size:13px;line-height:1.8;margin:0;}
    .contact-box{background:#111;border:1px solid #1a1a1a;border-radius:12px;padding:20px;margin-top:20px;}
    .contact-box h3{font-size:14px;font-weight:700;margin-bottom:8px;}
    .contact-box p{font-size:12px;color:#666;line-height:1.6;}
    .badge{display:inline-block;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;margin-right:6px;margin-bottom:6px;}
    .badge.green{background:#0d2e1f;color:#1D9E75;border:1px solid #1D9E75;}
    .badge.red{background:#2e0d0d;color:#E24B4A;border:1px solid #E24B4A;}
  </style>
</head>
<body>
  <nav>
    <div class="logo">Focus<span>Mirror</span></div>
    <a href="/app" class="nl">Back to App</a>
  </nav>

  <div class="page">
    <div class="hero">
      <h1>Privacy Policy</h1>
      <p>FocusMirror is built on one principle — your data serves you. Not advertisers. Not investors. Not anyone else.</p>
      <div class="last-updated">Last updated: June 2026 · Version 1.0</div>
    </div>

    <div class="highlight">
      <p>🔒 <strong>The short version:</strong> We collect only what we need to show you your focus score. We never sell your data. We never share it with third parties. You can delete everything at any time. Your camera feed is processed locally on your device and never stored on our servers.</p>
    </div>

    <div class="section">
      <h2>What We Collect</h2>
      <p>FocusMirror collects the following data when you use the app:</p>
      <ul>
        <li><strong>Focus metrics</strong> — blink rate, posture score, tab switch frequency, calculated focus score</li>
        <li><strong>Session data</strong> — session duration, time of day, date, username</li>
        <li><strong>Account data</strong> — username and encrypted password hash only. We never store your password in plain text.</li>
        <li><strong>Location data</strong> — approximate location (city level only) if you choose to appear on the World Focus Map. This is optional and can be declined.</li>
      </ul>
      <p><strong>What we do NOT collect:</strong></p>
      <span class="badge red">✗ Camera footage</span>
      <span class="badge red">✗ Video recordings</span>
      <span class="badge red">✗ Audio</span>
      <span class="badge red">✗ Device contacts</span>
      <span class="badge red">✗ Browsing history</span>
      <span class="badge red">✗ Real name</span>
      <span class="badge red">✗ Phone number</span>
      <span class="badge red">✗ Email address</span>
    </div>

    <div class="section">
      <h2>How Your Camera Works</h2>
      <p>FocusMirror uses your device camera to detect facial landmarks for blink rate and posture analysis. This processing happens entirely on your device using Google's BlazeFace model. No camera footage, images or video are ever transmitted to our servers. We receive only the calculated numbers — blink rate, posture score — not any visual data.</p>
      <p>Your face is never stored. Your face is never seen by anyone at FocusMirror. Your camera is used purely as a sensor, the same way a thermometer measures temperature without storing it.</p>
    </div>

    <div class="section">
      <h2>How We Use Your Data</h2>
      <span class="badge green">✓ Show you your focus score</span>
      <span class="badge green">✓ Build your personal study patterns</span>
      <span class="badge green">✓ Generate your Focus DNA profile</span>
      <span class="badge green">✓ Calculate exam readiness</span>
      <span class="badge green">✓ Improve your personal recommendations over time</span>
      <p style="margin-top:12px">With your explicit separate consent only:</p>
      <span class="badge green">✓ Anonymized data used to improve FocusMirror's AI models</span>
      <p style="margin-top:12px">Your anonymized behavioral patterns — never linked to your identity — may be used to train FocusMirror's recommendation engine if you explicitly opt in. You can withdraw this consent at any time from your account settings.</p>
    </div>

    <div class="section">
      <h2>We Never Do This</h2>
      <span class="badge red">✗ Sell your data to anyone</span>
      <span class="badge red">✗ Share your data with advertisers</span>
      <span class="badge red">✗ Share raw data with third parties</span>
      <span class="badge red">✗ Use your data to show you ads</span>
      <span class="badge red">✗ Share your data with your school without consent</span>
      <span class="badge red">✗ Store your camera feed</span>
      <span class="badge red">✗ Access your data for any purpose beyond improving your experience</span>
    </div>

    <div class="section">
      <h2>Parental Consent — Users Under 18</h2>
      <p>FocusMirror requires parental consent before users under 18 can have their data stored. During signup users under 18 are asked to confirm parental awareness before proceeding.</p>
      <p>Parents who have provided consent can view a daily summary of their child's focus performance showing general levels — High, Medium or Low — without access to specific scores or raw data.</p>
      <p>Students can see exactly which categories of data their parent has access to. No surprises. Full transparency about what is shared.</p>
    </div>

    <div class="section">
      <h2>Your Rights</h2>
      <p>You have complete control over your data at all times.</p>
      <ul>
        <li><strong>Right to access</strong> — View all data stored about you from your account settings</li>
        <li><strong>Right to deletion</strong> — Delete your entire account and all associated data permanently at any time</li>
        <li><strong>Right to withdrawal</strong> — Withdraw AI training consent at any time without affecting your account</li>
        <li><strong>Right to portability</strong> — Download all your session data as a JSON file from account settings</li>
        <li><strong>Right to correction</strong> — Request correction of any inaccurate data</li>
      </ul>
      <p>These rights apply regardless of your location. Whether you are in India, the European Union, the United States or anywhere else in the world FocusMirror respects your right to control your own data.</p>
    </div>

    <div class="section">
      <h2>Data Security</h2>
      <p>Passwords are hashed using SHA-256 with a unique salt per user. They are never stored in plain text and are never readable by anyone including FocusMirror's developers.</p>
      <p>Session data is stored on secure servers. We use HTTPS for all data transmission. No sensitive data is stored in browser localStorage.</p>
    </div>

    <div class="section">
      <h2>Sleep Protection Policy</h2>
      <p>FocusMirror automatically stops tracking sessions after midnight and displays a sleep reminder. This is not optional — it is a core product decision based on neuroscience research showing that adolescent brains require 8 to 10 hours of sleep for effective memory consolidation.</p>
      <p>One weekly override is available for students who have a legitimate reason to study past midnight. This override is a conscious deliberate choice not an automatic bypass.</p>
      <p>We believe protecting your sleep is more important than maintaining your streak. Your long term cognitive health always comes first.</p>
    </div>

    <div class="section">
      <h2>Compliance</h2>
      <p>FocusMirror is designed to comply with:</p>
      <ul>
        <li>India's Digital Personal Data Protection Act 2023 (DPDP Act)</li>
        <li>European Union General Data Protection Regulation (GDPR)</li>
        <li>United States Children's Online Privacy Protection Act (COPPA) for users under 13</li>
        <li>Illinois Biometric Information Privacy Act (BIPA)</li>
      </ul>
      <p>If you believe your privacy rights have been violated please contact us immediately.</p>
    </div>

    <div class="contact-box">
      <h3>Contact Us</h3>
      <p>If you have any questions about this privacy policy or how your data is handled please reach out. We are a small team and we read every message personally.</p>
      <p style="margin-top:8px;color:#1D9E75">focusmirror.onrender.com · Built by a student. For students.</p>
    </div>
  </div>
</body>
</html>""")
f.close()
print("privacy.html written!")