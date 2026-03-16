import streamlit as st


st.set_page_config(
    page_title="SENTINEL — Model",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 20px 40px !important; max-width: 100% !important; }

body, .stApp {
    background: #000408;
    color: #00f5ff;
    font-family: 'Share Tech Mono', monospace;
}

.stApp {
    background:
        linear-gradient(rgba(0,245,255,0.02) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.02) 1px, transparent 1px),
        #000408;
    background-size: 40px 40px;
}

.page-title {
    font-family: 'Orbitron', monospace;
    font-size: 32px;
    font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 30px rgba(0,245,255,0.5);
    letter-spacing: 0.1em;
    margin-bottom: 8px;
}

.page-subtitle {
    font-size: 13px;
    color: rgba(0,245,255,0.5);
    letter-spacing: 0.1em;
    margin-bottom: 28px;
}

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    letter-spacing: 0.2em;
    color: rgba(0,245,255,0.8);
    margin: 30px 0 14px;
    text-transform: uppercase;
    border-left: 3px solid #00f5ff;
    padding-left: 12px;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
    margin: 28px 0;
}

.card {
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 22px;
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
    margin-bottom: 16px;
}

.card-title {
    font-family: 'Orbitron', monospace;
    font-size: 12px;
    color: #00f5ff;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.card-body {
    font-family: 'Exo 2', sans-serif;
    font-size: 14px;
    color: rgba(200,230,255,0.76);
    line-height: 1.8;
}

.card-body strong { color: #00f5ff; }

.pipeline {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
}

.step {
    background: rgba(0,10,20,0.88);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 16px 12px;
    text-align: center;
}

.step-num {
    font-family: 'Orbitron', monospace;
    font-size: 20px;
    color: #00f5ff;
}

.step-label {
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: rgba(0,245,255,0.58);
    margin-top: 6px;
}

.fit-grid {
    display: grid;
    grid-template-columns: 1.8fr 1fr;
    gap: 10px;
}

.ok { color: #00ff88; }
.warn { color: #ffaa00; }
.risk { color: #ff3366; }

.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(0,245,255,0.5) !important;
    color: #00f5ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.2em !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    background: rgba(0,245,255,0.1) !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.3) !important;
}

.back-btn .stButton > button {
    padding: 8px 20px !important;
    border-color: rgba(0,245,255,0.3) !important;
    color: rgba(0,245,255,0.6) !important;
}
</style>
""", unsafe_allow_html=True)


# nav
nav1, nav2, nav3, nav4, nav5 = st.columns([2, 1, 1, 1, 2])
with nav1:
    st.markdown('<div style="font-family:\'Orbitron\', monospace; font-size:20px; font-weight:900; color:#00f5ff; text-shadow:0 0 20px rgba(0,245,255,0.6); letter-spacing:0.2em; padding-top:5px;">⬡ SENTINEL</div>', unsafe_allow_html=True)
with nav2:
    if st.button("⬡ DETECT", use_container_width=True, key="model_nav_detect"):
        st.switch_page("pages/1_detect.py")
with nav3:
    if st.button("⬡ ANALYTICS", use_container_width=True, key="model_nav_analytics"):
        st.switch_page("pages/2_analytics.py")
with nav4:
    if st.button("⬡ MODEL INFO", use_container_width=True, key="model_nav_model"):
        st.switch_page("pages/3_model.py")
with nav5:
    st.markdown('<div style="font-size:11px; color:rgba(0,245,255,0.3); letter-spacing:0.1em; text-align:right; padding-top:12px;">SYS:ONLINE // v3.7</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider" style="margin-top: 10px;"></div>', unsafe_allow_html=True)

col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← BACK", key="model_back"):
        st.switch_page("pages/1_detect.py")
    st.markdown('</div>', unsafe_allow_html=True)


st.markdown("""
<div class="page-title">▸ MODEL INTELLIGENCE BRIEF</div>
<div class="page-subtitle">// Current implementation: statistical + ML ensemble IDS layer and analyst interpretation guide</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ Problem Statement Fit</div>', unsafe_allow_html=True)
st.markdown("""
<div class="fit-grid">
  <div class="card">
    <div class="card-title">What Problem Is Solved Right Now</div>
    <div class="card-body">
      <strong>Implemented:</strong> Batch anomaly detection on uploaded network traffic with explainable risk scoring and analyst-facing visual inspection.<br><br>
      <strong>Why this helps:</strong> It detects behavior that deviates from normal traffic without requiring labeled attack classes, which addresses zero-day detection challenges better than static rules alone.<br><br>
      <strong>Primary users supported:</strong> network security analysts and IT admins reviewing suspicious flows in dashboard views.
    </div>
  </div>
  <div class="card">
    <div class="card-title">Current Scope Notes</div>
    <div class="card-body">
      <span class="ok">Implemented:</span> anomaly scoring, ranking, PCA mapping, cluster/risk analysis.<br>
      <span class="warn">Partially implemented:</span> actionable alerting (dashboard-level triage).<br>
      <span class="risk">Not yet implemented:</span> live stream ingestion and production SIEM push in this app build.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ Implemented ML Process</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pipeline">
  <div class="step"><div class="step-num">01</div><div class="step-label">Numeric Extraction</div></div>
  <div class="step"><div class="step-num">02</div><div class="step-label">Statistical Signals</div></div>
  <div class="step"><div class="step-num">03</div><div class="step-label">Isolation Forest</div></div>
  <div class="step"><div class="step-num">04</div><div class="step-label">PCA Projection</div></div>
  <div class="step"><div class="step-num">05</div><div class="step-label">K-Means Clustering</div></div>
  <div class="step"><div class="step-num">06</div><div class="step-label">DBSCAN Rarity</div></div>
  <div class="step"><div class="step-num">07</div><div class="step-label">Distance Deviation</div></div>
  <div class="step"><div class="step-num">08</div><div class="step-label">Ensemble ML Risk</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div class="card-title">Signal Combination Logic</div>
  <div class="card-body">
    Final ML risk is built from four normalized sources:<br>
    1) statistical risk baseline<br>
    2) Isolation Forest anomaly severity<br>
    3) cluster rarity score (K-Means/DBSCAN)<br>
    4) distance deviation score (Euclidean + Mahalanobis)<br><br>
    The output is a 0-100 scale so analysts can triage consistently.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ How To Read Current Graphs</div>', unsafe_allow_html=True)

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.markdown("""
    <div class="card">
      <div class="card-title">Detect Page Graphs</div>
      <div class="card-body">
        <strong>Threat gauge (% anomalous):</strong> fast health snapshot of the scanned batch.<br><br>
        <strong>Anomaly score distribution:</strong> separation between low-risk and high-risk flows; stronger split usually means clearer anomaly boundary.<br><br>
        <strong>Traffic breakdown pie:</strong> volume ratio of flagged vs normal flows for immediate incident scale estimation.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">Flagged Traffic Table</div>
      <div class="card-body">
        Sorted by descending risk so analysts start with highest-severity flows first.<br>
        Typical workflow: inspect top rows, compare ports/packet stats, export incidents for follow-up.
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_g2:
    st.markdown("""
    <div class="card">
      <div class="card-title">Analytics Page Graphs</div>
      <div class="card-body">
        <strong>PCA behavior map:</strong> clustered center means common behavior; isolated points suggest unusual patterns.<br><br>
        <strong>Statistical vs ML scatter:</strong> points near diagonal show layer agreement; off-diagonal points are disagreement candidates worth investigation.<br><br>
        <strong>Cluster analysis bars:</strong> large low-risk clusters indicate normal baselines; small high-risk clusters indicate rare behavior pockets.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <div class="card-title">Timeline and Correlation Views</div>
      <div class="card-body">
        <strong>Timeline:</strong> shows bursts of anomalous intensity over record order.<br>
        <strong>Feature correlation with risk:</strong> highlights which features are most associated with risk escalation in the current batch.
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ Theory Behind The Implementation</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div class="card-title">Why This Hybrid Approach Works</div>
  <div class="card-body">
    <strong>Statistical layer</strong> (Z-score + IQR) gives transparent, auditable baseline anomaly evidence.<br>
    <strong>Isolation Forest</strong> finds non-linear isolation behavior without labels.<br>
    <strong>Clustering + distance</strong> adds context: rarity and geometric deviation from typical traffic states.<br><br>
    Combining these reduces dependence on any single detector and supports more stable triage decisions.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
  <div class="card-title">Interpretation Theory For Analysts</div>
  <div class="card-body">
    <strong>Agreement between statistical and ML layers:</strong> higher confidence anomaly candidate.<br>
    <strong>Disagreement:</strong> investigate as edge-case behavior (potential novel attack or threshold issue).<br>
    <strong>Rare cluster + high distance + high IF score:</strong> strongest suspicious pattern profile in this system.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ Bottom Line</div>', unsafe_allow_html=True)
st.markdown("""
<div class="card">
  <div class="card-body">
    This page reflects the currently implemented SENTINEL state: an explainable, unsupervised anomaly workflow with analyst-first visualization and triage support.
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col_n1, col_n2, _ = st.columns([1, 1, 2])
with col_n1:
    if st.button("← BACK TO DETECT", use_container_width=True, key="model_footer_back_detect"):
        st.switch_page("pages/1_detect.py")
with col_n2:
    if st.button("VIEW ANALYTICS", use_container_width=True, key="model_footer_view_analytics"):
        st.switch_page("pages/2_analytics.py")
