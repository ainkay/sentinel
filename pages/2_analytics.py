import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler as SklearnScaler
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import (
    data_cleaning,
    feature_engineering,
    ml_anomaly,
    ml_clustering,
    ml_representation,
    ml_risk_model,
    risk_index,
    statistical_analysis,
)

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


def enrich_with_ml_outputs(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Ensure the analytics view has both statistical and ML-derived outputs."""
    result = dataframe.copy()
    numeric_df = data_cleaning.extract_numeric_data(result, handle_inf=True)

    if numeric_df.empty or numeric_df.shape[1] < 2:
        return result

    if '__risk_pct' not in result.columns:
        scaler = feature_engineering.StandardScaler()
        scaled = scaler.fit_transform(numeric_df.values)
        zscore_scores = statistical_analysis.compute_deviation_scores(scaled)

        iqr_scores = np.zeros(len(numeric_df))
        for col in numeric_df.columns:
            lower, upper = statistical_analysis.iqr_bounds(numeric_df[col], multiplier=1.5)
            distance = np.maximum(0, numeric_df[col].values - upper)
            distance = np.maximum(distance, lower - numeric_df[col].values)
            iqr_scores += np.abs(distance)
        iqr_scores = feature_engineering.StandardScaler().fit_transform(
            iqr_scores.reshape(-1, 1)
        ).flatten()

        indicators = {'zscore': zscore_scores, 'iqr': iqr_scores}
        statistical_risk = risk_index.compute_weighted_risk_index(
            indicators,
            {'zscore': 0.5, 'iqr': 0.5}
        )
        result['__risk_score'] = statistical_risk
        result['__risk_category'] = risk_index.categorize_risk(statistical_risk)
        result['__is_anomaly'] = result['__risk_category'].isin(['HIGH', 'CRITICAL'])
        result['__anomaly_label'] = np.where(result['__is_anomaly'], 'Anomalous', 'Normal')
        result['__anomaly_score'] = statistical_risk / 100.0
        result['__risk_pct'] = statistical_risk
        result['__anomaly_flag'] = np.where(result['__is_anomaly'], -1, 1)
        result['__statistical_risk_score'] = statistical_risk
        result['__statistical_risk_category'] = result['__risk_category']
        result['__statistical_anomaly_score'] = statistical_risk / 100.0

    if '__ml_risk_score' not in result.columns:
        isolation_model = ml_anomaly.train_isolation_forest(numeric_df)
        isolation_scores = ml_anomaly.get_anomaly_scores(numeric_df, model=isolation_model)
        isolation_flags = ml_anomaly.predict_anomalies(numeric_df, model=isolation_model)
        pca_result = ml_representation.run_pca(numeric_df, n_components=2)
        pca_components = pca_result['components']
        kmeans_result = ml_clustering.run_kmeans(numeric_df, k=4)
        dbscan_result = ml_clustering.run_dbscan(numeric_df)

        euclidean_scores = ml_risk_model.euclidean_distance_score(
            kmeans_result['processed_data'],
            kmeans_result['cluster_centers']
        )
        mahalanobis_scores = ml_risk_model.mahalanobis_distance_score(
            kmeans_result['processed_data']
        )
        distance_scores = (euclidean_scores + mahalanobis_scores) / 2.0
        cluster_rarity_scores = np.maximum(
            kmeans_result['rarity_scores'],
            dbscan_result['rarity_scores']
        )
        statistical_risk = result['__risk_pct'].to_numpy(dtype=float)
        ml_risk_scores = ml_risk_model.compute_ml_risk_score(
            statistical_risk_score=statistical_risk,
            isolation_forest_score=isolation_scores,
            cluster_rarity_score=cluster_rarity_scores,
            distance_deviation_score=distance_scores,
        )
        ml_risk_categories = risk_index.categorize_risk(ml_risk_scores)
        ml_flags = np.isin(ml_risk_categories, ['HIGH', 'CRITICAL'])
        result['__iforest_anomaly_score'] = isolation_scores
        result['__iforest_anomaly_pct'] = isolation_scores * 100.0
        result['__iforest_is_anomaly'] = isolation_flags
        result['__iforest_label'] = np.where(isolation_flags, 'Anomalous', 'Normal')
        result['__cluster_label'] = kmeans_result['labels']
        result['__dbscan_label'] = dbscan_result['labels']
        result['__cluster_rarity_score'] = cluster_rarity_scores
        result['__distance_deviation_score'] = distance_scores
        result['__mahalanobis_score'] = mahalanobis_scores
        result['__euclidean_distance_score'] = euclidean_scores
        result['__ml_risk_score'] = ml_risk_scores
        result['__ml_risk_category'] = ml_risk_categories
        result['__ml_is_anomaly'] = ml_flags
        result['__ml_anomaly_label'] = np.where(ml_flags, 'Anomalous', 'Normal')
        result['__pca_1'] = pca_components.iloc[:, 0].values
        result['__pca_2'] = pca_components.iloc[:, 1].values if pca_components.shape[1] > 1 else 0.0
        result['__pca_variance_1'] = pca_result['explained_variance_ratio'][0]
        result['__pca_variance_2'] = (
            pca_result['explained_variance_ratio'][1]
            if len(pca_result['explained_variance_ratio']) > 1
            else 0.0
        )
        stat_flags = result['__risk_pct'].to_numpy(dtype=float) >= 50
        result['__risk_alignment'] = np.where(stat_flags == ml_flags, 'Agreement', 'Disagreement')

    return result

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

    result_df = raw_df.copy()

result_df = enrich_with_ml_outputs(result_df)

# ─── PREP ─────────────────────────────────────────────────────────────────────
numeric_cols = [
    column for column in result_df.columns
    if not column.startswith('__') and pd.api.types.is_numeric_dtype(result_df[column])
]

total = len(result_df)
anomalies_mask = result_df['__anomaly_label'] == 'Anomalous'
anomalies = anomalies_mask.sum()
normal = total - anomalies
anomaly_pct = anomalies / total * 100
ml_anomalies_mask = result_df['__ml_is_anomaly'] if '__ml_is_anomaly' in result_df else anomalies_mask
ml_anomalies = int(ml_anomalies_mask.sum())
agreement_pct = (
    (result_df['__risk_alignment'] == 'Agreement').mean() * 100
    if '__risk_alignment' in result_df.columns and total > 0
    else 0
)

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
    high_risk = (result_df['__ml_risk_score'] > 75).sum() if '__ml_risk_score' in result_df else (result_df['__risk_pct'] > 75).sum()
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">ML High-Risk Flows</div>
        <div class="insight-value" style="color:#ff6b35;">{high_risk}</div>
        <div class="insight-sub">Ensemble risk score &gt; 75%</div>
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
    st.markdown(f"""
    <div class="insight-card">
        <div class="insight-label">Stat vs ML Agreement</div>
        <div class="insight-value" style="color:#00ff88;">{agreement_pct:.0f}%</div>
        <div class="insight-sub">Rows where both layers agree</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── PCA 2D BEHAVIOR MAP ──────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ PCA BEHAVIOR MAP — CLUSTERED TRAFFIC PROJECTION</div>', unsafe_allow_html=True)

if '__pca_1' in result_df.columns and '__pca_2' in result_df.columns:
    fig_pca = px.scatter(
        result_df,
        x='__pca_1',
        y='__pca_2',
        color='__cluster_label',
        size='__ml_risk_score',
        symbol='__ml_anomaly_label',
        color_continuous_scale='Turbo',
        hover_data={
            '__ml_risk_score': ':.2f',
            '__risk_pct': ':.2f',
            '__cluster_rarity_score': ':.2f',
            '__cluster_label': True,
            '__ml_anomaly_label': True,
        }
    )
    fig_pca.update_traces(marker=dict(opacity=0.75, line=dict(width=0)))
    fig_pca.update_layout(
        **PLOTLY_LAYOUT,
        xaxis_title=f"PC1 ({result_df['__pca_variance_1'].iloc[0] * 100:.1f}% variance)",
        yaxis_title=f"PC2 ({result_df['__pca_variance_2'].iloc[0] * 100:.1f}% variance)",
        height=420,
        coloraxis_colorbar=dict(title='Cluster')
    )
    st.plotly_chart(fig_pca, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── STATISTICAL VS ML COMPARISON ─────────────────────────────────────────────
st.markdown('<div class="section-header">▸ STATISTICAL VS ML ANOMALY COMPARISON</div>', unsafe_allow_html=True)

if '__ml_risk_score' in result_df.columns:
    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        fig_compare = go.Figure()
        for state, color in {
            'Agreement': 'rgba(0,255,136,0.7)',
            'Disagreement': 'rgba(255,51,102,0.85)'
        }.items():
            subset = result_df[result_df['__risk_alignment'] == state]
            fig_compare.add_trace(go.Scattergl(
                x=subset['__risk_pct'],
                y=subset['__ml_risk_score'],
                mode='markers',
                name=state,
                marker=dict(color=color, size=6),
                hovertemplate=(
                    'Statistical Risk: %{x:.1f}<br>'
                    'ML Risk: %{y:.1f}<br>'
                    'State: ' + state + '<extra></extra>'
                )
            ))
        fig_compare.add_vline(x=50, line_dash='dash', line_color='rgba(0,245,255,0.35)')
        fig_compare.add_hline(y=50, line_dash='dash', line_color='rgba(255,170,0,0.35)')
        fig_compare.update_layout(
            **PLOTLY_LAYOUT,
            height=320,
            xaxis_title='Statistical Risk Score',
            yaxis_title='ML Ensemble Risk Score'
        )
        st.plotly_chart(fig_compare, use_container_width=True)

    with compare_col2:
        ml_compare = pd.DataFrame({
            'Layer': ['Statistical', 'ML Ensemble', 'Isolation Forest'],
            'High Risk Flows': [
                int((result_df['__risk_pct'] >= 50).sum()),
                int(result_df['__ml_is_anomaly'].sum()),
                int(result_df['__iforest_is_anomaly'].sum()),
            ]
        })
        fig_layer = go.Figure(go.Bar(
            x=ml_compare['Layer'],
            y=ml_compare['High Risk Flows'],
            marker=dict(color=['rgba(0,245,255,0.7)', 'rgba(255,107,53,0.85)', 'rgba(255,51,102,0.8)'])
        ))
        fig_layer.update_layout(
            **PLOTLY_LAYOUT,
            height=320,
            xaxis_title='Detection Layer',
            yaxis_title='Flagged Flows'
        )
        st.plotly_chart(fig_layer, use_container_width=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ─── CLUSTER ANALYSIS ─────────────────────────────────────────────────────────
st.markdown('<div class="section-header">▸ TRAFFIC CLUSTER ANALYSIS</div>', unsafe_allow_html=True)

if '__cluster_label' in result_df.columns:
    cluster_summary = (
        result_df
        .groupby('__cluster_label', as_index=False)
        .agg(
            flow_count=('__cluster_label', 'size'),
            avg_ml_risk=('__ml_risk_score', 'mean'),
            avg_stat_risk=('__risk_pct', 'mean'),
            avg_rarity=('__cluster_rarity_score', 'mean')
        )
        .sort_values('avg_ml_risk', ascending=False)
    )

    cluster_col1, cluster_col2 = st.columns(2)
    with cluster_col1:
        fig_cluster = go.Figure(go.Bar(
            x=cluster_summary['flow_count'],
            y=cluster_summary['__cluster_label'].astype(str),
            orientation='h',
            marker=dict(color=cluster_summary['avg_ml_risk'], colorscale='Turbo'),
            customdata=np.stack(
                [
                    cluster_summary['avg_ml_risk'],
                    cluster_summary['avg_stat_risk'],
                    cluster_summary['avg_rarity']
                ],
                axis=1
            ),
            hovertemplate=(
                'Cluster %{y}<br>'
                'Flows: %{x}<br>'
                'Avg ML Risk: %{customdata[0]:.1f}<br>'
                'Avg Statistical Risk: %{customdata[1]:.1f}<br>'
                'Avg Rarity: %{customdata[2]:.2f}<extra></extra>'
            )
        ))
        fig_cluster.update_layout(
            **PLOTLY_LAYOUT,
            height=340,
            xaxis_title='Flow Count',
            yaxis_title='Cluster'
        )
        st.plotly_chart(fig_cluster, use_container_width=True)

    with cluster_col2:
        dbscan_counts = (
            result_df['__dbscan_label']
            .astype(str)
            .value_counts()
            .rename_axis('label')
            .reset_index(name='count')
        )
        fig_dbscan = go.Figure(go.Bar(
            x=dbscan_counts['label'],
            y=dbscan_counts['count'],
            marker=dict(color='rgba(0,245,255,0.65)')
        ))
        fig_dbscan.update_layout(
            **PLOTLY_LAYOUT,
            height=340,
            xaxis_title='DBSCAN Label (-1 = rare/noise)',
            yaxis_title='Flow Count'
        )
        st.plotly_chart(fig_dbscan, use_container_width=True)

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
            score_column = '__ml_risk_score' if '__ml_risk_score' in result_df.columns else '__anomaly_score'
            s = result_df.loc[c.index, score_column]
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
            xaxis_title='|Correlation with Active Risk Score|'
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

    if '__ml_risk_score' in timeline_df.columns:
        fig_time.add_trace(go.Scatter(
            x=list(range(len(timeline_df))),
            y=timeline_df['__ml_risk_score'] / 100.0,
            mode='lines',
            name='ML Risk',
            line=dict(color='rgba(255,107,53,0.85)', width=1.5)
        ))

    anom_pts_t = timeline_df[timeline_df['__anomaly_label'] == 'Anomalous']
    if len(anom_pts_t) > 0:
        fig_time.add_trace(go.Scatter(
            x=anom_pts_t.index.tolist(),
            y=anom_pts_t['__anomaly_score'],
            mode='markers', name='Anomalous',
            marker=dict(color='rgba(255,51,102,0.9)', size=6, symbol='circle')
        ))

    threshold = timeline_df['__anomaly_score'].quantile(0.95)
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