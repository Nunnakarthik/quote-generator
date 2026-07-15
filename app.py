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
    background: linear-gradient(-45deg, #1a1338, #2d1b4e, #1a2a4e, #16142a);
    background-size: 400% 400%;
    animation: gradientShift 16s ease infinite;
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
    position:fixed; border-radius:50%; filter:blur(60px); opacity:0.45; pointer-events:none;
  }
  .orb1 { width:340px; height:340px; background:#8b5cf6; top:-80px; left:-80px; animation:float1 12s ease-in-out infinite; }
  .orb2 { width:280px; height:280px; background:#4f46e5; bottom:-60px; right:-60px; animation:float2 14s ease-in-out infinite; }
  .orb3 { width:200px; height:200px; background:#ec4899; top:60%; left:75%; animation:float3 10s ease-in-out infinite; opacity:0.3; }
  @keyframes float1 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(40px,60px);} }
  @keyframes float2 { 0%,100%{transform:translate(0,0);} 50%{transform:translate(-50px,-30px);} }
  @keyframes float3 { 0%,100%{transform:translate(0,0) scale(1);} 50%{transform:translate(-30px,40px) scale(1.15);} }

  .wrap { width:100%; max-width:640px; position:relative; z-index:1; perspective:1200px; }
  .badge {
    display:inline-flex; align-items:center; gap:8px;
    background:rgba(255,255,255,0.06);
    border:1px solid rgba(255,255,255,0.12);
    padding:7px 16px; border-radius:999px;
    font-size:12px; font-weight:600; letter-spacing:1.5px;
    text-transform:uppercase; color:#c4b5fd;
    margin-bottom:22px;
    animation: fadeInDown 0.7s ease both;
  }
  .dot { width:6px; height:6px; border-radius:50%; background:#a78bfa; box-shadow:0 0 10px 2px #a78bfa; animation: pulse 2s ease-in-out infinite; }
  @keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.3;} }
  @keyframes fadeInDown { from{opacity:0; transform:translateY(-12px);} to{opacity:1; transform:translateY(0);} }
  @keyframes fadeInUp { from{opacity:0; transform:translateY(20px) scale(0.98);} to{opacity:1; transform:translateY(0) scale(1);} }

  .card {
    background:rgba(255,255,255,0.055);
    backdrop-filter:blur(24px);
    -webkit-backdrop-filter:blur(24px);
    border:1px solid rgba(255,255,255,0.12);
    border-radius:26px;
    padding:52px 44px;
    box-shadow:0 25px 70px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.08);
    transition:transform 0.15s ease-out, opacity 0.3s ease, box-shadow 0.3s ease;
    transform-style:preserve-3d;
    animation: fadeInUp 0.8s cubic-bezier(0.22,1,0.36,1) both;
    position:relative;
    overflow:hidden;
  }
  .card::before {
    content:'';
    position:absolute; inset:0;
    background:linear-gradient(135deg, rgba(139,92,246,0.15), transparent 60%);
    pointer-events:none;
  }
  .card:hover { box-shadow:0 30px 90px rgba(139,92,246,0.25), inset 0 1px 0 rgba(255,255,255,0.1); }
  .card.fade { opacity:0; transform:translateY(10px) scale(0.97) !important; }

  .quote-mark { font-family:'Fraunces',serif; font-size:60px; color:#a78bfa; line-height:0.4; margin-bottom:10px; opacity:0.7; text-shadow:0 0 30px rgba(167,139,250,0.5); }
  .quote-text {
    font-family:'Fraunces', serif; font-style:italic; font-weight:500;
    font-size:27px; line-height:1.45; color:#f5f3ff; margin-bottom:26px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
  }
  .author {
    font-size:15px; font-weight:600;
    background:linear-gradient(90deg, #c4b5fd, #f0abfc);
    -webkit-background-clip:text; background-clip:text; color:transparent;
  }
  .author::before { content:'— '; color:#c4b5fd; -webkit-text-fill-color:#c4b5fd; }

  .actions { display:flex; gap:10px; margin-top:34px; flex-wrap:wrap; position:relative; z-index:2; }
  button {
    font-family:'Inter',sans-serif; font-weight:600; font-size:14px;
    padding:12px 20px; border-radius:13px; border:1px solid rgba(255,255,255,0.14);
    background:rgba(255,255,255,0.07); color:#e9e5ff; cursor:pointer;
    display:flex; align-items:center; gap:8px;
    transition:all 0.2s cubic-bezier(0.22,1,0.36,1);
  }
  button:hover { background:rgba(255,255,255,0.14); transform:translateY(-2px); border-color:rgba(255,255,255,0.3); }
  button:active { transform:translateY(0) scale(0.97); }
  .primary {
    background:linear-gradient(135deg,#8b5cf6,#6d28d9); border:none;
    box-shadow:0 10px 25px rgba(139,92,246,0.4);
    position:relative; overflow:hidden;
  }
  .primary:hover { box-shadow:0 14px 34px rgba(139,92,246,0.55); }
  .footer-note { text-align:center; margin-top:26px; font-size:13px; color:rgba(255,255,255,0.35); animation: fadeInDown 1s ease both; }

  .sparkle {
    position:absolute; pointer-events:none; font-size:16px;
    animation: sparkleFly 0.9s ease-out forwards;
  }
  @keyframes sparkleFly {
    0% { opacity:1; transform:translate(0,0) scale(0.5) rotate(0deg); }
    100% { opacity:0; transform:translate(var(--dx), var(--dy)) scale(1.3) rotate(180deg); }
  }

  .toast {
    position:fixed; bottom:28px; left:50%; transform:translateX(-50%) translateY(20px);
    background:#1e1b3a; border:1px solid rgba(255,255,255,0.15); color:#e9e5ff;
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

  <div class="wrap">
    <div class="badge"><span class="dot"></span>Quote of the Day</div>
    <div class="card" id="card">
      <div class="quote-mark">&ldquo;</div>
      <div class="quote-text" id="quoteText">{{ quote }}</div>
      <div class="author" id="quoteAuthor">{{ author }}</div>
      <div class="actions">
        <button class="primary" id="newBtn" onclick="newQuote(event)">✨ New quote</button>
        <button onclick="copyQuote()">📋 Copy</button>
        <button onclick="shareQuote()">🔗 Share</button>
      </div>
    </div>
    <div class="footer-note">Powered by ZenQuotes • A new quote every day</div>
  </div>
  <div class="toast" id="toast"></div>

<script>
  const card = document.getElementById('card');
  const qText = document.getElementById('quoteText');
  const qAuthor = document.getElementById('quoteAuthor');
  const toast = document.getElementById('toast');
  const newBtn = document.getElementById('newBtn');

  // 3D tilt effect following the mouse
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    const rotateX = ((y - centerY) / centerY) * -6;
    const rotateY = ((x - centerX) / centerX) * 6;
    card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.01)`;
  });
  card.addEventListener('mouseleave', () => {
    card.style.transform = 'rotateX(0) rotateY(0) scale(1)';
  });

  function showToast(msg){
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(()=> toast.classList.remove('show'), 1800);
  }

  function burstSparkles(originEl){
    const rect = originEl.getBoundingClientRect();
    const emojis = ['✨','⭐','💫'];
    for(let i=0;i<8;i++){
      const s = document.createElement('div');
      s.className = 'sparkle';
      s.textContent = emojis[Math.floor(Math.random()*emojis.length)];
      s.style.left = (rect.left + rect.width/2) + 'px';
      s.style.top = (rect.top + rect.height/2) + 'px';
      const angle = Math.random() * Math.PI * 2;
      const dist = 60 + Math.random()*60;
      s.style.setProperty('--dx', Math.cos(angle)*dist + 'px');
      s.style.setProperty('--dy', Math.sin(angle)*dist + 'px');
      document.body.appendChild(s);
      setTimeout(()=> s.remove(), 900);
    }
  }

  async function newQuote(e){
    burstSparkles(newBtn);
    card.classList.add('fade');
    try {
      const res = await fetch('/quote');
      const data = await res.json();
      setTimeout(()=>{
        qText.textContent = data.quote;
        qAuthor.textContent = data.author;
        card.classList.remove('fade');
      }, 220);
    } catch(err){
      card.classList.remove('fade');
      showToast('Could not fetch a new quote');
    }
  }

  function copyQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    navigator.clipboard.writeText(text).then(()=> showToast('Copied to clipboard ✅'));
  }

  function shareQuote(){
    const text = `"${qText.textContent}" — ${qAuthor.textContent}`;
    if (navigator.share) {
      navigator.share({ text, title: 'Daily Spark' }).catch(()=>{});
    } else {
      navigator.clipboard.writeText(text).then(()=> showToast('Copied — share it anywhere ✅'));
    }
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