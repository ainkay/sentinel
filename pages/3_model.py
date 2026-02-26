import streamlit as st
import numpy as np
import plotly.graph_objects as go

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

.page-title { font-family: 'Orbitron', monospace; font-size: 32px; font-weight: 700; color: #00f5ff; text-shadow: 0 0 30px rgba(0,245,255,0.5); letter-spacing: 0.1em; margin-bottom: 8px; }
.page-subtitle { font-size: 13px; color: rgba(0,245,255,0.5); letter-spacing: 0.1em; margin-bottom: 40px; }

.section-header { font-family: 'Orbitron', monospace; font-size: 14px; letter-spacing: 0.2em; color: rgba(0,245,255,0.8); margin: 30px 0 16px; text-transform: uppercase; border-left: 3px solid #00f5ff; padding-left: 12px; }
.section-divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent); margin: 30px 0; }

/* TECH CARD */
.tech-card {
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 28px;
    clip-path: polygon(0 0,calc(100% - 16px) 0,100% 16px,100% 100%,16px 100%,0 calc(100% - 16px));
    margin-bottom: 20px;
    transition: all 0.3s ease;
}
.tech-card:hover { border-color: rgba(0,245,255,0.5); box-shadow: 0 0 20px rgba(0,245,255,0.07); }

.tech-card-title { font-family: 'Orbitron', monospace; font-size: 13px; color: #00f5ff; letter-spacing: 0.15em; margin-bottom: 14px; text-transform: uppercase; }
.tech-card-body { font-family: 'Exo 2', sans-serif; font-size: 14px; color: rgba(200,230,255,0.7); line-height: 1.8; }
.tech-card-body strong { color: #00f5ff; }

/* PIPELINE STEPS */
.pipeline { display: flex; align-items: stretch; gap: 0; margin: 20px 0; flex-wrap: wrap; }
.pipeline-step {
    flex: 1; min-width: 140px;
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 20px 16px;
    text-align: center;
    position: relative;
    transition: all 0.3s ease;
}
.pipeline-step:not(:last-child)::after {
    content: '→';
    position: absolute; right: -14px; top: 50%;
    transform: translateY(-50%);
    color: rgba(0,245,255,0.5);
    font-size: 18px; z-index: 2;
}
.pipeline-step:hover { border-color: rgba(0,245,255,0.6); background: rgba(0,245,255,0.05); }
.pipeline-num { font-family: 'Orbitron', monospace; font-size: 22px; color: #00f5ff; text-shadow: 0 0 15px rgba(0,245,255,0.5); }
.pipeline-label { font-size: 10px; color: rgba(0,245,255,0.5); letter-spacing: 0.1em; margin-top: 8px; text-transform: uppercase; }

/* SPEC TABLE */
.spec-table { width: 100%; border-collapse: collapse; }
.spec-table tr { border-bottom: 1px solid rgba(0,245,255,0.08); }
.spec-table tr:hover { background: rgba(0,245,255,0.03); }
.spec-table td { padding: 12px 16px; font-size: 13px; }
.spec-table td:first-child { color: rgba(0,245,255,0.5); letter-spacing: 0.1em; font-size: 11px; text-transform: uppercase; width: 35%; }
.spec-table td:last-child { color: rgba(200,230,255,0.8); font-family: 'Exo 2', sans-serif; }

/* COMPARISON TABLE */
.compare-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1px; background: rgba(0,245,255,0.1); margin: 20px 0; }
.compare-cell { background: rgba(0,10,20,0.9); padding: 16px; text-align: center; font-size: 12px; }
.compare-cell.header { font-family: 'Orbitron', monospace; font-size: 11px; letter-spacing: 0.15em; color: rgba(0,245,255,0.6); background: rgba(0,20,40,0.8); }
.compare-cell.good { color: #00ff88; }
.compare-cell.bad { color: #ff3366; }
.compare-cell.mid { color: #ffaa00; }

.stButton > button {
    background: transparent !important; border: 1px solid rgba(0,245,255,0.5) !important;
    color: #00f5ff !important; font-family: 'Orbitron', monospace !important;
    font-size: 11px !important; letter-spacing: 0.2em !important; padding: 10px 20px !important;
    transition: all 0.3s ease !important; text-transform: uppercase !important;
}
.stButton > button:hover { background: rgba(0,245,255,0.1) !important; box-shadow: 0 0 15px rgba(0,245,255,0.3) !important; }
.back-btn .stButton > button { padding: 8px 20px !important; border-color: rgba(0,245,255,0.3) !important; color: rgba(0,245,255,0.6) !important; }

/* FORMULA BOX */
.formula-box {
    background: rgba(0,245,255,0.04);
    border: 1px solid rgba(0,245,255,0.2);
    border-left: 3px solid #00f5ff;
    padding: 16px 20px;
    margin: 16px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    color: rgba(0,245,255,0.85);
}
</style>
""", unsafe_allow_html=True)

# ─── RESPONSIVE NAV ───────────────────────────────────────────────────────────
nav1, nav2, nav3, nav4, nav5 = st.columns([2, 1, 1, 1, 2])
with nav1:
    st.markdown('<div style="font-family:\'Orbitron\', monospace; font-size:20px; font-weight:900; color:#00f5ff; text-shadow:0 0 20px rgba(0,245,255,0.6); letter-spacing:0.2em; padding-top:5px;">⬡ SENTINEL</div>', unsafe_allow_html=True)
with nav2:
    if st.button("⬡ DETECT", use_container_width=True): st.switch_page("pages/1_detect.py")
with nav3:
    if st.button("⬡ ANALYTICS", use_container_width=True): st.switch_page("pages/2_analytics.py")
with nav4:
    if st.button("⬡ MODEL INFO", use_container_width=True): st.switch_page("pages/3_model.py")
with nav5:
    st.markdown('<div style="font-size:11px; color:rgba(0,245,255,0.3); letter-spacing:0.1em; text-align:right; padding-top:12px;">SYS:ONLINE // v3.7</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider" style="margin-top: 10px;"></div>', unsafe_allow_html=True)

col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← BACK"):
        st.switch_page("pages/1_detect.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="page-title">▸ MODEL INTELLIGENCE BRIEF</div>
<div class="page-subtitle">// Isolation Forest — unsupervised anomaly detection for network intrusion</div>
""", unsafe_allow_html=True)

# ─── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ HOW ISOLATION FOREST WORKS</div>', unsafe_allow_html=True)

col_l, col_r = st.columns([3, 2])
with col_l:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Core Algorithm</div>
        <div class="tech-card-body">
            Isolation Forest detects anomalies by exploiting a fundamental property of outliers:
            they are <strong>few</strong> and <strong>different</strong>.<br><br>
            The algorithm builds an ensemble of random binary trees called <strong>Isolation Trees (iTrees)</strong>.
            For each tree, the algorithm randomly selects a feature and a split value between the
            feature's min and max. This process repeats recursively until each point is isolated.<br><br>
            <strong>Key insight:</strong> Anomalies require fewer splits to isolate (shorter path lengths),
            while normal points are deep in the tree (longer paths). The anomaly score is derived from the
            average path length across all trees.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        score(x, n) = 2^(−E[h(x)] / c(n))<br><br>
        h(x) = path length of point x<br>
        E[h(x)] = mean path length over forest<br>
        c(n) = average path length for sample size n<br><br>
        score → 1.0 : highly anomalous<br>
        score → 0.5 : indeterminate<br>
        score → 0.0 : normal behavior
    </div>
    """, unsafe_allow_html=True)

with col_r:
    np.random.seed(42)
    depths_normal = np.random.normal(12, 2, 200)
    depths_anom = np.random.normal(4, 1.5, 30)

    fig_depth = go.Figure()
    fig_depth.add_trace(go.Histogram(
        x=depths_normal, name='Normal Points',
        marker_color='rgba(0,255,136,0.7)', nbinsx=20, opacity=0.8
    ))
    fig_depth.add_trace(go.Histogram(
        x=depths_anom, name='Anomalous Points',
        marker_color='rgba(255,51,102,0.8)', nbinsx=15, opacity=0.8
    ))
    fig_depth.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=10),
        legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)'),
        xaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Isolation Tree Depth'),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Count'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        title=dict(text='Path Length Distribution', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_depth, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── PROCESSING PIPELINE ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ DETECTION PIPELINE</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pipeline">
    <div class="pipeline-step">
        <div class="pipeline-num">01</div>
        <div class="pipeline-label">Data Ingestion</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">02</div>
        <div class="pipeline-label">Feature Extraction</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">03</div>
        <div class="pipeline-label">Standardization</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">04</div>
        <div class="pipeline-label">iTree Building</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">05</div>
        <div class="pipeline-label">Scoring</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">06</div>
        <div class="pipeline-label">Alert Generation</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── TECHNICAL SPECS ──────────────────────────────────────────────────────────
col_specs, col_compare = st.columns([1, 1])

with col_specs:
    st.markdown('<div class="section-header">▸ MODEL SPECIFICATIONS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-card">
        <table class="spec-table">
            <tr><td>Algorithm</td><td>Isolation Forest (Liu et al., 2008)</td></tr>
            <tr><td>Learning Type</td><td>Unsupervised / Semi-supervised</td></tr>
            <tr><td>Default Trees</td><td>200 estimators</td></tr>
            <tr><td>Contamination</td><td>5% (tunable 1%–30%)</td></tr>
            <tr><td>Feature Scaling</td><td>StandardScaler (z-score normalization)</td></tr>
            <tr><td>Missing Values</td><td>Median imputation</td></tr>
            <tr><td>Inf/NaN Handling</td><td>Replace → drop columns</td></tr>
            <tr><td>Classification</td><td>Binary: Normal / Anomalous</td></tr>
            <tr><td>Time Complexity</td><td>O(n × t × ψ)</td></tr>
            <tr><td>Space Complexity</td><td>O(t × ψ)</td></tr>
            <tr><td>Compatible Datasets</td><td>CICIDS2017, NSL-KDD, UNSW-NB15</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

with col_compare:
    st.markdown('<div class="section-header">▸ IDS APPROACH COMPARISON</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="compare-grid">
        <div class="compare-cell header">ATTRIBUTE</div>
        <div class="compare-cell header">RULE-BASED IDS</div>
        <div class="compare-cell header">SENTINEL ML</div>

        <div class="compare-cell">Novel attacks</div>
        <div class="compare-cell bad">✗ Missed</div>
        <div class="compare-cell good">✓ Detected</div>

        <div class="compare-cell">False positives</div>
        <div class="compare-cell bad">High</div>
        <div class="compare-cell good">Reduced</div>

        <div class="compare-cell">No labeled data</div>
        <div class="compare-cell bad">✗ Required</div>
        <div class="compare-cell good">✓ Not needed</div>

        <div class="compare-cell">Maintenance</div>
        <div class="compare-cell bad">Manual rules</div>
        <div class="compare-cell good">Auto-learns</div>

        <div class="compare-cell">Attack types</div>
        <div class="compare-cell bad">✗ No</div>
        <div class="compare-cell mid">In progress</div>

        <div class="compare-cell">Speed</div>
        <div class="compare-cell good">Fast</div>
        <div class="compare-cell good">Fast O(nψt)</div>

        <div class="compare-cell">Transparency</div>
        <div class="compare-cell good">High</div>
        <div class="compare-cell mid">Score-based</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── LIMITATIONS ──────────────────────────────────────────────────────────────
col_lim, col_next = st.columns(2)
with col_lim:
    st.markdown('<div class="section-header">▸ CURRENT LIMITATIONS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-body">
            <strong>⚠ Binary classification only</strong> — System detects anomalies but does not classify
            attack type (DDoS, port scan, brute force, etc.)<br><br>
            <strong>⚠ Numeric features only</strong> — Protocol strings, IPs, and categorical data
            must be pre-encoded before analysis<br><br>
            <strong>⚠ Contamination sensitivity</strong> — The threshold parameter significantly affects
            false positive/negative trade-off and requires domain tuning<br><br>
            <strong>⚠ Temporal patterns</strong> — Current implementation does not model time-series
            sequences; each flow is treated independently<br><br>
            <strong>⚠ No deep packet inspection</strong> — Analysis is limited to flow-level metadata,
            not packet payload content
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_next:
    st.markdown('<div class="section-header">▸ FUTURE ROADMAP</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-body">
            <strong>→ Multi-class attack classification</strong><br>
            Random Forest / XGBoost with labeled CICIDS data for attack-type labeling<br><br>
            <strong>→ Temporal sequence modeling</strong><br>
            LSTM / GRU networks to capture time-series patterns in traffic flows<br><br>
            <strong>→ Real-time packet capture integration</strong><br>
            Direct pcap/NetFlow integration for live monitoring<br><br>
            <strong>→ SHAP explainability layer</strong><br>
            Feature-level explanations for each flagged anomaly<br><br>
            <strong>→ SIEM integration</strong><br>
            Webhook/API output to Splunk, ELK, and other SIEM platforms<br><br>
            <strong>→ Federated learning</strong><br>
            Cross-organization model updates without sharing raw traffic data
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

col_n1, col_n2, _ = st.columns([1, 1, 2])
with col_n1:
    if st.button("← BACK TO DETECT", use_container_width=True):
        st.switch_page("pages/1_detect.py")
with col_n2:
    if st.button("VIEW ANALYTICS", use_container_width=True):
        st.switch_page("pages/2_analytics.py")