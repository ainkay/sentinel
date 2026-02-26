import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

st.set_page_config(
    page_title="SENTINEL — Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS (shared theme) ───────────────────────────────────────────────────────
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
    font-size: 32px; font-weight: 700;
    color: #00f5ff;
    text-shadow: 0 0 30px rgba(0,245,255,0.5);
    letter-spacing: 0.1em; margin-bottom: 8px;
}
.page-subtitle { font-size: 13px; color: rgba(0,245,255,0.5); letter-spacing: 0.1em; margin-bottom: 40px; }

.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 14px; letter-spacing: 0.2em;
    color: rgba(0,245,255,0.8);
    margin: 30px 0 16px;
    text-transform: uppercase;
    border-left: 3px solid #00f5ff;
    padding-left: 12px;
}

.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
    margin: 30px 0;
}

.insight-card {
    background: rgba(0,10,20,0.8);
    border: 1px solid rgba(0,245,255,0.2);
    padding: 20px;
    clip-path: polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,10px 100%,0 calc(100% - 10px));
    transition: all 0.3s ease;
}
.insight-card:hover { border-color: rgba(0,245,255,0.5); }

.insight-label {
    font-size: 10px; color: rgba(0,245,255,0.4);
    letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px;
}
.insight-value {
    font-family: 'Orbitron', monospace;
    font-size: 22px; font-weight: 700;
    color: #00f5ff; text-shadow: 0 0 15px rgba(0,245,255,0.4);
}
.insight-sub { font-size: 11px; color: rgba(0,245,255,0.4); margin-top: 6px; }

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
    font-size: 11px !important;
    padding: 8px 20px !important;
    border-color: rgba(0,245,255,0.3) !important;
    color: rgba(0,245,255,0.6) !important;
}
</style>
""", unsafe_allow_html=True)

# ─── PLOTLY THEME ─────────────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,10,20,0.8)',
    plot_bgcolor='rgba(0,4,12,0.5)',
    font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=11),
    legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)'),
    xaxis=dict(gridcolor='rgba(0,245,255,0.07)', zeroline=False, showspikes=True, spikecolor='rgba(0,245,255,0.3)'),
    yaxis=dict(gridcolor='rgba(0,245,255,0.07)', zeroline=False),
    margin=dict(l=10, r=10, t=30, b=10),
    # height removed here; charts will specify explicit heights when needed
)

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

# ─── BACK ─────────────────────────────────────────────────────────────────────
col_back, _ = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← BACK TO DETECT"):
        st.switch_page("pages/1_detect.py")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── TITLE ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">▸ TRAFFIC ANALYTICS LAB</div>
<div class="page-subtitle">// Deep-dive into feature distributions, correlations, and PCA anomaly maps</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ────────────────────────────────────────────────────────────────
result_df = None
if 'result_df' in st.session_state and st.session_state['result_df']:
    try:
        result_df = pd.read_json(st.session_state['result_df'])
    except Exception:
        result_df = None

if result_df is None:
    st.info("ℹ No scan data found — loading demo dataset for analysis")
    if st.button("← BACK TO DETECT", key="back_demo"):
        st.switch_page("pages/1_detect.py")
    np.random.seed(42)
    n = 1500
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
    df_n = pd.DataFrame(normal_data)
    df_a = pd.DataFrame(attack_data)
    raw_df = pd.concat([df_n, df_a], ignore_index=True).sample(frac=1, random_state=42)

    scaler = StandardScaler()
    num_cols = raw_df.select_dtypes(include='number').columns
    scaled = scaler.fit_transform(raw_df[num_cols])
    model = IsolationForest(n_estimators=200, contamination=0.08, random_state=42)
    # train isolation forest on the scaled demo data before making predictions
    model.fit(scaled)
    preds = model.predict(scaled)
    scores = model.decision_function(scaled)
    result_df = raw_df.copy()
    result_df['__anomaly_label'] = pd.Series(preds).map({1: 'Normal', -1: 'Anomalous'}).values
    result_df['__anomaly_score'] = np.round(scores, 4)
    result_df['__risk_pct'] = np.round((scores.min() - scores) / (scores.min() - scores.max()) * 100, 1)

# ─── PREP ─────────────────────────────────────────────────────────────────────
numeric_cols = [c for c in result_df.columns if c not in ('__anomaly_flag', '__anomaly_label', '__anomaly_score', '__risk_pct')
                and pd.api.types.is_numeric_dtype(result_df[c])]

total = len(result_df)
anomalies_mask = result_df['__anomaly_label'] == 'Anomalous'
anomalies = anomalies_mask.sum()
normal = total - anomalies
anomaly_pct = anomalies / total * 100

# ─── INSIGHT CARDS ────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ INTELLIGENCE SUMMARY</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_risk = result_df.loc[anomalies_mask, '__risk_pct'].mean() if anomalies > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">Avg Threat Severity</div>
        <div class="insight-value" style="color:#ff3366;">{avg_risk:.0f}%</div>
        <div class="insight-sub">Mean risk for anomalies</div>
    </div>""", unsafe_allow_html=True)
with col2:
    high_risk = (result_df['__risk_pct'] > 75).sum()
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">Critical Threats</div>
        <div class="insight-value" style="color:#ff6b35;">{high_risk}</div>
        <div class="insight-sub">Risk score &gt; 75%</div>
    </div>""", unsafe_allow_html=True)
with col3:
    features_used = len(numeric_cols)
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">Features Analyzed</div>
        <div class="insight-value">{features_used}</div>
        <div class="insight-sub">Numeric traffic features</div>
    </div>""", unsafe_allow_html=True)
with col4:
    clean_pct = 100 - anomaly_pct
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">Clean Traffic</div>
        <div class="insight-value" style="color:#00ff88;">{clean_pct:.0f}%</div>
        <div class="insight-sub">{normal:,} normal flows</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── PCA 2D ANOMALY MAP ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ PCA ANOMALY MAP — 2D PROJECTION</div>', unsafe_allow_html=True)

if len(numeric_cols) >= 2:
    pca_data = result_df[numeric_cols].replace([np.inf, -np.inf], np.nan).fillna(0)
    scaler_pca = StandardScaler()
    scaled_pca = scaler_pca.fit_transform(pca_data)
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(scaled_pca)
    var_explained = pca.explained_variance_ratio_

    pca_df = pd.DataFrame({
        'PC1': components[:, 0],
        'PC2': components[:, 1],
        'Label': result_df['__anomaly_label'].values,
        'Risk': result_df['__risk_pct'].values,
        'Score': result_df['__anomaly_score'].values,
    })

    normal_pts = pca_df[pca_df['Label'] == 'Normal']
    anom_pts = pca_df[pca_df['Label'] == 'Anomalous']

    fig_pca = go.Figure()
    fig_pca.add_trace(go.Scattergl(
        x=normal_pts['PC1'], y=normal_pts['PC2'],
        mode='markers', name='Normal',
        marker=dict(color='rgba(0,255,136,0.4)', size=4, line=dict(width=0)),
        hovertemplate='PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra>Normal</extra>'
    ))
    fig_pca.add_trace(go.Scattergl(
        x=anom_pts['PC1'], y=anom_pts['PC2'],
        mode='markers', name='Anomalous',
        marker=dict(
            color=anom_pts['Risk'],
            colorscale=[[0, 'rgba(255,107,53,0.7)'], [1, 'rgba(255,51,102,1)']],
            size=7, line=dict(color='rgba(255,51,102,0.8)', width=0.5),
            showscale=True,
            colorbar=dict(title='Risk%', tickfont=dict(color='rgba(0,245,255,0.6)', size=10))
        ),
        hovertemplate='PC1: %{x:.2f}<br>PC2: %{y:.2f}<br>Risk: %{marker.color:.0f}%<extra>ANOMALY</extra>'
    ))
    fig_pca.update_layout(
        **PLOTLY_LAYOUT,
        # height is specified separately to avoid conflicts with layout defaults
        xaxis_title=f'PC1 ({var_explained[0]*100:.1f}% variance)',
        yaxis_title=f'PC2 ({var_explained[1]*100:.1f}% variance)',
        title=dict(text='', x=0.5)
    )
    fig_pca.update_layout(height=420)
    st.plotly_chart(fig_pca, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── FEATURE DISTRIBUTIONS ────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ FEATURE DISTRIBUTION COMPARISON</div>', unsafe_allow_html=True)

if numeric_cols:
    sel_feature = st.selectbox("SELECT FEATURE", numeric_cols, key='feat_sel')
    normal_vals = result_df[result_df['__anomaly_label'] == 'Normal'][sel_feature].replace([np.inf, -np.inf], np.nan).dropna()
    anom_vals = result_df[result_df['__anomaly_label'] == 'Anomalous'][sel_feature].replace([np.inf, -np.inf], np.nan).dropna()

    col_hist, col_box = st.columns(2)
    with col_hist:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=normal_vals, name='Normal',
            marker_color='rgba(0,255,136,0.6)', nbinsx=40, opacity=0.75
        ))
        fig_hist.add_trace(go.Histogram(
            x=anom_vals, name='Anomalous',
            marker_color='rgba(255,51,102,0.75)', nbinsx=40, opacity=0.75
        ))
        fig_hist.update_layout(**PLOTLY_LAYOUT, height=320, barmode='overlay', xaxis_title=sel_feature, yaxis_title='Count')
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_box:
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=normal_vals, name='Normal',
            marker_color='rgba(0,255,136,0.7)',
            line_color='rgba(0,255,136,0.9)',
            fillcolor='rgba(0,255,136,0.1)'
        ))
        fig_box.add_trace(go.Box(
            y=anom_vals, name='Anomalous',
            marker_color='rgba(255,51,102,0.7)',
            line_color='rgba(255,51,102,0.9)',
            fillcolor='rgba(255,51,102,0.1)'
        ))
        fig_box.update_layout(**PLOTLY_LAYOUT, height=320, yaxis_title=sel_feature)
        st.plotly_chart(fig_box, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── FEATURE IMPORTANCE (anomaly score correlation) ───────────────────────────
st.markdown('<div class="section-header">▸ FEATURE ANOMALY CORRELATION</div>', unsafe_allow_html=True)

if numeric_cols and '__anomaly_score' in result_df.columns:
    corr_vals = {}
    for col in numeric_cols[:20]:
        try:
            c = result_df[col].replace([np.inf, -np.inf], np.nan).dropna()
            s = result_df.loc[c.index, '__anomaly_score']
            corr = np.corrcoef(c, s)[0, 1]
            if not np.isnan(corr):
                corr_vals[col] = abs(corr)
        except Exception:
            pass

    if corr_vals:
        corr_sorted = sorted(corr_vals.items(), key=lambda x: x[1], reverse=True)[:15]
        features_c, corrs_c = zip(*corr_sorted)
        colors_corr = ['rgba(255,51,102,0.8)' if c > 0.3 else 'rgba(0,245,255,0.6)' for c in corrs_c]

        fig_corr = go.Figure(go.Bar(
            x=list(corrs_c), y=list(features_c),
            orientation='h',
            marker=dict(color=colors_corr, line=dict(width=0)),
            hovertemplate='%{y}: %{x:.3f}<extra></extra>'
        ))
        # apply base layout and explicit height/title first
        fig_corr.update_layout(
            **PLOTLY_LAYOUT,
            height=380,
            xaxis_title='|Correlation with Anomaly Score|'
        )
        # customize the y-axis separately to avoid passing the same key twice
        fig_corr.update_yaxes(
            gridcolor='rgba(0,245,255,0.07)',
            zeroline=False,
            tickfont=dict(size=10)
        )
        st.plotly_chart(fig_corr, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── RISK SCORE TIMELINE ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ ANOMALY SCORE TIMELINE (RECORD ORDER)</div>', unsafe_allow_html=True)

if '__anomaly_score' in result_df.columns:
    sample_size = min(500, len(result_df))
    idx = np.linspace(0, len(result_df) - 1, sample_size, dtype=int)
    timeline_df = result_df.iloc[idx].reset_index(drop=True)

    fig_time = go.Figure()
    fig_time.add_trace(go.Scatter(
        x=list(range(len(timeline_df))),
        y=timeline_df['__anomaly_score'],
        mode='lines', name='Anomaly Score',
        line=dict(color='rgba(0,245,255,0.6)', width=1.5),
        fill='tozeroy', fillcolor='rgba(0,245,255,0.05)'
    ))

    anom_pts_t = timeline_df[timeline_df['__anomaly_label'] == 'Anomalous']
    if len(anom_pts_t) > 0:
        fig_time.add_trace(go.Scatter(
            x=anom_pts_t.index.tolist(),
            y=anom_pts_t['__anomaly_score'],
            mode='markers', name='Anomalous',
            marker=dict(color='rgba(255,51,102,0.9)', size=6, symbol='circle')
        ))

    threshold = timeline_df['__anomaly_score'].quantile(0.05)
    fig_time.add_hline(
        y=threshold, line_dash='dash',
        line_color='rgba(255,170,0,0.6)',
        annotation_text='THRESHOLD',
        annotation_font_color='rgba(255,170,0,0.8)'
    )

    fig_time.update_layout(
        **PLOTLY_LAYOUT, height=260,
        xaxis_title='Record Index', yaxis_title='Decision Score'
    )
    st.plotly_chart(fig_time, use_container_width=True)

# ─── NAV BOTTOM ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
col_n1, col_n2, col_n3 = st.columns(3)
with col_n1:
    if st.button("← BACK TO DETECTION", use_container_width=True):
        st.switch_page("pages/1_detect.py")
with col_n3:
    if st.button("MODEL INFO →", use_container_width=True):
        st.switch_page("pages/3_model.py")