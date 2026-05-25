html = open('templates/index.html', 'w', encoding='utf-8')
html.write("""<!DOCTYPE html>
<html>
<head>
  <title>FocusMirror</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#1D9E75">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="FocusMirror">
  <link rel="manifest" href="/static/manifest.json">
  <link rel="apple-touch-icon" href="/static/icon-192.png">
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { background:#0a0a0a; color:#fff; font-family:'Segoe UI',sans-serif; padding:16px; }
    h1 { font-size:18px; font-weight:300; letter-spacing:4px; text-transform:uppercase; margin-bottom:12px; color:#1D9E75; text-align:center; }
    .cam-wrap { position:relative; border-radius:12px; overflow:hidden; border:1px solid #222; background:#111; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    #video { width:100%; display:block; transform:scaleX(-1); }
    #overlay { position:absolute; top:0; left:0; width:100%; height:100%; transform:scaleX(-1); }
    .cam-label { position:absolute; top:8px; right:8px; background:rgba(0,0,0,0.6); padding:3px 8px; border-radius:20px; font-size:10px; color:#1D9E75; letter-spacing:2px; z-index:10; }
    .status { text-align:center; font-size:12px; color:#666; margin-bottom:12px; padding:8px; background:#111; border-radius:8px; max-width:480px; margin-left:auto; margin-right:auto; }
    .status.good { color:#1D9E75; }
    .status.warn { color:#EF9F27; }
    .status.error { color:#E24B4A; }
    .burnout-banner { display:none; background:#2e0d0d; border:1px solid #E24B4A; border-radius:10px; padding:10px; margin-bottom:12px; font-size:12px; color:#E24B4A; text-align:center; max-width:480px; margin-left:auto; margin-right:auto; }
    .grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .card { background:#111; border:1px solid #222; border-radius:12px; padding:14px; text-align:center; }
    .card .label { font-size:9px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:5px; }
    .card .value { font-size:28px; font-weight:600; }
    .card .sub { font-size:10px; color:#555; margin-top:2px; }
    .alert-box { background:#111; border:1px solid #222; border-radius:12px; padding:14px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .alert-box .state { font-size:9px; letter-spacing:3px; text-transform:uppercase; margin-bottom:6px; color:#888; }
    .alert-box .message { font-size:14px; line-height:1.5; }
    .alert-box.good .message { color:#1D9E75; }
    .alert-box.warn .message { color:#EF9F27; }
    .alert-box.danger .message { color:#E24B4A; }
    .bars { background:#111; border:1px solid #222; border-radius:12px; padding:14px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .section-label { font-size:9px; color:#666; text-transform:uppercase; letter-spacing:2px; margin-bottom:10px; }
    .bar-track { background:#1a1a1a; border-radius:4px; height:6px; margin-bottom:10px; }
    .bar-fill { height:6px; border-radius:4px; transition:width 1s ease; }
    .bar-row { display:flex; justify-content:space-between; margin-bottom:4px; }
    .bar-name { font-size:11px; color:#888; }
    .bar-num { font-size:11px; color:#fff; font-weight:500; }
    .graph-box { background:#111; border:1px solid #222; border-radius:12px; padding:14px; margin-bottom:12px; max-width:480px; margin-left:auto; margin-right:auto; }
    .heatmap-box { background:#111; border:1px solid #222; border-radius:12px; padding:14px; max-width:480px; margin-left:auto; margin-right:auto; margin-bottom:16px; }
    .heatmap-grid { display:flex; gap:3px; flex-wrap:wrap; margin-top:8px; min-height:32px; }
    .heatmap-cell { width:28px; height:28px; border-radius:5px; display:flex; align-items:center; justify-content:center; font-size:9px; color:rgba(255,255,255,0.8); font-weight:600; }
    .start-btn { display:block; width:100%; max-width:480px; margin:0 auto 8px; padding:12px; background:#1D9E75; color:#000; border:none; border-radius:12px; font-size:14px; font-weight:600; cursor:pointer; }
    .start-btn:disabled { background:#1a1a1a; color:#444; cursor:not-allowed; }
    .reset-btn { display:block; width:100%; max-width:480px; margin:0 auto 12px; padding:10px; background:#1a1a1a; color:#888; border:1px solid #333; border-radius:12px; font-size:13px; cursor:pointer; }
  </style>
</head>
<body>
  <h1>FocusMirror</h1>
  <div class="burnout-banner" id="burnout-banner"></div>
  <div class="cam-wrap">
    <video id="video" autoplay muted playsinline></video>
    <canvas id="overlay"></canvas>
    <div class="cam-label">LIVE</div>
  </div>
  <div class="status" id="status">Loading models...</div>
  <button class="start-btn" id="start-btn" disabled onclick="startTracking()">Start Tracking</button>
  <button class="reset-btn" onclick="resetSession()">Reset Session (new visitor)</button>
  <div class="grid">
    <div class="card"><div class="label">Focus Score</div><div class="value" id="score-val" style="color:#1D9E75">--</div><div class="sub">out of 100</div></div>
    <div class="card"><div class="label">Blink Rate</div><div class="value" id="bpm-val" style="color:#185FA5">--</div><div class="sub">per minute</div></div>
    <div class="card"><div class="label">Posture</div><div class="value" id="posture-val" style="color:#BA7517">--</div><div class="sub">score</div></div>
    <div class="card"><div class="label">Session</div><div class="value" id="session-val" style="color:#888">--</div><div class="sub">minutes</div></div>
  </div>
  <div class="alert-box good" id="alert-box">
    <div class="state" id="state-label">STARTING</div>
    <div class="message" id="rec-text">Press Start Tracking to begin</div>
  </div>
  <div class="bars">
    <div class="section-label">Live Metrics</div>
    <div class="bar-row"><span class="bar-name">Focus Score</span><span class="bar-num" id="b-score">0</span></div>
    <div class="bar-track"><div class="bar-fill" id="bf-score" style="width:0%;background:#1D9E75"></div></div>
    <div class="bar-row"><span class="bar-name">Posture</span><span class="bar-num" id="b-posture">0</span></div>
    <div class="bar-track"><div class="bar-fill" id="bf-posture" style="width:0%;background:#185FA5"></div></div>
    <div class="bar-row"><span class="bar-name">Blink Health</span><span class="bar-num" id="b-blink">0</span></div>
    <div class="bar-track"><div class="bar-fill" id="bf-blink" style="width:0%;background:#BA7517"></div></div>
  </div>
  <div class="graph-box">
    <div class="section-label">Focus Trend</div>
    <canvas id="focusChart" height="80"></canvas>
  </div>
  <div class="heatmap-box">
    <div class="section-label">Focus Heatmap</div>
    <div style="font-size:10px;color:#444;margin-bottom:6px;">Green=High  Yellow=Medium  Red=Low</div>
    <div class="heatmap-grid" id="heatmap-grid"><div style="color:#333;font-size:11px;">Builds every 10 seconds...</div></div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.2.0/dist/tf.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/blazeface@0.0.7/dist/blazeface.min.js"></script>
  <script>
    const video=document.getElementById('video');
    const canvas=document.getElementById('overlay');
    const ctx=canvas.getContext('2d');
    const statusEl=document.getElementById('status');
    const startBtn=document.getElementById('start-btn');
    const scoreHistory=[];
    const timeLabels=[];
    const chartCtx=document.getElementById('focusChart').getContext('2d');
    const chart=new Chart(chartCtx,{type:'line',data:{labels:timeLabels,datasets:[{data:scoreHistory,borderColor:'#1D9E75',backgroundColor:'rgba(29,158,117,0.08)',fill:true,tension:0.4,pointRadius:0,borderWidth:2}]},options:{responsive:true,animation:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false},ticks:{color:'#444',font:{size:9}}},y:{min:0,max:100,grid:{color:'rgba(255,255,255,0.05)'},ticks:{color:'#444',font:{size:9},stepSize:25}}}}});

    function scoreColor(s){return s>=70?'#1D9E75':s>=45?'#EF9F27':'#E24B4A';}

    function updateHeatmap(data){
      if(!data||!data.length)return;
      const grid=document.getElementById('heatmap-grid');
      grid.innerHTML='';
      data.forEach(d=>{
        const cell=document.createElement('div');
        cell.className='heatmap-cell';
        cell.style.background=scoreColor(d.score);
        cell.style.opacity=0.4+(d.score/100)*0.6;
        cell.textContent=d.score;
        grid.appendChild(cell);
      });
    }

    function updateDashboard(d){
      document.getElementById('score-val').textContent=d.score;
      document.getElementById('bpm-val').textContent=d.bpm;
      document.getElementById('posture-val').textContent=d.posture;
      document.getElementById('session-val').textContent=d.session_minutes;
      document.getElementById('state-label').textContent=d.state;
      document.getElementById('rec-text').textContent=d.recommendation;
      document.getElementById('score-val').style.color=scoreColor(d.score);
      document.getElementById('b-score').textContent=d.score;
      document.getElementById('b-posture').textContent=d.posture;
      document.getElementById('bf-score').style.width=d.score+'%';
      document.getElementById('bf-posture').style.width=d.posture+'%';
      const bh=Math.max(0,100-Math.abs(d.bpm-15)*6);
      document.getElementById('b-blink').textContent=bh;
      document.getElementById('bf-blink').style.width=bh+'%';
      scoreHistory.push(d.score);
      timeLabels.push(new Date().toLocaleTimeString());
      if(scoreHistory.length>60){scoreHistory.shift();timeLabels.shift();}
      chart.update();
      updateHeatmap(d.heatmap);
      const box=document.getElementById('alert-box');
      box.className='alert-box';
      if(d.score>=70)box.classList.add('good');
      else if(d.score>=45)box.classList.add('warn');
      else box.classList.add('danger');
      const banner=document.getElementById('burnout-banner');
      if(d.burnout_mins!==null&&d.burnout_mins!==undefined){
        banner.style.display='block';
        banner.textContent=d.burnout_mins===0?'BURNOUT - Stop now. Take a 20 min break.':'Burnout in '+d.burnout_mins+' min - take a break soon.';
      }else{banner.style.display='none';}
    }

    let model=null,tracking=false,lastSend=0;
    let blinkTimes=[];
    let earPrev=0.5;

    // Posture tracking variables
    let baselineFaceHeight=null;
    let baselineNoseX=null;
    let postureCalibrated=false;
    let calibrationFrames=0;
    let faceHeightSamples=[];
    let noseXSamples=[];

    function getBPM(){
      const now=Date.now();
      blinkTimes=blinkTimes.filter(t=>now-t<60000);
      return blinkTimes.length;
    }

    function estimatePosture(p){
      try{
        const [x1,y1]=p.topLeft;
        const [x2,y2]=p.bottomRight;
        const faceHeight=y2-y1;
        const faceWidth=x2-x1;
        const nose=p.landmarks[2];
        const noseX=nose[0];
        const faceCenterX=(x1+x2)/2;

        // Calibrate baseline in first 30 frames
        if(!postureCalibrated){
          faceHeightSamples.push(faceHeight);
          noseXSamples.push(faceCenterX);
          calibrationFrames++;
          if(calibrationFrames>=30){
            baselineFaceHeight=faceHeightSamples.reduce((a,b)=>a+b)/faceHeightSamples.length;
            baselineNoseX=noseXSamples.reduce((a,b)=>a+b)/noseXSamples.length;
            postureCalibrated=true;
          }
          return 100;
        }

        let score=100;

        // If face is significantly bigger than baseline = slouching forward
        const heightRatio=faceHeight/baselineFaceHeight;
        if(heightRatio>1.15) score-=30;
        else if(heightRatio>1.08) score-=15;

        // If face is significantly smaller = leaning back/away
        if(heightRatio<0.85) score-=20;

        // Head tilt sideways = distracted
        const leftEye=p.landmarks[0];
        const rightEye=p.landmarks[1];
        const eyeTilt=Math.abs(leftEye[1]-rightEye[1])/(x2-x1);
        if(eyeTilt>0.08) score-=20;

        // Head turned sideways
        const noseOffset=Math.abs(noseX-faceCenterX)/(faceWidth/2);
        if(noseOffset>0.15) score-=15;

        return Math.max(0,Math.min(100,score));
      }catch{return 100;}
    }

    function detectBlink(p){
      try{
        // Use eye landmark positions relative to face height
        const [x1,y1]=p.topLeft;
        const [x2,y2]=p.bottomRight;
        const faceHeight=y2-y1;
        const leftEye=p.landmarks[0];
        const rightEye=p.landmarks[1];
        const mouth=p.landmarks[3];

        // Distance from eyes to mouth relative to face height
        // When blinking, eyes move slightly downward
        const eyeAvgY=(leftEye[1]+rightEye[1])/2;
        const eyeToMouth=Math.abs(mouth[1]-eyeAvgY)/faceHeight;

        // Normalized EAR approximation
        // Lower value = eyes more closed
        const ear=eyeToMouth;
        return ear;
      }catch{return 0.5;}
    }

    async function resetSession(){
      await fetch('/reset',{method:'POST'});
      scoreHistory.length=0;timeLabels.length=0;chart.update();
      document.getElementById('heatmap-grid').innerHTML='<div style="color:#333;font-size:11px;">Builds every 10 seconds...</div>';
      document.getElementById('score-val').textContent='--';
      document.getElementById('bpm-val').textContent='--';
      document.getElementById('posture-val').textContent='--';
      document.getElementById('session-val').textContent='--';
      document.getElementById('rec-text').textContent='Session reset! Press Start Tracking.';
      document.getElementById('state-label').textContent='READY';
      tracking=false;startBtn.disabled=false;startBtn.textContent='Start Tracking';
      blinkTimes=[];earPrev=0.5;
      baselineFaceHeight=null;baselineNoseX=null;
      postureCalibrated=false;calibrationFrames=0;
      faceHeightSamples=[];noseXSamples=[];
    }

    async function detect(){
      if(!model){requestAnimationFrame(detect);return;}
      canvas.width=video.videoWidth;canvas.height=video.videoHeight;
      ctx.clearRect(0,0,canvas.width,canvas.height);
      if(tracking){
        try{
          const preds=await model.estimateFaces(video,false);
          if(preds.length>0){
            const p=preds[0];
            const [x1,y1]=p.topLeft;
            const [x2,y2]=p.bottomRight;

            // Draw face box
            ctx.strokeStyle='#1D9E75';ctx.lineWidth=2;
            ctx.strokeRect(x1,y1,x2-x1,y2-y1);

            // Draw landmarks
            p.landmarks.forEach(([lx,ly])=>{
              ctx.beginPath();ctx.arc(lx,ly,3,0,2*Math.PI);
              ctx.fillStyle='#1D9E75';ctx.fill();
            });

            // Blink detection
            const ear=detectBlink(p);
            if(ear<0.35&&earPrev>=0.35)blinkTimes.push(Date.now());
            earPrev=ear;

            // Posture
            const posture=estimatePosture(p);
            const bpm=getBPM();

            // Show calibration status
            if(!postureCalibrated){
              statusEl.textContent='Calibrating posture... '+(calibrationFrames)+'/30 frames';
              statusEl.className='status warn';
            }else{
              statusEl.textContent='Tracking - BPM: '+bpm+' | Posture: '+posture;
              statusEl.className='status good';
            }

            const now=Date.now();
            if(now-lastSend>=2000){
              lastSend=now;
              try{
                const resp=await fetch('/sensor',{
                  method:'POST',
                  headers:{'Content-Type':'application/json'},
                  body:JSON.stringify({ear,bpm,posture,expression:'Neutral',stress:0,confusion:0,zoneout:0})
                });
                const data=await resp.json();
                updateDashboard(data);
              }catch(e){console.log('Send error:',e);}
            }
          }else{
            statusEl.textContent='No face detected - face the camera';
            statusEl.className='status warn';
          }
        }catch(e){console.log('Detection error:',e);}
      }
      requestAnimationFrame(detect);
    }

    function startTracking(){
      tracking=true;
      startBtn.disabled=true;
      startBtn.textContent='Tracking...';
      statusEl.textContent='Calibrating posture baseline - sit normally for 3 seconds...';
      statusEl.className='status warn';
    }

    async function init(){
      try{
        statusEl.textContent='Starting camera...';
        const stream=await navigator.mediaDevices.getUserMedia({video:{facingMode:'user'},audio:false});
        video.srcObject=stream;
        await new Promise(r=>video.onloadedmetadata=r);
        statusEl.textContent='Loading BlazeFace model...';
        model=await blazeface.load();
        statusEl.textContent='Ready! Press Start Tracking.';
        statusEl.className='status good';
        startBtn.disabled=false;
        requestAnimationFrame(detect);
      }catch(e){
        statusEl.textContent='Error: '+e.message;
        statusEl.className='status error';
      }
    }

    init();

    if('serviceWorker' in navigator){
      navigator.serviceWorker.register('/static/sw.js')
        .then(()=>console.log('PWA ready!'))
        .catch(e=>console.log('SW error:',e));
    }
  </script>
</body>
</html>""")
html.close()
print("index.html written successfully!")