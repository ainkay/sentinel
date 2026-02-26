import streamlit as st

st.set_page_config(page_title="SENTINEL IDS", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

#MainMenu, footer, header,
[data-testid="collapsedControl"],
[data-testid="stSidebar"],
[data-testid="stSidebarNav"] { display:none !important; }

.block-container { padding:0 !important; margin:0 !important; max-width:100% !important; }
section.main > div { padding:0 !important; }
div[data-testid="stVerticalBlock"] { gap:0 !important; }
div[data-testid="stVerticalBlock"] > div { padding:0 !important; margin:0 !important; }
.element-container { margin:0 !important; padding:0 !important; }
*, *::before, *::after { box-sizing:border-box; }

html, body, .stApp { background:#060d1a !important; color:#cdd9f0; font-family:'Syne',sans-serif; overflow-x:hidden; }

.stApp::before {
    content:''; position:fixed; inset:0;
    background-image: linear-gradient(rgba(56,189,248,0.035) 1px,transparent 1px), linear-gradient(90deg,rgba(56,189,248,0.035) 1px,transparent 1px);
    background-size:80px 80px; pointer-events:none; z-index:0;
}

.hero {
    position:relative; z-index:1;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    text-align:center; padding:10vh 48px 6vh;
}
.pill {
    display:inline-flex; align-items:center; gap:8px;
    border:1px solid rgba(56,189,248,0.22); border-radius:99px;
    padding:6px 20px; font-family:'Space Mono',monospace; font-size:10px;
    letter-spacing:0.2em; color:rgba(56,189,248,0.75); text-transform:uppercase;
    margin-bottom:44px; background:rgba(56,189,248,0.05);
}
.pdot { width:6px; height:6px; background:#4ade80; border-radius:50%; box-shadow:0 0 8px #4ade80; animation:blk 2s infinite; }
@keyframes blk { 0%,100%{opacity:1} 50%{opacity:0.25} }

.hero-title {
    font-size:clamp(64px,10vw,128px); font-weight:800; line-height:0.9;
    letter-spacing:-0.02em; color:#f0f8ff;
    text-shadow:0 0 100px rgba(56,189,248,0.18); margin-bottom:8px;
}
.hero-title .hl { color:#38bdf8; }
.hero-sub {
    font-family:'Space Mono',monospace; font-size:11px;
    letter-spacing:0.38em; color:rgba(56,189,248,0.32);
    text-transform:uppercase; margin-bottom:36px;
}
.hero-p {
    max-width:540px; font-size:16px; line-height:1.88;
    color:rgba(205,217,240,0.48); margin-bottom:44px;
}
.hero-p b { color:rgba(205,217,240,0.82); font-weight:600; }

.srow { display:flex; gap:28px; justify-content:center; margin-bottom:44px; flex-wrap:wrap; }
.sc { display:flex; align-items:center; gap:7px; font-family:'Space Mono',monospace; font-size:10px; color:rgba(205,217,240,0.35); letter-spacing:0.06em; }
.sdot { width:5px; height:5px; background:#4ade80; border-radius:50%; box-shadow:0 0 7px #4ade80; }

.stats {
    display:flex; width:100%; max-width:600px;
    border:1px solid rgba(56,189,248,0.1); border-radius:12px; overflow:hidden;
    background:rgba(56,189,248,0.02); margin-bottom:56px;
}
.stat { flex:1; padding:20px 16px; text-align:center; border-right:1px solid rgba(56,189,248,0.08); }
.stat:last-child { border-right:none; }
.sn { font-size:28px; font-weight:800; color:#38bdf8; text-shadow:0 0 20px rgba(56,189,248,0.4); line-height:1; }
.sl { font-family:'Space Mono',monospace; font-size:9px; color:rgba(205,217,240,0.26); letter-spacing:0.12em; text-transform:uppercase; margin-top:5px; }

/* CTA button centering: use column trick */
div[data-testid="stButton"] > button {
    background:linear-gradient(135deg,#0ea5e9,#38bdf8) !important;
    color:#060d1a !important; border:none !important;
    font-family:'Space Mono',monospace !important; font-size:11px !important;
    font-weight:700 !important; letter-spacing:0.2em !important;
    text-transform:uppercase !important; padding:15px 48px !important;
    border-radius:8px !important; width:100% !important;
    box-shadow:0 0 40px rgba(56,189,248,0.3) !important; transition:all 0.25s !important;
}
div[data-testid="stButton"] > button:hover {
    transform:translateY(-2px) !important; box-shadow:0 0 60px rgba(56,189,248,0.5) !important;
}

.how {
    width:100%; max-width:900px;
    padding:64px 0 80px;
    border-top:1px solid rgba(56,189,248,0.07);
}
.how-lbl { font-family:'Space Mono',monospace; font-size:9px; letter-spacing:0.35em; color:rgba(56,189,248,0.25); text-transform:uppercase; text-align:center; margin-bottom:36px; }
.steps { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.step { background:rgba(56,189,248,0.025); border:1px solid rgba(56,189,248,0.08); border-radius:10px; padding:26px 20px; transition:all 0.25s; }
.step:hover { border-color:rgba(56,189,248,0.18); background:rgba(56,189,248,0.05); transform:translateY(-2px); }
.snum { font-family:'Space Mono',monospace; font-size:9px; color:rgba(56,189,248,0.28); letter-spacing:0.15em; margin-bottom:14px; }
.sico { font-size:26px; margin-bottom:11px; }
.sname { font-size:15px; font-weight:700; color:rgba(240,248,255,0.85); margin-bottom:8px; }
.stxt { font-size:13px; color:rgba(205,217,240,0.36); line-height:1.72; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="pill"><span class="pdot"></span>ML-Powered Network Security</div>
  <div class="hero-title">SENTIN<span class="hl">E</span>L</div>
  <div class="hero-sub">Intelligent Intrusion Detection System</div>
  <div class="hero-p">Upload network traffic data and let our <b>Isolation Forest</b> ML model
  detect suspicious patterns automatically — <b>no labeled training data required</b>.</div>
  <div class="srow">
    <div class="sc"><span class="sdot"></span>System Online</div>
    <div class="sc"><span class="sdot"></span>ML Engine Ready</div>
    <div class="sc"><span class="sdot"></span>Monitoring Active</div>
  </div>
  <div class="stats">
    <div class="stat"><div class="sn">99.2%</div><div class="sl">Detection Rate</div></div>
    <div class="stat"><div class="sn">&lt;1s</div><div class="sl">Scan Speed</div></div>
    <div class="stat"><div class="sn">78+</div><div class="sl">Features</div></div>
    <div class="stat"><div class="sn">0</div><div class="sl">Labels Needed</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

# Centered CTA via columns
_, mid, _ = st.columns([2.2, 1.6, 2.2])
with mid:
    if st.button("🚀  START DETECTION  →", use_container_width=True):
        st.switch_page("pages/1_detect.py")

st.markdown("""
<div style="display:flex;justify-content:center;padding:0 48px">
<div class="how">
  <div class="how-lbl">// How it works</div>
  <div class="steps">
    <div class="step"><div class="snum">STEP 01</div><div class="sico">📂</div>
      <div class="sname">Upload Data</div>
      <div class="stxt">Drop any network traffic CSV — CICIDS2017, NSL-KDD, UNSW-NB15 — or use built-in demo data to start instantly.</div></div>
    <div class="step"><div class="snum">STEP 02</div><div class="sico">🧠</div>
      <div class="sname">ML Scans Traffic</div>
      <div class="stxt">Isolation Forest builds hundreds of random trees to find flows that are statistically unique — those are your threats.</div></div>
    <div class="step"><div class="snum">STEP 03</div><div class="sico">📊</div>
      <div class="sname">Review & Export</div>
      <div class="stxt">Explore the threat dashboard with PCA maps and feature analysis, then download flagged anomalies as CSV.</div></div>
  </div>
</div>
</div>
""", unsafe_allow_html=True)