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
<div class="page-subtitle">// Dual Statistical Methods — Z-score & IQR anomaly detection with weighted risk scoring</div>
""", unsafe_allow_html=True)

# ─── HOW IT WORKS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ DETECTION METHODOLOGY</div>', unsafe_allow_html=True)

st.markdown("""
<div class="tech-card">
    <div class="tech-card-title">Overview: Transparent Statistical Anomaly Detection</div>
    <div class="tech-card-body">
        SENTINEL uses <strong>dual statistical methods</strong> combined into a <strong>weighted composite risk index</strong>.<br><br>
        Instead of black-box machine learning, anomaly detection is based on fundamental statistical principles:<br>
        <strong>1) Z-score deviation</strong> — Flag rows where any feature deviates from mean by >2.5 standard deviations<br>
        <strong>2) IQR method</strong> — Flag rows where any feature falls outside Tukey's boxplot bounds<br>
        <strong>3) Composite risk</strong> — Combine deviations into a normalized 0–100 risk score<br><br>
        <strong>Philosophy:</strong> Every decision is mathematically auditable, interpretable, and fast.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STEP 1: STANDARDIZATION ──────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ STEP 1: STANDARDIZATION (Z-SCORE NORMALIZATION)</div>', unsafe_allow_html=True)

col_1a, col_1b = st.columns([3, 2])
with col_1a:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Mathematical Foundation</div>
        <div class="tech-card-body">
            Before anomaly detection, all features are standardized to have <strong>mean = 0</strong> and <strong>standard deviation = 1</strong>.<br><br>
            This enables fair comparison across features with different units and scales (e.g., packet count vs. duration in seconds).<br><br>
            <strong>Why standardization matters:</strong> A packet count difference of 1000 might be significant, but a duration difference of 1000 seconds is huge. Without scaling, we cannot fairly combine them.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <strong>Z-Score Formula (per feature):</strong><br>
        Z<sub>ij</sub> = (X<sub>ij</sub> − μ<sub>j</sub>) / σ<sub>j</sub><br><br>
        X<sub>ij</sub> = original value for sample i, feature j<br>
        μ<sub>j</sub> = mean of feature j<br>
        σ<sub>j</sub> = standard deviation of feature j<br>
        Z<sub>ij</sub> = standardized value (units: standard deviations from mean)
    </div>
    """, unsafe_allow_html=True)

with col_1b:
    np.random.seed(42)
    original = np.random.normal(100, 20, 500)
    standardized = (original - np.mean(original)) / np.std(original)

    fig_std = go.Figure()
    fig_std.add_trace(go.Histogram(
        x=original, name='Original (μ≈100, σ≈20)',
        marker_color='rgba(255,170,0,0.6)', nbinsx=25, opacity=0.7
    ))
    fig_std.add_trace(go.Histogram(
        x=standardized, name='Standardized (μ=0, σ=1)',
        marker_color='rgba(0,255,136,0.6)', nbinsx=25, opacity=0.7
    ))
    fig_std.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=10),
        legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)', x=0.4, y=0.95),
        xaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Value'),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Count'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        title=dict(text='Standardization Effect', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_std, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STEP 2: MULTIVARIATE Z-SCORE DETECTION ────────────────────────────────
st.markdown('<div class="section-header">▸ STEP 2: MULTIVARIATE Z-SCORE DETECTION</div>', unsafe_allow_html=True)

col_2a, col_2b = st.columns([3, 2])
with col_2a:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Method: Statistical Deviation Detection</div>
        <div class="tech-card-body">
            For each row (network flow), compute the Z-score of all numeric features.<br><br>
            <strong>Detection rule:</strong> Flag a row as anomalous if <strong>ANY</strong> feature has |Z| > threshold (default 2.5).<br><br>
            <strong>Interpretation:</strong> Z = 2.5 means the value is 2.5 standard deviations from the mean, 
            which occurs in <~2% of normal data (99% confidence level).<br><br>
            <strong>Advantages:</strong> Fast, transparent, multivariate-aware, based on normal distribution assumption
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <strong>Multivariate Z-Score Test:</strong><br>
        Anomalous if: max(|Z<sub>i1</sub>|, |Z<sub>i2</sub>|, ..., |Z<sub>in</sub>|) > threshold<br><br>
        Threshold = 2.5 ⟹ ~99% of normal data passes<br>
        Threshold = 3.0 ⟹ ~99.7% of normal data passes<br><br>
        <strong>Deviation Score (for visualization):</strong><br>
        Deviation<sub>i</sub> = Σ |Z<sub>ij</sub>| / number of features<br>
        (Average absolute Z-score across all features)
    </div>
    """, unsafe_allow_html=True)

with col_2b:
    np.random.seed(42)
    normal_z = np.random.normal(0, 1, 800)
    anomalous_z = np.concatenate([np.random.normal(3.5, 0.8, 40), np.random.normal(-3.5, 0.8, 40)])

    fig_zscore = go.Figure()
    fig_zscore.add_vline(x=2.5, line_dash="dash", line_color="rgba(0,255,136,0.5)", annotation_text="threshold=2.5")
    fig_zscore.add_vline(x=-2.5, line_dash="dash", line_color="rgba(0,255,136,0.5)")
    fig_zscore.add_trace(go.Histogram(
        x=normal_z, name='Normal Z-scores',
        marker_color='rgba(0,255,136,0.6)', nbinsx=40, opacity=0.7
    ))
    fig_zscore.add_trace(go.Histogram(
        x=anomalous_z, name='Anomalous Z-scores',
        marker_color='rgba(255,51,102,0.8)', nbinsx=15, opacity=0.8
    ))
    fig_zscore.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=9),
        legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)', x=0.35, y=0.95),
        xaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Z-Score'),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Count'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        title=dict(text='Z-Score Distribution (Normal vs Anomalous)', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_zscore, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STEP 3: IQR METHOD ────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ STEP 3: IQR (INTERQUARTILE RANGE) METHOD</div>', unsafe_allow_html=True)

col_3a, col_3b = st.columns([3, 2])
with col_3a:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Tukey's Boxplot Method</div>
        <div class="tech-card-body">
            The IQR method uses quartiles to define the "normal" range for each feature independently.<br><br>
            <strong>Detection rule:</strong> Flag a feature value as outlier if it falls outside [Q1 − 1.5×IQR, Q3 + 1.5×IQR]<br><br>
            <strong>Key advantage over Z-score:</strong> IQR is <strong>robust to outliers</strong> (doesn't depend on mean/std). 
            A single extreme value cannot distort the bounds.<br><br>
            <strong>Combined detection:</strong> A row is anomalous if <strong>ANY</strong> feature triggers IQR boundaries.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <strong>Quartile Definitions:</strong><br>
        Q1 = 25th percentile (25% of data below)<br>
        Q3 = 75th percentile (75% of data below)<br>
        IQR = Q3 − Q1 (spread of middle 50%)<br><br>
        <strong>Outlier Bounds:</strong><br>
        Lower = Q1 − 1.5 × IQR<br>
        Upper = Q3 + 1.5 × IQR<br><br>
        <strong>Flag if:</strong> X < Lower  OR  X > Upper
    </div>
    """, unsafe_allow_html=True)

with col_3b:
    np.random.seed(42)
    data = np.concatenate([np.random.normal(50, 10, 1000), [10, 15, 110, 120]])
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    fig_iqr = go.Figure()
    fig_iqr.add_trace(go.Box(
        y=data, name='Data',
        marker_color='rgba(255,170,0,0.5)',
        line=dict(color='rgba(0,245,255,0.7)'),
        boxmean=True
    ))
    fig_iqr.update_layout(
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=10),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Value'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        showlegend=False,
        title=dict(text='IQR Boxplot (Outliers shown as points)', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_iqr, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STEP 4: WEIGHTED COMPOSITE RISK INDEX ────────────────────────────────
st.markdown('<div class="section-header">▸ STEP 4: WEIGHTED COMPOSITE RISK INDEX</div>', unsafe_allow_html=True)

col_4a, col_4b = st.columns([3, 2])
with col_4a:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Combining Both Methods into Risk Score</div>
        <div class="tech-card-body">
            Neither Z-score nor IQR is perfect alone:<br>
            <strong>Z-score:</strong> Sensitive to outliers in training data<br>
            <strong>IQR:</strong> Ignores the magnitude of deviation<br><br>
            <strong>Solution:</strong> Normalize both indicators to [0, 1] and combine them with equal weights (0.5 each) 
            into a <strong>0–100 risk score</strong>.<br><br>
            <strong>Final categorization:</strong><br>
            • LOW: 0–25<br>
            • MEDIUM: 25–50<br>
            • HIGH: 50–75<br>
            • CRITICAL: 75–100
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <strong>Risk Scoring Formula:</strong><br>
        Risk<sub>i</sub> = (w<sub>z</sub> × Indicator<sub>zscore,i</sub> + w<sub>iqr</sub> × Indicator<sub>iqr,i</sub>) × 100<br><br>
        Where w<sub>z</sub> = 0.5, w<sub>iqr</sub> = 0.5, and both indicators ∈ [0, 1]<br><br>
        <strong>Indicator Normalization (Min-Max):</strong><br>
        Normalized = (value − min) / (max − min)<br><br>
        <strong>Risk Category:</strong><br>
        IF Risk < 25: LOW<br>
        ELIF Risk < 50: MEDIUM<br>
        ELIF Risk < 75: HIGH<br>
        ELSE: CRITICAL
    </div>
    """, unsafe_allow_html=True)

with col_4b:
    np.random.seed(42)
    risk_scores = np.random.beta(2, 5, 800) * 100  # Skewed towards low risk
    anomaly_scores = np.random.beta(5, 2, 100) * 100  # Skewed towards high risk

    fig_risk = go.Figure()
    fig_risk.add_vline(x=25, line_dash="dash", line_color="rgba(0,255,136,0.5)", annotation_text="LOW|MED")
    fig_risk.add_vline(x=50, line_dash="dash", line_color="rgba(255,170,0,0.5)", annotation_text="MED|HIGH")
    fig_risk.add_vline(x=75, line_dash="dash", line_color="rgba(255,51,102,0.5)", annotation_text="HIGH|CRIT")
    
    fig_risk.add_trace(go.Histogram(
        x=risk_scores, name='Normal Flows',
        marker_color='rgba(0,255,136,0.6)', nbinsx=40, opacity=0.7
    ))
    fig_risk.add_trace(go.Histogram(
        x=anomaly_scores, name='Anomalous Flows',
        marker_color='rgba(255,51,102,0.8)', nbinsx=20, opacity=0.8
    ))
    fig_risk.update_layout(
        barmode='overlay',
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=9),
        legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)', x=0.5, y=0.95),
        xaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Risk Score (0–100)', range=[0, 100]),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='Count'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        title=dict(text='Risk Score Distribution (Detect Page)', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_risk, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STEP 5: PCA VISUALIZATION ────────────────────────────────────────────
st.markdown('<div class="section-header">▸ STEP 5: PRINCIPAL COMPONENT ANALYSIS (PCA 2D PROJECTION)</div>', unsafe_allow_html=True)

col_5a, col_5b = st.columns([3, 2])
with col_5a:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">Dimensionality Reduction</div>
        <div class="tech-card-body">
            Network flow data often has 10+ features (bytes, packets, duration, flags, etc.). 
            <strong>PCA reduces this to 2 dimensions for visualization.</strong><br><br>
            <strong>How PCA works:</strong> <br>
            1) Compute covariance matrix of standardized features<br>
            2) Find eigenvectors (principal components) = directions of maximum variance<br>
            3) Project data onto the first 2 eigenvectors (PC1, PC2)<br>
            4) Plot as 2D scatter: normal points cluster, anomalies appear isolated<br><br>
            <strong>Interpretation:</strong> Green points cluster together (similar behavior), 
            Red points far from cluster (anomalous behavior)
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="formula-box">
        <strong>PCA Process:</strong><br>
        1. Cov(X) = Covariance matrix of features<br>
        2. Eigendecomposition: Cov(X) = V Λ V<sup>T</sup><br>
        3. λ<sub>1</sub> ≥ λ<sub>2</sub> ≥ ... ≥ λ<sub>n</sub> (sorted eigenvalues)<br>
        4. v<sub>1</sub>, v<sub>2</sub> = eigenvectors for top 2 λ's<br><br>
        <strong>Projection:</strong><br>
        PC1 = X · v<sub>1</sub><br>
        PC2 = X · v<sub>2</sub><br><br>
        <strong>Variance Explained:</strong><br>
        Ratio = λ<sub>i</sub> / Σλ<sub>j</sub> (% of total variance captured)
    </div>
    """, unsafe_allow_html=True)

with col_5b:
    np.random.seed(42)
    normal_pca = np.random.multivariate_normal([0, 0], [[1, 0.3], [0.3, 1]], 300)
    anomalous_pca = np.random.multivariate_normal([3, 3], [[0.5, 0], [0, 0.5]], 40)

    fig_pca = go.Figure()
    fig_pca.add_trace(go.Scatter(
        x=normal_pca[:, 0], y=normal_pca[:, 1],
        mode='markers', name='Normal',
        marker=dict(size=6, color='rgba(0,255,136,0.5)', line=dict(color='rgba(0,255,136,0.8)', width=0.5))
    ))
    fig_pca.add_trace(go.Scatter(
        x=anomalous_pca[:, 0], y=anomalous_pca[:, 1],
        mode='markers', name='Anomalous',
        marker=dict(size=8, color='rgba(255,51,102,0.8)', symbol='diamond', line=dict(color='rgba(255,51,102,1)', width=1))
    ))
    fig_pca.update_layout(
        paper_bgcolor='rgba(0,10,20,0.8)',
        plot_bgcolor='rgba(0,4,12,0.5)',
        font=dict(color='rgba(0,245,255,0.7)', family='Share Tech Mono', size=10),
        legend=dict(font=dict(color='rgba(0,245,255,0.7)'), bgcolor='rgba(0,10,20,0.5)'),
        xaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='PC1 (60%)'),
        yaxis=dict(gridcolor='rgba(0,245,255,0.07)', title='PC2 (20%)'),
        margin=dict(l=10, r=10, t=30, b=10),
        height=240,
        title=dict(text='PCA 2D Projection (Analytics Page)', font=dict(size=11, color='rgba(0,245,255,0.6)'), x=0.5)
    )
    st.plotly_chart(fig_pca, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── PROCESSING PIPELINE ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ COMPLETE DETECTION PIPELINE</div>', unsafe_allow_html=True)
st.markdown("""
<div class="pipeline">
    <div class="pipeline-step">
        <div class="pipeline-num">01</div>
        <div class="pipeline-label">Data Cleaning</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">02</div>
        <div class="pipeline-label">Feature Scaling</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">03</div>
        <div class="pipeline-label">Z-Score Deviation</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">04</div>
        <div class="pipeline-label">IQR Detection</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">05</div>
        <div class="pipeline-label">Risk Scoring</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">06</div>
        <div class="pipeline-label">Categorization</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── TECHNICAL SPECS ──────────────────────────────────────────────────────────
col_specs = st.columns([1])[0]

with col_specs:
    st.markdown('<div class="section-header">▸ DETECTION SPECIFICATIONS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tech-card">
        <table class="spec-table">
            <tr><td>Detection Method</td><td>Dual Statistical (Z-score + IQR)</td></tr>
            <tr><td>Learning Type</td><td>Non-parametric / Unsupervised</td></tr>
            <tr><td>Training Required</td><td>No (parameter-free)</td></tr>
            <tr><td>Z-Score Threshold</td><td>2.5 (99% confidence)</td></tr>
            <tr><td>IQR Multiplier</td><td>1.5 (Tukey's method)</td></tr>
            <tr><td>Feature Scaling</td><td>StandardScaler (manual z-norm)</td></tr>
            <tr><td>Risk Score Range</td><td>0–100 (normalized, 0=normal)</td></tr>
            <tr><td>Anomaly Categories</td><td>LOW | MEDIUM | HIGH | CRITICAL</td></tr>
            <tr><td>Multivariate Support</td><td>Yes (all features combined)</td></tr>
            <tr><td>Time Complexity</td><td>O(n × m) [n=rows, m=features]</td></tr>
            <tr><td>Space Complexity</td><td>O(m) [single pass]</td></tr>
            <tr><td>Compatible Datasets</td><td>CICIDS2017, NSL-KDD, NetFlow JSON</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

# placeholder to maintain layout and prevent empty area
st.markdown('<div class="section-header">▸ ADDITIONAL DETAILS</div>', unsafe_allow_html=True)
st.markdown("""
<div class="tech-card">
    <div class="tech-card-body">
        Comparative analysis and roadmap information have been omitted from the live UI for brevity.
        See the project documentation or source files for the full context.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── NOTE ON CONTENT ───────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ CONTENT NOTICE</div>', unsafe_allow_html=True)
st.markdown("""
<div class="tech-card">
    <div class="tech-card-body">
        The advantages and limitations sections have been removed from the public interface
        as requested. For full context on strengths/weaknesses, refer to the project
        documentation or source code comments.
    </div>
</div>
""", unsafe_allow_html=True)

# the following sections have been removed per user request; placeholder keeps UI balanced
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">▸ NOTE</div>', unsafe_allow_html=True)
st.markdown("""
<div class="tech-card">
    <div class="tech-card-body">
        Future enhancements and reference details have been intentionally omitted from this page.
        The streamlined interface focuses on core methodology and specs—see the docs for the full write‑up.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── VISUAL INTERPRETATION GUIDE ─────────────────────────────────────────────
st.markdown('<div class="section-header">▸ HOW TO INTERPRET OUTPUT VISUALIZATIONS</div>', unsafe_allow_html=True)

col_v1, col_v2, col_v3 = st.columns(3)

with col_v1:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">📊 DETECT PAGE: Risk Score Histogram</div>
        <div class="tech-card-body">
            <strong>What it shows:</strong> Distribution of risk scores across all uploaded flows.<br><br>
            <strong>Interpretation:</strong><br>
            • <span style="color: #00ff88;">Green peak</span> on left = most flows are normal (LOW risk)<br>
            • <span style="color: #ff3366;">Red tail</span> on right = anomalous flows (HIGH/CRITICAL)<br>
            • <strong>Gap in middle</strong> = good separation between normal/anomalous<br>
            • <strong>Bimodal distribution</strong> = dataset contains both benign and attack traffic<br><br>
            <strong>Action:</strong> If histogram is flat (no clear separation), adjust Z-score threshold or IQR multiplier in src/statistical_analysis.py
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_v2:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">🎯 DETECT PAGE: Threat Gauge (% Anomalous)</div>
        <div class="tech-card-body">
            <strong>What it shows:</strong> Percentage of flows flagged as HIGH or CRITICAL risk.<br><br>
            <strong>Interpretation:</strong><br>
            • <span style="color: #00ff88;">0–5%</span> = clean network (LOW false positives expected)<br>
            • <span style="color: #ffaa00;">5–15%</span> = moderate anomalies (typical production)<br>
            • <span style="color: #ff3366;">15%+</span> = under attack or misconfigured thresholds<br><br>
            <strong>Domain knowledge:</strong> For CICIDS2017, expect ~15–25% anomalies (contains DDoS attacks).<br><br>
            <strong>Action:</strong> Compare against historical baseline. Alert if % suddenly spikes.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_v3:
    st.markdown("""
    <div class="tech-card">
        <div class="tech-card-title">🔬 ANALYTICS PAGE: PCA 2D Scatter</div>
        <div class="tech-card-body">
            <strong>What it shows:</strong> All flows projected onto first 2 principal components.<br><br>
            <strong>Interpretation:</strong><br>
            • <span style="color: #00ff88;">Green cluster</span> in center = normal flows (high density)<br>
            • <span style="color: #ff3366;">Red diamonds</span> far from cluster = anomalies (isolated)<br>
            • <strong>Tight cluster</strong> = homogeneous benign traffic<br>
            • <strong>Scattered points</strong> = high variance (mixed attack types)<br><br>
            <strong>Mathematical:</strong> PCA preserves variance, so anomalies with extreme feature values appear far from origin.<br><br>
            <strong>Action:</strong> Manually inspect outlier points. Click to see feature values.
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