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
]

ZEN_RANDOM_URL = "https://zenquotes.io/api/random"
ZEN_TODAY_URL = "https://zenquotes.io/api/today"


def fetch_from_zenquotes(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        item = data[0]
        return {"quote": item["q"], "author": item["a"]}
    except Exception:
        return None


def get_random_quote():
    quote = fetch_from_zenquotes(ZEN_RANDOM_URL)
    if quote:
        return quote
    return random.choice(FALLBACK_QUOTES)


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
    min-height:100vh;
    display:flex; align-items:center; justify-content:center;
    background: linear-gradient(-45deg, #ff6b9d, #a855f7, #6366f1, #22d3ee, #ff6b9d);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family:'Inter', sans-serif;
    padding:24px;
    position:relative;
  }
  @keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
  .orb {
    position:fixed; border-radius:50%; filter:blur(70px); opacity:0.55; pointer-events:none;
  }
  .orb1 { width:380px; height:380px; background:#fbbf24; top:-100px; left:-100px; animation:float1 10s ease-in-out infinite; }
  .orb2 { width:320px; height:320px; background:#f472b6; bottom:-80px; right:-80px; animation:float2 13s ease-in-out infinite; }
  .orb3 { width:240px; height:240px; background:#67e8f9; top:55%; left:80%; animation:float3 9s ease-in-out infinite; }
  @keyframes float1 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(60px,80px);} }
  @keyframes float2 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(-70px,-50px);} }
  @keyframes float3 { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(-50px,60px) scale(1.2);} }

  .particle {
    position:fixed; border-radius:50%; background:rgba(255,255,255,0.85); pointer-events:none;
    animation: drift linear infinite;
    box-shadow:0 0 4px rgba(255,255,255,0.6);
  }
  @keyframes drift {
    0% { transform:translateY(-10vh) translateX(0) scale(0); opacity:0; }
    10% { opacity:1; }
    50% { transform:translateY(50vh) translateX(20px) scale(1); }
    90% { opacity:1; }
    100% { transform:translateY(110vh) translateX(-15px) scale(1); opacity:0; }
  }

  .rope-wrap {
    position:fixed; top:0; z-index:2;
  }
  .rope-inner {
    display:flex; flex-direction:column; align-items:center;
    transform-origin:top center;
  }
  .rope {
    width:14px; min-height:40px;
    background:
      repeating-linear-gradient(120deg,
        #c9a876 0px, #c9a876 4px,
        #a8895f 4px, #a8895f 8px);
    box-shadow:
      inset -2px 0 3px rgba(0,0,0,0.35),
      inset 2px 0 3px rgba(255,240,210,0.25),
      0 0 6px rgba(0,0,0,0.3);
    border-radius:3px;
    position:relative;
    opacity:0.92;
  }
  .rope::before, .rope::after {
    content:'';
    position:absolute; width:1px; background:#b89a6d; opacity:0.7;
  }
  .rope::before { top:15%; left:-4px; height:14px; transform:rotate(-25deg); }
  .rope::after { top:55%; right:-4px; height:11px; transform:rotate(20deg); }
  .knot {
    width:22px; height:14px; margin-top:-3px;
    background:radial-gradient(circle at 35% 30%, #c9a876, #7d5f3a 75%);
    border-radius:50% 50% 40% 40%;
    box-shadow:0 3px 6px rgba(0,0,0,0.45);
  }

 .sway { animation: idleSway 4.5s ease-in-out infinite; }
  @keyframes idleSway {
    0%,100% { transform: rotate(-1.4deg); }
    50% { transform: rotate(1.4deg); }
  }
  .card-sway {
    animation: cardSway 4.5s ease-in-out infinite;
    transform-origin: top center;
  }
  @keyframes cardSway {
    0%,100% { transform: rotate(-0.6deg); }
    50% { transform: rotate(0.6deg); }
  }

  .rope-stretch .rope { animation: stretchPulse 0.5s cubic-bezier(0.34,1.56,0.64,1); }
  @keyframes stretchPulse {
    0% { transform: scaleY(1) scaleX(1); }
    35% { transform: scaleY(1.18) scaleX(0.7); }
    55% { transform: scaleY(0.92) scaleX(1.15); }
    75% { transform: scaleY(1.05) scaleX(0.92); }
    100% { transform: scaleY(1) scaleX(1); }
  }

  .wrap { width:100%; max-width:640px; position:relative; z-index:1; }

  .card {
    background:rgba(255,255,255,0.12);
    backdrop-filter:blur(24px);
    -webkit-backdrop-filter:blur(24px);
    border:1px solid rgba(255,255,255,0.35);
    border-radius:26px;
    padding:52px 44px;
    box-shadow:0 25px 70px rgba(80,20,120,0.35), inset 0 1px 0 rgba(255,255,255,0.4);
    animation: fadeInUp 0.8s cubic-bezier(0.22,1,0.36,1) both, glow 4s ease-in-out infinite;
    position:relative;
    overflow:hidden;
    min-height:260px;
  }
  @keyframes glow {
    0%,100% { box-shadow:0 25px 70px rgba(80,20,120,0.35), inset 0 1px 0 rgba(255,255,255,0.4), 0 0 0 rgba(255,255,255,0); }
    50% { box-shadow:0 25px 70px rgba(80,20,120,0.35), inset 0 1px 0 rgba(255,255,255,0.4), 0 0 50px rgba(255,255,255,0.15); }
  }
  @keyframes fadeInUp { from{opacity:0; transform:translateY(20px) scale(0.98);} to{opacity:1; transform:translateY(0) scale(1);} }

  .card.yank-up {
    animation: yankUp 0.22s cubic-bezier(0.7,0,0.9,0.2) forwards !important;
  }
  @keyframes yankUp {
    to { transform: translateY(-120vh); }
  }
  .card.drop-bounce {
    animation: dropBounce 0.5s cubic-bezier(0.34,1.6,0.64,1) forwards !important;
  }
  @keyframes dropBounce {
    from { transform: translateY(-120vh); }
    to { transform: translateY(0); }
  }

  .quote-mark { font-family:'Fraunces',serif; font-size:60px; color:#fff; line-height:0.4; margin-bottom:10px; opacity:0.85; text-shadow:0 0 30px rgba(255,255,255,0.6); }

  .quote-text {
    font-family:'Fraunces', serif; font-style:italic; font-weight:500;
    font-size:27px; line-height:1.45; color:#fff; margin-bottom:26px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.15);
  }
  .author { font-size:15px; font-weight:700; color:#fff9db; }
  .author::before { content:'— '; opacity:0.8; }

  .actions { display:flex; gap:10px; margin-top:34px; flex-wrap:wrap; }
  button {
    font-family:'Inter',sans-serif; font-weight:600; font-size:14px;
    padding:12px 20px; border-radius:13px; border:none; cursor:pointer;
    display:flex; align-items:center; gap:8px;
    transition:all 0.2s cubic-bezier(0.22,1,0.36,1);
    color:#fff;
  }
  button:hover { transform:translateY(-2px) scale(1.03); }
  button:active { transform:translateY(0) scale(0.97); }
  button:disabled { opacity:0.6; cursor:default; transform:none; }
  .primary { background:linear-gradient(135deg,#fbbf24,#f472b6); color:#3b1e0e; box-shadow:0 10px 25px rgba(251,191,36,0.5); }
  .primary:hover { box-shadow:0 14px 34px rgba(251,191,36,0.7); }
  .btn-copy { background:linear-gradient(135deg,#38bdf8,#6366f1); box-shadow:0 10px 25px rgba(56,189,248,0.45); }
  .btn-copy:hover { box-shadow:0 14px 34px rgba(56,189,248,0.65); }
  .btn-share { background:linear-gradient(135deg,#34d399,#059669); box-shadow:0 10px 25px rgba(52,211,153,0.45); }
  .btn-share:hover { box-shadow:0 14px 34px rgba(52,211,153,0.65); }

  .toast {
    position:fixed; bottom:28px; left:50%; transform:translateX(-50%) translateY(20px);
    background:rgba(30,20,50,0.9); border:1px solid rgba(255,255,255,0.25); color:#fff;
    padding:13px 22px; border-radius:13px; font-size:14px; font-weight:500;
    opacity:0; pointer-events:none; transition:all 0.3s cubic-bezier(0.22,1,0.36,1);
    box-shadow:0 12px 30px rgba(0,0,0,0.45);
  }
  .toast.show { opacity:1; transform:translateX(-50%) translateY(0); }

  @media (max-width:480px){
    .card{ padding:38px 26px; }
    .quote-text{ font-size:21px; }
    .orb1,.orb2,.orb3{ display:none; }
  }
</style>
</head>
<body>
  <div class="orb orb1"></div>
  <div class="orb orb2"></div>
  <div class="orb orb3"></div>
  <div id="particles"></div>

  <div class="rope-wrap" id="ropeWrap">
    <div class="rope-inner sway" id="ropeInner">
      <div class="rope" id="rope"></div>
      <div class="knot"></div>
    </div>
  </div>

  <div class="wrap">
    <div class="card card-sway" id="card">
      <div class="quote-mark">&ldquo;</div>
      <div class="quote-text" id="quoteText">{{ quote }}</div>
      <div class="author" id="quoteAuthor">{{ author }}</div>
      <div class="actions">
        <button class="primary" id="newBtn" onclick="newQuote()"><span id="newBtnLabel">✨ New quote</span></button>
        <button class="btn-copy" onclick="copyQuote()">📋 Copy</button>
        <button class="btn-share" onclick="shareQuote()">🔗 Share</button>
      </div>
    </div>
  </div>
  <div class="toast" id="toast"></div>

<script>
  const card = document.getElementById('card');
  const qText = document.getElementById('quoteText');
  const qAuthor = document.getElementById('quoteAuthor');
  const toast = document.getElementById('toast');
  const newBtn = document.getElementById('newBtn');
  const particlesContainer = document.getElementById('particles');
  const ropeWrap = document.getElementById('ropeWrap');
  const ropeInner = document.getElementById('ropeInner');
  const rope = document.getElementById('rope');

  function updateRope(){
    const cardRect = card.getBoundingClientRect();
    const cardCenterX = cardRect.left + cardRect.width / 2;
    const cardTopY = cardRect.top;

    ropeWrap.style.left = (cardCenterX - 7) + 'px';
    const length = Math.max(20, cardTopY - 4);
    rope.style.height = length + 'px';
    ropeWrap.style.visibility = cardTopY < 8 ? 'hidden' : 'visible';

    requestAnimationFrame(updateRope);
  }
  requestAnimationFrame(updateRope);

  function spawnParticle(startMidway){
    const p = document.createElement('div');
    p.className = 'particle';
    const size = 3 + Math.random() * 7;
    const duration = 10 + Math.random() * 10;
    p.style.width = size + 'px';
    p.style.height = size + 'px';
    p.style.left = Math.random() * 100 + 'vw';
    p.style.animationDuration = duration + 's';
    p.style.opacity = 0.4 + Math.random() * 0.5;
    if (startMidway) {
      p.style.animationDelay = '-' + (Math.random() * duration) + 's';
    }
    particlesContainer.appendChild(p);
    setTimeout(()=> p.remove(), 21000);
  }
  for(let i=0;i<60;i++){ spawnParticle(true); }
  setInterval(()=> spawnParticle(false), 300);

  function showToast(msg){
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(()=> toast.classList.remove('show'), 1800);
  }

  async function newQuote(){
    newBtn.disabled = true;
    ropeInner.classList.remove('sway');
    card.classList.remove('card-sway');
    card.classList.remove('drop-bounce');
    card.classList.add('yank-up');

    const startTime = Date.now();
    const MIN_HIDDEN_TIME = 220;

    let data = null;
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 4000);
      const res = await fetch('/quote', { signal: controller.signal });
      clearTimeout(timeoutId);
      data = await res.json();
    } catch(err){
      showToast('Could not fetch a new quote — try again');
    }

    const elapsed = Date.now() - startTime;
    const remaining = Math.max(0, MIN_HIDDEN_TIME - elapsed);

    setTimeout(() => {
      if (data) {
        qText.textContent = data.quote;
        qAuthor.textContent = data.author;
      }
      card.classList.remove('yank-up');
      void card.offsetWidth;
      card.classList.add('drop-bounce');

      setTimeout(() => {
        ropeInner.classList.add('rope-stretch');
        setTimeout(() => {
          ropeInner.classList.remove('rope-stretch');
          ropeInner.classList.add('sway');
          card.classList.add('card-sway');
        }, 500);
      }, 480);

      newBtn.disabled = false;
    }, remaining);
  }

  function copyQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    navigator.clipboard.writeText(text).then(()=> showToast('Copied to clipboard ✅'));
  }

  function shareQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    if (navigator.share) { navigator.share({ text, title: 'Daily Spark' }).catch(()=>{}); }
    else { navigator.clipboard.writeText(text).then(()=> showToast('Copied — share it anywhere ✅')); }
  }
</script>
</body>
</html>
"""

@app.route("/")
def home():
    q = get_quote_of_the_day()
    return render_template_string(HTML_PAGE, quote=q["quote"], author=q["author"])

@app.route("/quote")
def random_quote():
    return jsonify(get_random_quote())

@app.route("/quote/today")
def quote_of_the_day():
    return jsonify(get_quote_of_the_day())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)