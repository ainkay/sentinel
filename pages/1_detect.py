import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="SENTINEL — Detect",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── SHARED CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600&display=swap');

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }
section[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 20px 40px !important; max-width: 100% !important; }

* { box-sizing: border-box; }

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

/* PAGE TITLE */
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
    margin-bottom: 40px;
}

/* BUTTONS */
.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(0,245,255,0.5) !important;
    color: #00f5ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    letter-spacing: 0.2em !important;
    padding: 14px 30px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}

.stButton > button:hover {
    background: rgba(0,245,255,0.1) !important;
    border-color: #00f5ff !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.3) !important;
}

/* METRIC CARDS */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 30px 0;
}

.metric-card {
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 24px 20px;
    clip-path: polygon(0 0, calc(100% - 12px) 0, 100% 12px, 100% 100%, 12px 100%, 0 calc(100% - 12px));
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.metric-card:hover {
    border-color: rgba(0,245,255,0.5);
    box-shadow: 0 0 20px rgba(0,245,255,0.08);
}

.metric-label {
    font-size: 10px;
    color: rgba(0,245,255,0.45);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.metric-value {
    font-family: 'Orbitron', monospace;
    font-size: 28px;
    font-weight: 700;
    line-height: 1;
}

.metric-value.normal { color: #00ff88; text-shadow: 0 0 15px rgba(0,255,136,0.5); }
.metric-value.warning { color: #ffaa00; text-shadow: 0 0 15px rgba(255,170,0,0.5); }
.metric-value.danger { color: #ff3366; text-shadow: 0 0 15px rgba(255,51,102,0.5); }
.metric-value.info { color: #00f5ff; text-shadow: 0 0 15px rgba(0,245,255,0.5); }

.metric-delta {
    font-size: 11px;
    color: rgba(0,245,255,0.4);
    margin-top: 8px;
}

/* THREAT GAUGE */
.threat-section {
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.15);
    padding: 30px;
    margin: 20px 0;
    clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 calc(100% - 20px));
}

.threat-title {
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    letter-spacing: 0.2em;
    color: rgba(0,245,255,0.7);
    margin-bottom: 20px;
    text-transform: uppercase;
}

.threat-bar-bg {
    background: rgba(0,245,255,0.08);
    height: 12px;
    position: relative;
    overflow: hidden;
    clip-path: polygon(0 0, calc(100% - 6px) 0, 100% 6px, 100% 100%, 6px 100%, 0 calc(100% - 6px));
}

.threat-bar-fill {
    height: 100%;
    transition: width 1.5s cubic-bezier(0.23, 1, 0.32, 1);
}

.threat-label-row {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 11px;
    color: rgba(0,245,255,0.4);
}

/* SECTION DIVIDER */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
    margin: 30px 0;
}

/* Back button */
.back-btn .stButton > button {
    font-size: 11px !important;
    padding: 8px 20px !important;
    border-color: rgba(0,245,255,0.3) !important;
    color: rgba(0,245,255,0.6) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── IMPORTS ──────────────────────────────────────────────────────────────────
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

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

# ─── BACK BUTTON ──────────────────────────────────────────────────────────────
col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← BACK TO HOME"):
        st.switch_page("app.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TITLE ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">▸ ANOMALY DETECTION ENGINE</div>
<div class="page-subtitle">// Upload network traffic CSV → ML analysis → Threat intelligence</div>
""", unsafe_allow_html=True)

# ─── SETTINGS ROW ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    uploaded_file = st.file_uploader(
        "UPLOAD NETWORK TRAFFIC CSV",
        type=["csv"],
        help="Supports CICIDS2017, NSL-KDD, UNSW-NB15 formats"
    )
with col2:
    contamination = st.slider(
        "ANOMALY SENSITIVITY",
        min_value=0.01, max_value=0.30, value=0.05, step=0.01,
        help="Expected proportion of anomalies (0.05 = 5%)"
    )
with col3:
    n_estimators = st.selectbox(
        "MODEL STRENGTH",
        [100, 200, 300, 500],
        index=1,
        help="Number of isolation trees"
    )

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── DEMO DATA BUTTON ─────────────────────────────────────────────────────────
col_demo, _ = st.columns([1, 3])
with col_demo:
    use_demo = st.button("⬡ LOAD DEMO TRAFFIC DATA")

# ─── DATA GENERATION / LOADING ────────────────────────────────────────────────
df = None

if use_demo:
    np.random.seed(42)
    n = 2000
    normal_data = {
        'Flow Duration': np.random.exponential(500, int(n * 0.92)),
        'Total Fwd Packets': np.random.poisson(8, int(n * 0.92)),
        'Total Backward Packets': np.random.poisson(6, int(n * 0.92)),
        'Total Length of Fwd Packets': np.random.normal(400, 120, int(n * 0.92)),
        'Total Length of Bwd Packets': np.random.normal(300, 100, int(n * 0.92)),
        'Flow Bytes/s': np.random.normal(5000, 2000, int(n * 0.92)),
        'Flow Packets/s': np.random.normal(50, 20, int(n * 0.92)),
        'Fwd Packet Length Mean': np.random.normal(50, 15, int(n * 0.92)),
        'Bwd Packet Length Mean': np.random.normal(45, 12, int(n * 0.92)),
        'Packet Length Mean': np.random.normal(48, 14, int(n * 0.92)),
        'Destination Port': np.random.choice([80, 443, 22, 8080, 3306], int(n * 0.92)),
    }
    attack_data = {
        'Flow Duration': np.random.exponential(50, int(n * 0.08)),
        'Total Fwd Packets': np.random.poisson(200, int(n * 0.08)),
        'Total Backward Packets': np.random.poisson(2, int(n * 0.08)),
        'Total Length of Fwd Packets': np.random.normal(50000, 10000, int(n * 0.08)),
        'Total Length of Bwd Packets': np.random.normal(100, 50, int(n * 0.08)),
        'Flow Bytes/s': np.random.normal(500000, 100000, int(n * 0.08)),
        'Flow Packets/s': np.random.normal(5000, 1000, int(n * 0.08)),
        'Fwd Packet Length Mean': np.random.normal(250, 50, int(n * 0.08)),
        'Bwd Packet Length Mean': np.random.normal(10, 5, int(n * 0.08)),
        'Packet Length Mean': np.random.normal(230, 45, int(n * 0.08)),
        'Destination Port': np.random.choice([0, 1, 65535, 31337, 4444], int(n * 0.08)),
    }
    df_normal = pd.DataFrame(normal_data)
    df_attack = pd.DataFrame(attack_data)
    df = pd.concat([df_normal, df_attack], ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    st.success("✓ DEMO TRAFFIC DATA LOADED — 2,000 flow records across 11 features")

elif uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.columns = df.columns.str.strip()
        st.success(f"✓ FILE LOADED — {len(df):,} records × {len(df.columns)} features")
    except Exception as e:
        st.error(f"✗ PARSE ERROR: {e}")

# ─── ANALYSIS ─────────────────────────────────────────────────────────────────
# restore any previous scan from session state so results persist across runs
result_df = None
scan_done = False
if 'result_df' in st.session_state and st.session_state['result_df']:
    try:
        result_df = pd.read_json(st.session_state['result_df'])
        scan_done = True
    except Exception:
        result_df = None

if df is not None:
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    numeric_df = df.select_dtypes(include=['number']).copy()
    numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan).dropna(axis=1, how='all')
    numeric_df = numeric_df.fillna(numeric_df.median())

    if numeric_df.empty or numeric_df.shape[1] < 2:
        st.error("✗ INSUFFICIENT NUMERIC FEATURES — Minimum 2 required.")
    else:
        with st.expander("▸ RAW TRAFFIC PREVIEW (first 20 rows)"):
            st.dataframe(df.head(20), use_container_width=True)

        run_col, _ = st.columns([1, 3])
        with run_col:
            run_btn = st.button("⬡  INITIATE THREAT SCAN  ⬡", use_container_width=True)

        if run_btn or use_demo:
            with st.spinner("SCANNING TRAFFIC PATTERNS..."):
                progress = st.progress(0)
                for i in range(0, 101, 5):
                    time.sleep(0.02)
                    progress.progress(i)

                scaler = StandardScaler()
                scaled = scaler.fit_transform(numeric_df)

                model = IsolationForest(
                    n_estimators=n_estimators,
                    contamination=contamination,
                    random_state=42
                )
                model.fit(scaled)
                predictions = model.predict(scaled)
                scores = model.decision_function(scaled)

                result_df = df.copy()
                result_df['__anomaly_flag'] = predictions
                result_df['__anomaly_label'] = result_df['__anomaly_flag'].map({1: 'Normal', -1: 'Anomalous'})
                result_df['__anomaly_score'] = np.round(scores, 4)
                result_df['__risk_pct'] = np.round((scores.min() - scores) / (scores.min() - scores.max()) * 100, 1)
                # persist scan output so we can show results after reruns or when clicking analytics
                st.session_state['result_df'] = result_df.to_json()
                scan_done = True

            progress.empty()
            st.success("✓ SCAN COMPLETE — THREAT ANALYSIS READY")

        # show results anytime a scan is stored in session_state
        if scan_done:
            total = len(result_df)
            anomalies = (result_df['__anomaly_label'] == 'Anomalous').sum()
            normal = total - anomalies
            anomaly_pct = anomalies / total * 100
            health = 100 - anomaly_pct

            if health > 90:
                health_status = "SECURE"
                health_color = "normal"
                threat_color = "#00ff88"
            elif health > 75:
                health_status = "ELEVATED RISK"
                health_color = "warning"
                threat_color = "#ffaa00"
            elif health > 60:
                health_status = "HIGH RISK"
                health_color = "warning"
                threat_color = "#ff6b35"
            else:
                health_status = "CRITICAL"
                health_color = "danger"
                threat_color = "#ff3366"

            st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-card">
                    <div class="metric-label">Total Records Analyzed</div>
                    <div class="metric-value info">{total:,}</div>
                    <div class="metric-delta">→ {numeric_df.shape[1]} features used</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Anomalies Detected</div>
                    <div class="metric-value danger">{anomalies:,}</div>
                    <div class="metric-delta">→ {anomaly_pct:.1f}% of traffic</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Normal Traffic</div>
                    <div class="metric-value normal">{normal:,}</div>
                    <div class="metric-delta">→ {100 - anomaly_pct:.1f}% of traffic</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Network Status</div>
                    <div class="metric-value {health_color}">{health_status}</div>
                    <div class="metric-delta">→ Health: {health:.1f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="threat-section">
                <div class="threat-title">▸ THREAT INDEX GAUGE</div>
                <div class="threat-bar-bg">
                    <div class="threat-bar-fill" style="
                        width: {anomaly_pct:.1f}%;
                        background: linear-gradient(90deg, #00ff88, {threat_color});
                    "></div>
                </div>
                <div class="threat-label-row">
                    <span>SECURE</span>
                    <span style="color:{threat_color}; font-family:'Orbitron',monospace; font-size:16px;">
                        {anomaly_pct:.1f}% ANOMALOUS
                    </span>
                    <span>CRITICAL</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            col_chart1, col_chart2 = st.columns(2)

            with col_chart1:
                st.markdown("**▸ ANOMALY SCORE DISTRIBUTION**", unsafe_allow_html=False)

                normal_scores = result_df[result_df['__anomaly_label'] == 'Normal']['__anomaly_score']
                anom_scores = result_df[result_df['__anomaly_label'] == 'Anomalous']['__anomaly_score']

                fig1 = go.Figure()
                fig1.add_trace(go.Histogram(
                    x=normal_scores, name='Normal',
                    marker_color='rgba(0,255,136,0.7)',
                    nbinsx=40, opacity=0.8
                ))
                fig1.add_trace(go.Histogram(
                    x=anom_scores, name='Anomalous',
                    marker_color='rgba(255,51,102,0.8)',
                    nbinsx=40, opacity=0.8
                ))
                fig1.update_layout(
                    barmode='overlay',
                    paper_bgcolor='rgba(0,10,20,0.8)',
                    plot_bgcolor='rgba(0,10,20,0.5)',
                    font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono'),
                    legend=dict(font=dict(color='rgba(0,245,255,0.7)')),
                    xaxis=dict(gridcolor='rgba(0,245,255,0.08)', title='Anomaly Score'),
                    yaxis=dict(gridcolor='rgba(0,245,255,0.08)', title='Count'),
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=280
                )
                st.plotly_chart(fig1, use_container_width=True)

            with col_chart2:
                st.markdown("**▸ TRAFFIC CLASSIFICATION BREAKDOWN**", unsafe_allow_html=False)
                labels = ['Normal', 'Anomalous']
                values = [normal, anomalies]
                colors = ['rgba(0,255,136,0.8)', 'rgba(255,51,102,0.8)']

                fig2 = go.Figure(go.Pie(
                    labels=labels, values=values,
                    hole=0.6,
                    marker=dict(colors=colors, line=dict(color='#000408', width=3)),
                    textfont=dict(family='Orbitron', size=11, color='white')
                ))
                fig2.update_layout(
                    paper_bgcolor='rgba(0,10,20,0.8)',
                    font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono'),
                    legend=dict(font=dict(color='rgba(0,245,255,0.7)')),
                    margin=dict(l=10, r=10, t=20, b=10),
                    height=280,
                    annotations=[dict(
                        text=f'{anomaly_pct:.0f}%<br>THREAT',
                        x=0.5, y=0.5, font_size=14,
                        font=dict(family='Orbitron', color='#ff3366'),
                        showarrow=False
                    )]
                )
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            st.markdown("### ▸ FLAGGED ANOMALOUS TRAFFIC")

            flagged = result_df[result_df['__anomaly_label'] == 'Anomalous'].copy()
            flagged = flagged.sort_values('__risk_pct', ascending=False)

            display_cols = [c for c in flagged.columns if not c.startswith('__')][:12]
            display_cols += ['__anomaly_score', '__risk_pct', '__anomaly_label']

            st.dataframe(
                flagged[display_cols].head(100).rename(columns={
                    '__anomaly_score': 'Score',
                    '__risk_pct': 'Risk%',
                    '__anomaly_label': 'Status'
                }),
                use_container_width=True,
                height=350
            )

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            with col_dl1:
                csv_all = result_df.rename(columns={
                    '__anomaly_label': 'Status',
                    '__anomaly_score': 'Score',
                    '__risk_pct': 'Risk%'
                }).to_csv(index=False)
                st.download_button(
                    "⬡ DOWNLOAD FULL RESULTS",
                    data=csv_all,
                    file_name="sentinel_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_dl2:
                csv_flagged = flagged.rename(columns={
                    '__anomaly_label': 'Status',
                    '__anomaly_score': 'Score',
                    '__risk_pct': 'Risk%'
                }).to_csv(index=False)
                st.download_button(
                    "⬡ DOWNLOAD THREATS ONLY",
                    data=csv_flagged,
                    file_name="sentinel_threats.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col_dl3:
                if st.button("⬡ VIEW ANALYTICS →", use_container_width=True):
                    st.switch_page("pages/2_analytics.py")

else:
    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:20px; margin-top:20px;">
        <div style="border:1px solid rgba(0,245,255,0.15); padding:24px; background:rgba(0,10,20,0.5);
             clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px));">
            <div style="font-size:24px; margin-bottom:12px;">📡</div>
            <div style="font-family:'Orbitron',monospace; font-size:12px; color:rgba(0,245,255,0.8); margin-bottom:8px; letter-spacing:0.1em;">STEP 1</div>
            <div style="font-size:13px; color:rgba(0,245,255,0.6);">Upload a network traffic CSV (CICIDS2017, NSL-KDD) or load demo data</div>
        </div>
        <div style="border:1px solid rgba(0,245,255,0.15); padding:24px; background:rgba(0,10,20,0.5);
             clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px));">
            <div style="font-size:24px; margin-bottom:12px;">🧠</div>
            <div style="font-family:'Orbitron',monospace; font-size:12px; color:rgba(0,245,255,0.8); margin-bottom:8px; letter-spacing:0.1em;">STEP 2</div>
            <div style="font-size:13px; color:rgba(0,245,255,0.6);">Isolation Forest ML scans traffic features to identify statistical outliers</div>
        </div>
        <div style="border:1px solid rgba(0,245,255,0.15); padding:24px; background:rgba(0,10,20,0.5);
             clip-path:polygon(0 0,calc(100% - 12px) 0,100% 12px,100% 100%,12px 100%,0 calc(100% - 12px));">
            <div style="font-size:24px; margin-bottom:12px;">🚨</div>
            <div style="font-family:'Orbitron',monospace; font-size:12px; color:rgba(0,245,255,0.8); margin-bottom:8px; letter-spacing:0.1em;">STEP 3</div>
            <div style="font-size:13px; color:rgba(0,245,255,0.6);">Review threat dashboard, download flagged traffic, navigate to analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)