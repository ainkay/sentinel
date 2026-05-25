# 🛡️ SENTINEL IDS

[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)](https://streamlit.io)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E)](https://scikit-learn.org)
[![Plotly](https://img.shields.io/badge/Plotly-Data%20Visualization-3F4F75)](https://plotly.com)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-sentinel--v1.streamlit.app-brightgreen)](https://sentinel-v1.streamlit.app/)

**A deployed, ML-powered Intrusion Detection System that analyzes network traffic CSVs and flags anomalous behavior — no setup required.**

🔗 **Try it live:** [sentinel-v1.streamlit.app](https://sentinel-v1.streamlit.app/)

---

## 📖 What is SENTINEL?

SENTINEL is a network security tool that lets you upload a CSV of network traffic and instantly receive a full anomaly analysis — complete with threat scores, risk classifications, and visual breakdowns.

Traditional rule-based security systems struggle to detect zero-day attacks and tend to overwhelm analysts with false positives. SENTINEL takes a different approach: it uses unsupervised machine learning (Isolation Forest) to identify statistically unusual traffic patterns without needing any pre-labeled attack data.

The result is a fast, accessible threat analysis tool that works out of the box — useful for security students, researchers, or small teams who want meaningful insight into their network data without enterprise-grade infrastructure.

---

## 🚀 How to Use

1. Visit [sentinel-v1.streamlit.app](https://sentinel-v1.streamlit.app/)
2. Upload a network traffic CSV (e.g. CICIDS2017, NSL-KDD, or your own)
3. Get instant threat classification, risk scores, and visual analytics
4. Export flagged results as a CSV for further investigation

No installation. No configuration. Just upload and analyse.

---

## ✨ Features

- **Unsupervised Threat Detection** — Uses Isolation Forest to detect zero-day anomalies based on statistical deviation, not known signatures
- **Instant Risk Scoring** — Raw anomaly scores are translated into an intuitive 0–100 risk metric, separating normal traffic from potential threats
- **Analytics Lab** — Includes 2D PCA anomaly mapping, normal vs. anomalous feature distribution comparisons, and correlation analysis
- **Ensemble ML Scoring** — Combines four signals (statistical score, Isolation Forest, cluster rarity, distance deviation) into a final risk score
- **Exportable Reports** — Download full analysis results or strictly flagged threat rows as CSV files

---

## 🧠 How It Works

SENTINEL runs a multi-layered ML pipeline on your uploaded traffic data:

| Layer | Method | Purpose |
|---|---|---|
| Anomaly Detection | Isolation Forest | Flags statistical outliers in traffic flow |
| Dimensionality Reduction | PCA | Powers the 2D traffic behavior map |
| Behavioral Clustering | K-Means + DBSCAN | Groups traffic into behavioral regimes |
| Ensemble Scoring | Weighted combination | Final normalized 0–100 risk score |

---

## 🗂️ Project Structure

```
sentinel/
├── app.py                  # Main entry point & landing page
├── pages/
│   ├── 1_detect.py         # Detection engine — file upload, ML inference, metrics
│   ├── 2_analytics.py      # Analytics lab — PCA, histograms, correlations
│   └── 3_model.py          # Model info — algorithm specs and roadmap
├── src/
│   ├── ml_anomaly.py       # Isolation Forest workflow
│   ├── ml_representation.py# PCA and autoencoder representation
│   ├── ml_clustering.py    # K-Means and DBSCAN clustering
│   └── ml_risk_model.py    # Ensemble risk scoring
├── notebooks/              # Jupyter notebooks for EDA and pipeline exploration
├── requirements.txt
└── README.md
```

---

## ⚠️ Current Limitations

SENTINEL is an MVP. The core detection logic and UI work well, but there are known architectural issues being actively worked on:

- **Performance** — ML training runs on the main UI thread, which can cause freezing on large datasets
- **State management** — DataFrames are serialized to JSON between pages, which is memory-inefficient
- **Data leakage risk** — Imputation currently uses the full uploaded batch rather than a clean training baseline

These are documented and prioritized for the next phase of development.

---

## 🗺️ What's Next

**Phase 1 — Architecture cleanup**
- Refactor inline styling into a centralized theme file
- Implement `@st.cache_data` across ML functions to prevent UI freezing
- Fix DataFrame state management to avoid JSON overhead

**Phase 2 — ML improvements**
- Add multi-class attack classification (DDoS, Port Scan, etc.) via Random Forest / XGBoost
- Fix imputation leakage with proper fit/transform separation

**Phase 3 — Real-time capabilities**
- Live traffic capture via Wireshark / PCAP / NetFlow streaming
- Webhook integrations to push alerts to SIEM platforms like Splunk or Elastic Security

---

## 🛠️ Running Locally

```bash
git clone https://github.com/ainkay/sentinel.git
cd sentinel
pip install -r requirements.txt
streamlit run app.py
```

---

## 📄 License

This project is open source. Feel free to fork, use, and build on it.
