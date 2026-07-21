from flask import Flask, jsonify, render_template_string
import requests
from datetime import date
import random

app = Flask(__name__)

FALLBACK_QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein"},
    {"quote": "It always seems impossible until it's done.", "author": "Nelson Mandela"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "The best way to predict the future is to create it.", "author": "Abraham Lincoln"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"quote": "The way to get started is to quit talking and begin doing.", "author": "Walt Disney"},
    {"quote": "Success is not final, failure is not fatal.", "author": "Winston Churchill"},
    {"quote": "Don't let yesterday take up too much of today.", "author": "Will Rogers"},
    {"quote": "You learn more from failure than from success.", "author": "Unknown"},
    {"quote": "If you are working on something exciting, it will keep you motivated.", "author": "Steve Jobs"},
    {"quote": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"quote": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius"},
    {"quote": "Everything you've ever wanted is on the other side of fear.", "author": "George Addair"},
    {"quote": "Success is not the key to happiness. Happiness is the key to success.", "author": "Albert Schweitzer"},
    {"quote": "The only person you are destined to become is the person you decide to be.", "author": "Ralph Waldo Emerson"},
    {"quote": "Go confidently in the direction of your dreams. Live the life you've imagined.", "author": "Henry David Thoreau"},
    {"quote": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis"},
    {"quote": "Act as if what you do makes a difference. It does.", "author": "William James"},
    {"quote": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein"},
    {"quote": "The two most important days in your life are the day you are born and the day you find out why.", "author": "Mark Twain"},
    {"quote": "Dream big and dare to fail.", "author": "Norman Vaughan"},
    {"quote": "Change your thoughts and you change your world.", "author": "Norman Vincent Peale"},
    {"quote": "Opportunities don't happen. You create them.", "author": "Chris Grosser"},
    {"quote": "Don't be afraid to give up the good to go for the great.", "author": "John D. Rockefeller"},
    {"quote": "I find that the harder I work, the more luck I seem to have.", "author": "Thomas Jefferson"},
    {"quote": "The secret of getting ahead is getting started.", "author": "Mark Twain"},
    {"quote": "Difficulties in your life do not come to destroy you, but to help you realize your hidden potential.", "author": "Unknown"},
    {"quote": "Everything has beauty, but not everyone can see it.", "author": "Confucius"},
    {"quote": "You miss 100% of the shots you don't take.", "author": "Wayne Gretzky"},
    {"quote": "Whatever you are, be a good one.", "author": "Abraham Lincoln"},
    {"quote": "Keep your face always toward the sunshine, and shadows will fall behind you.", "author": "Walt Whitman"},
    {"quote": "You are never too old to set another goal or to dream a new dream.", "author": "C.S. Lewis"},
    {"quote": "The mind is everything. What you think you become.", "author": "Buddha"},
    {"quote": "An unexamined life is not worth living.", "author": "Socrates"},
    {"quote": "Eighty percent of success is showing up.", "author": "Woody Allen"},
    {"quote": "Your time is limited, so don't waste it living someone else's life.", "author": "Steve Jobs"},
    {"quote": "Winning isn't everything, but wanting to win is.", "author": "Vince Lombardi"},
    {"quote": "I attribute my success to this: I never gave or took any excuse.", "author": "Florence Nightingale"},
    {"quote": "Life is 10% what happens to us and 90% how we react to it.", "author": "Charles R. Swindoll"},
    {"quote": "The only way to achieve the impossible is to believe it is possible.", "author": "Charles Kingsleigh"},
    {"quote": "Too many of us are not living our dreams because we are living our fears.", "author": "Les Brown"},
    {"quote": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"},
    {"quote": "In this life we cannot do great things. We can only do small things with great love.", "author": "Mother Teresa"},
    {"quote": "Only a life lived for others is a life worthwhile.", "author": "Albert Einstein"},
    {"quote": "Believe in yourself and all that you are.", "author": "Christian D. Larson"},
    {"quote": "Do what you can, with what you have, where you are.", "author": "Theodore Roosevelt"},
    {"quote": "Knowing yourself is the beginning of all wisdom.", "author": "Aristotle"},
    {"quote": "Where there is love there is life.", "author": "Mahatma Gandhi"},
    {"quote": "The best thing to hold onto in life is each other.", "author": "Audrey Hepburn"},
    {"quote": "We are most alive when we're in love.", "author": "John Updike"},
    {"quote": "Love yourself first and everything else falls into line.", "author": "Lucille Ball"},
    {"quote": "In the end, it's not the years in your life that count. It's the life in your years.", "author": "Abraham Lincoln"},
    {"quote": "Life is short, and it's up to you to make it sweet.", "author": "Sarah Louise Delany"},
    {"quote": "You only live once, but if you do it right, once is enough.", "author": "Mae West"},
    {"quote": "What lies behind us and what lies before us are tiny matters compared to what lies within us.", "author": "Ralph Waldo Emerson"},
    {"quote": "Turn your wounds into wisdom.", "author": "Oprah Winfrey"},
    {"quote": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu"},
    {"quote": "Simplicity is the ultimate sophistication.", "author": "Leonardo da Vinci"},
    {"quote": "Not all those who wander are lost.", "author": "J.R.R. Tolkien"},
    {"quote": "You must be the change you wish to see in the world.", "author": "Mahatma Gandhi"},

    {"quote": "I'm not lazy, I'm on energy-saving mode.", "author": "Unknown"},
    {"quote": "I used to think I was indecisive, but now I'm not so sure.", "author": "Unknown"},
    {"quote": "Common sense is like deodorant. The people who need it most never use it.", "author": "Unknown"},
    {"quote": "I'm on a seafood diet. I see food and I eat it.", "author": "Unknown"},
    {"quote": "Behind every great man is a woman rolling her eyes.", "author": "Jim Carrey"},
    {"quote": "I told my computer I needed a break, and now it won't stop sending me KitKat ads.", "author": "Unknown"},
    {"quote": "I am on a whiskey diet. I've lost three days already.", "author": "Tommy Cooper"},
    {"quote": "The trouble with having an open mind is that people keep coming along and putting things in it.", "author": "Terry Pratchett"},
    {"quote": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison"},
    {"quote": "Age is of no importance unless you're a cheese.", "author": "Billie Burke"},
    {"quote": "I'm sorry, if you were right, I'd agree with you.", "author": "Robin Williams"},
    {"quote": "Procrastination is the art of keeping up with yesterday.", "author": "Don Marquis"},

    {"quote": "Whatever our souls are made of, his and mine are the same.", "author": "Emily Brontë"},
    {"quote": "You had me at hello.", "author": "Jerry Maguire (film)"},
    {"quote": "I love you not only for what you are, but for what I am when I am with you.", "author": "Roy Croft"},
    {"quote": "In all the world, there is no heart for me like yours.", "author": "Maya Angelou"},
    {"quote": "To love and be loved is to feel the sun from both sides.", "author": "David Viscott"},
    {"quote": "I have found the one whom my soul loves.", "author": "Song of Solomon"},
    {"quote": "You are my today and all of my tomorrows.", "author": "Leo Christopher"},
    {"quote": "If I know what love is, it is because of you.", "author": "Hermann Hesse"},
    {"quote": "Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.", "author": "Lao Tzu"},
    {"quote": "Grow old with me, the best is yet to be.", "author": "Robert Browning"},
]

ZEN_RANDOM_URL = "https://zenquotes.io/api/random"
ZEN_TODAY_URL = "https://zenquotes.io/api/today"


def fetch_from_zenquotes(url):
    try:
        response = requests.get(url, timeout=4)
        response.raise_for_status()
        data = response.json()
        item = data[0]
        return {"quote": item["q"], "author": item["a"]}
    except Exception:
        return None


def get_random_quote():
    quote = fetch_from_zenquotes(ZEN_RANDOM_URL)
    return quote if quote else random.choice(FALLBACK_QUOTES)


def get_quote_of_the_day():
    quote = fetch_from_zenquotes(ZEN_TODAY_URL)
    if quote:
        return quote
    index = date.today().toordinal() % len(FALLBACK_QUOTES)
    return FALLBACK_QUOTES[index]


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Spark — Quote of the Day</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;1,500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  html, body { height:100%; overflow-x:hidden; }
  body {
    min-height:100vh; display:flex; align-items:center; justify-content:center;
    background: radial-gradient(ellipse at 50% 0%, #1a1533 0%, #0a0818 55%, #050410 100%);
    font-family:'Inter', sans-serif; padding:24px; position:relative;
  }
  #sky { position:fixed; inset:0; z-index:0; display:block; }

  .wrap {
    width:100%; max-width:600px; position:relative; z-index:1;
    display:flex; flex-direction:column; align-items:center;
  }

  .quote-body { transition: opacity 0.15s ease; width:100%; }
  .quote-body.hidden { opacity:0; }

  .quote-text {
    font-family:'Fraunces', serif; font-style:italic; font-weight:500;
    font-size:32px; line-height:1.5; color:#fdfaf3; margin-bottom:14px;
    text-shadow: 0 2px 30px rgba(0,0,0,0.7), 0 0 60px rgba(0,0,0,0.4);
    text-align:center;
  }
  .author {
    font-size:16px; font-weight:700; color:#fbbf24;
    text-shadow:0 2px 12px rgba(0,0,0,0.6);
    width:100%; text-align:right; margin-bottom:14px;
  }
  .author::before { content:'— '; opacity:0.7; }

  .actions { display:flex; gap:10px; margin-top:22px; flex-wrap:wrap; justify-content:center; }
  button {
    font-family:'Inter',sans-serif; font-weight:600; font-size:14px;
    padding:13px 22px; border-radius:13px; border:none; cursor:pointer;
    display:flex; align-items:center; gap:8px;
    transition:all 0.2s cubic-bezier(0.22,1,0.36,1); color:#fff;
  }
  button:hover { transform:translateY(-2px) scale(1.03); }
  button:active { transform:translateY(0) scale(0.97); }
  button:disabled { opacity:0.6; cursor:default; transform:none; }
  .primary { background:linear-gradient(135deg,#fbbf24,#f97316); color:#3b1e0e; box-shadow:0 10px 28px rgba(251,191,36,0.55); }
  .primary:hover { box-shadow:0 14px 36px rgba(251,191,36,0.75); }
  .btn-copy { background:linear-gradient(135deg,#38bdf8,#6366f1); box-shadow:0 10px 25px rgba(56,189,248,0.45); }
  .btn-share { background:linear-gradient(135deg,#34d399,#059669); box-shadow:0 10px 25px rgba(52,211,153,0.45); }

  .toast {
    position:fixed; bottom:28px; left:50%; transform:translateX(-50%) translateY(20px);
    background:rgba(20,15,35,0.92); border:1px solid rgba(251,191,36,0.3); color:#fde68a;
    padding:13px 22px; border-radius:13px; font-size:14px; font-weight:500;
    opacity:0; pointer-events:none; transition:all 0.3s ease; box-shadow:0 12px 30px rgba(0,0,0,0.5);
  }
  .toast.show { opacity:1; transform:translateX(-50%) translateY(0); }

  @media (max-width:480px){
    .quote-text{ font-size:24px; }
  }
</style>
</head>
<body>
  <canvas id="sky"></canvas>

  <div class="wrap">
    <div class="quote-body" id="quoteBody">
      <div class="quote-text" id="quoteText">{{ quote }}</div>
      <div class="author" id="quoteAuthor">{{ author }}</div>
    </div>
    <div class="actions">
      <button class="primary" id="newBtn" onclick="newQuote()"><span id="newBtnLabel"> New quote</span></button>
      <button class="btn-copy" onclick="copyQuote()"> Copy</button>
      <button class="btn-share" onclick="shareQuote()"> Share</button>
    </div>
  </div>
  <div class="toast" id="toast"></div>

<script>
  const sky = document.getElementById('sky');
  const skyCtx = sky.getContext('2d');
  let W, H, stars = [];

  function resizeSky(){
    W = sky.width = window.innerWidth;
    H = sky.height = window.innerHeight;
    stars = [];
    const count = Math.floor((W * H) / 8000);
    for (let i = 0; i < count; i++){
      stars.push({
        x: Math.random()*W, y: Math.random()*H,
        r: Math.random()*1.4+0.3,
        phase: Math.random()*Math.PI*2,
        twinkleSpeed: 0.5+Math.random()*1.2,
        vx: (Math.random()-0.5) * 0.04,
        vy: (Math.random()-0.5) * 0.04,
      });
    }
  }
  window.addEventListener('resize', resizeSky);
  resizeSky();

  let shootingStars = [];
  function maybeSpawnShootingStar(){
    if (Math.random() < 0.006 && shootingStars.length < 1){
      const startX = Math.random() * W * 0.6 + W * 0.1;
      shootingStars.push({ x: startX, y: -10, vx: 5+Math.random()*3, vy: 3+Math.random()*1.5, life: 1 });
    }
  }

  const satellite = {
    x: -120, y: Math.random()*H*0.4 + 40,
    vx: 0.28, vy: 0.06,
  };
  function drawSatellite(){
    satellite.x += satellite.vx;
    satellite.y += satellite.vy;
    if (satellite.x > W + 120) { satellite.x = -120; satellite.y = Math.random()*H*0.4 + 40; }

    skyCtx.save();
    skyCtx.translate(satellite.x, satellite.y);
    const angle = Math.atan2(satellite.vy, satellite.vx);
    skyCtx.rotate(angle);
    const s = 2.2;

    const bodyGrad = skyCtx.createLinearGradient(-7*s, -6*s, 7*s, 6*s);
    bodyGrad.addColorStop(0, '#e8ecf2');
    bodyGrad.addColorStop(0.5, '#aab2c0');
    bodyGrad.addColorStop(1, '#6b7280');
    skyCtx.fillStyle = bodyGrad;
    skyCtx.fillRect(-7*s, -5*s, 14*s, 10*s);
    skyCtx.strokeStyle = 'rgba(30,35,45,0.6)';
    skyCtx.lineWidth = 0.8;
    skyCtx.strokeRect(-7*s, -5*s, 14*s, 10*s);

    skyCtx.fillStyle = 'rgba(212,168,83,0.85)';
    skyCtx.fillRect(-4*s, -2.5*s, 8*s, 5*s);

    [-1, 1].forEach(dir => {
      const px = dir === -1 ? -30*s : 9*s;
      const panelGrad = skyCtx.createLinearGradient(px, -3*s, px, 3*s);
      panelGrad.addColorStop(0, '#3a5fae');
      panelGrad.addColorStop(0.5, '#5c86d6');
      panelGrad.addColorStop(1, '#2c4785');
      skyCtx.fillStyle = panelGrad;
      skyCtx.fillRect(px, -3*s, 21*s, 6*s);
      skyCtx.strokeStyle = 'rgba(230,235,245,0.55)';
      skyCtx.lineWidth = 0.5;
      skyCtx.strokeRect(px, -3*s, 21*s, 6*s);
      for (let i = 1; i < 6; i++){
        skyCtx.beginPath();
        skyCtx.moveTo(px + i*3.5*s, -3*s);
        skyCtx.lineTo(px + i*3.5*s, 3*s);
        skyCtx.stroke();
      }
      skyCtx.strokeStyle = 'rgba(150,155,165,0.7)';
      skyCtx.lineWidth = 1.2*s;
      skyCtx.beginPath();
      skyCtx.moveTo(dir === -1 ? -7*s : 7*s, 0);
      skyCtx.lineTo(px + (dir===-1 ? 21*s : 0), 0);
      skyCtx.stroke();
    });

    skyCtx.strokeStyle = 'rgba(210,215,225,0.8)';
    skyCtx.lineWidth = 1*s;
    skyCtx.beginPath();
    skyCtx.moveTo(3*s, -5*s); skyCtx.lineTo(6*s, -13*s);
    skyCtx.stroke();
    skyCtx.beginPath();
    skyCtx.ellipse(6*s, -14*s, 3.2*s, 1.6*s, 0.3, 0, Math.PI*2);
    skyCtx.fillStyle = 'rgba(225,228,235,0.85)';
    skyCtx.fill();
    skyCtx.strokeStyle = 'rgba(140,145,155,0.7)';
    skyCtx.lineWidth = 0.5;
    skyCtx.stroke();

    skyCtx.restore();

    const blink = 0.4 + 0.6 * Math.abs(Math.sin(Date.now() * 0.005));
    skyCtx.beginPath();
    skyCtx.arc(satellite.x, satellite.y, 2.4*s*0.5, 0, Math.PI*2);
    skyCtx.fillStyle = `rgba(255,90,90,${blink})`;
    skyCtx.shadowColor = 'rgba(255,90,90,0.8)';
    skyCtx.shadowBlur = 6;
    skyCtx.fill();
    skyCtx.shadowBlur = 0;
  }

  let explodeParticles = [];
  let reformParticles = [];
  const starColors = ['255,230,180', '255,255,255', '190,220,255', '255,200,150'];

  function samplePointsForText(quoteStr, authorStr, boxWidth){
    const off = document.createElement('canvas');
    off.width = boxWidth;
    off.height = 400;
    const octx = off.getContext('2d');
    octx.fillStyle = '#ffffff';

    octx.font = 'italic 500 32px Georgia, serif';
    octx.textAlign = 'center';
    const words = quoteStr.split(' ');
    let line = '', y = 34, lineHeight = 40;
    const lines = [];
    words.forEach((word, i) => {
      const test = line + word + ' ';
      if (octx.measureText(test).width > boxWidth - 10 && i > 0) {
        lines.push(line); line = word + ' ';
      } else line = test;
    });
    lines.push(line);
    lines.forEach(l => { octx.fillText(l.trim(), boxWidth/2, y); y += lineHeight; });

    y += 20;
    octx.font = 'bold 16px Arial';
    octx.textAlign = 'right';
    octx.fillText('— ' + authorStr, boxWidth - 5, y);

    const imgData = octx.getImageData(0, 0, off.width, off.height).data;
    const points = [];
    const step = 4;
    for (let py = 0; py < off.height; py += step){
      for (let px = 0; px < off.width; px += step){
        const idx = (py * off.width + px) * 4;
        if (imgData[idx+3] > 100) points.push({ x: px, y: py });
      }
    }
    return points;
  }

  function startExplode(rect, quoteStr, authorStr){
    const points = samplePointsForText(quoteStr, authorStr, rect.width);
    explodeParticles = points.map(p => {
      const angle = Math.random() * Math.PI * 2;
      const speed = 1.5 + Math.random() * 4;
      return {
        x: rect.left + p.x, y: rect.top + p.y,
        vx: Math.cos(angle) * speed, vy: Math.sin(angle) * speed,
        life: 1, size: 0.8 + Math.random()*1.6,
        color: starColors[Math.floor(Math.random()*starColors.length)],
      };
    });
  }

  function startReform(rect, quoteStr, authorStr){
    const points = samplePointsForText(quoteStr, authorStr, rect.width);
    reformParticles = points.map(p => {
      const tx = rect.left + p.x, ty = rect.top + p.y;
      const angle = Math.random() * Math.PI * 2;
      const dist = 120 + Math.random() * 260;
      return {
        sx: tx + Math.cos(angle)*dist, sy: ty + Math.sin(angle)*dist,
        tx, ty, progress: 0, size: 0.8 + Math.random()*1.6,
        color: starColors[Math.floor(Math.random()*starColors.length)],
      };
    });
  }

  function drawGlowStar(x, y, size, alpha, colorRGB, sparkle){
    const glowR = size * 5;
    const grad = skyCtx.createRadialGradient(x, y, 0, x, y, glowR);
    grad.addColorStop(0, `rgba(${colorRGB},${alpha})`);
    grad.addColorStop(0.35, `rgba(${colorRGB},${alpha*0.35})`);
    grad.addColorStop(1, `rgba(${colorRGB},0)`);
    skyCtx.beginPath();
    skyCtx.arc(x, y, glowR, 0, Math.PI*2);
    skyCtx.fillStyle = grad;
    skyCtx.fill();

    skyCtx.beginPath();
    skyCtx.arc(x, y, size * 0.6, 0, Math.PI*2);
    skyCtx.fillStyle = `rgba(255,255,255,${Math.min(1, alpha*1.3)})`;
    skyCtx.fill();

    if (sparkle && alpha > 0.5){
      skyCtx.strokeStyle = `rgba(255,255,255,${(alpha-0.5)*1.2})`;
      skyCtx.lineWidth = 0.7;
      const len = size * 3.5;
      skyCtx.beginPath();
      skyCtx.moveTo(x - len, y); skyCtx.lineTo(x + len, y);
      skyCtx.moveTo(x, y - len); skyCtx.lineTo(x, y + len);
      skyCtx.stroke();
    }
  }

  function drawExplode(){
    explodeParticles = explodeParticles.filter(p => {
      p.x += p.vx; p.y += p.vy; p.vx *= 0.97; p.vy *= 0.97; p.life -= 0.045;
      if (p.life <= 0) return false;
      drawGlowStar(p.x, p.y, p.size, p.life, p.color, p.size > 1.6);
      return true;
    });
  }

  function drawReform(){
    let stillGoing = false;
    reformParticles.forEach(p => {
      if (p.progress < 1) { p.progress += 0.055; stillGoing = true; }
      const t = Math.min(p.progress, 1);
      const ease = 1 - Math.pow(1-t, 3);
      const x = p.sx + (p.tx - p.sx) * ease;
      const y = p.sy + (p.ty - p.sy) * ease;
      const alpha = 0.3 + t*0.7;
      drawGlowStar(x, y, p.size, alpha, p.color, p.size > 1.6);
    });
    return stillGoing;
  }

  function drawSky(t){
    skyCtx.clearRect(0, 0, W, H);

    stars.forEach(s => {
      s.x += s.vx; s.y += s.vy;
      if (s.x < 0) s.x = W; if (s.x > W) s.x = 0;
      if (s.y < 0) s.y = H; if (s.y > H) s.y = 0;
      const twinkle = 0.4 + 0.6 * Math.abs(Math.sin(t * 0.001 * s.twinkleSpeed + s.phase));
      skyCtx.beginPath();
      skyCtx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      skyCtx.fillStyle = `rgba(255,255,255,${twinkle})`;
      skyCtx.fill();
    });

    drawSatellite();

    maybeSpawnShootingStar();
    shootingStars.forEach(s => {
      const grad = skyCtx.createLinearGradient(s.x, s.y, s.x - s.vx*11, s.y - s.vy*11);
      grad.addColorStop(0, `rgba(255,244,214,${s.life})`);
      grad.addColorStop(1, 'rgba(255,244,214,0)');
      skyCtx.strokeStyle = grad; skyCtx.lineWidth = 2; skyCtx.lineCap = 'round';
      skyCtx.beginPath();
      skyCtx.moveTo(s.x, s.y); skyCtx.lineTo(s.x - s.vx*11, s.y - s.vy*11); skyCtx.stroke();
      s.x += s.vx; s.y += s.vy; s.life -= 0.02;
    });
    shootingStars = shootingStars.filter(s => s.life > 0 && s.y < H + 50 && s.x < W + 50);

    if (explodeParticles.length) drawExplode();
    if (reformParticles.length) drawReform();

    requestAnimationFrame(drawSky);
  }
  requestAnimationFrame(drawSky);

  const qText = document.getElementById('quoteText');
  const qAuthor = document.getElementById('quoteAuthor');
  const quoteBody = document.getElementById('quoteBody');
  const toast = document.getElementById('toast');
  const newBtn = document.getElementById('newBtn');

  // Quietly try to upgrade to a fresh quote after initial fast render, without blocking page load
  (async () => {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 6000);
      const res = await fetch('/quote/today', { signal: controller.signal });
      clearTimeout(timeoutId);
      const data = await res.json();
      if (data && data.quote) {
        qText.textContent = data.quote;
        qAuthor.textContent = data.author;
      }
    } catch(e) { /* silently keep the fallback quote already shown */ }
  })();

  function showToast(msg){
    toast.textContent = msg; toast.classList.add('show');
    setTimeout(()=> toast.classList.remove('show'), 1800);
  }

  async function newQuote(){
    newBtn.disabled = true;
    const rect = quoteBody.getBoundingClientRect();

    startExplode(rect, qText.textContent, qAuthor.textContent);
    quoteBody.classList.add('hidden');

    const fetchPromise = (async () => {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);
        const res = await fetch('/quote', { signal: controller.signal });
        clearTimeout(timeoutId);
        return await res.json();
      } catch(err){
        showToast('Could not fetch a new quote — try again');
        return null;
      }
    })();

    const [data] = await Promise.all([
      fetchPromise,
      new Promise(r => setTimeout(r, 280))
    ]);

    if (data) {
      qText.textContent = data.quote;
      qAuthor.textContent = data.author;
    }

    const newRect = quoteBody.getBoundingClientRect();
    startReform(newRect, qText.textContent, qAuthor.textContent);

    await new Promise(r => setTimeout(r, 420));

    reformParticles = [];
    quoteBody.classList.remove('hidden');
    newBtn.disabled = false;
  }

  function copyQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    navigator.clipboard.writeText(text).then(()=> showToast('Copied to clipboard ✅'));
  }

  function shareQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    if (navigator.share) navigator.share({ text, title: 'Daily Spark' }).catch(()=>{});
    else navigator.clipboard.writeText(text).then(()=> showToast('Copied — share it anywhere ✅'));
  }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    # Serve instantly from local fallback — no blocking external call on page load
    index = date.today().toordinal() % len(FALLBACK_QUOTES)
    q = FALLBACK_QUOTES[index]
    return render_template_string(HTML_PAGE, quote=q["quote"], author=q["author"])

@app.route("/quote")
def random_quote():
    return jsonify(get_random_quote())

@app.route("/quote/today")
def quote_of_the_day():
    return jsonify(get_quote_of_the_day())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)