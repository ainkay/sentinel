# 🛡️ SENTINEL IDS: Intelligent Intrusion Detection System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-F7931E)
![Plotly](https://img.shields.io/badge/Plotly-Data%20Visualization-3F4F75)

## 📖 Project Description

SENTINEL is an advanced, Machine Learning-powered Intrusion Detection System (IDS) prototype designed to assist network security analysts and IT administrators in identifying malicious network behavior in real-time. Traditional rule-based security systems frequently fail to detect zero-day attacks and often overwhelm security teams with false positives. SENTINEL addresses this critical vulnerability by employing an unsupervised anomaly detection approach, specifically utilizing the Isolation Forest algorithm. By identifying statistical outliers in network traffic flow data, the system can detect novel threats without requiring labeled training datasets or exhaustive manual rule creation.

The application features a dark-themed, highly responsive Streamlit dashboard tailored to the operational requirements of cybersecurity professionals. Users can easily upload standard network traffic datasets, such as CICIDS2017 or NSL-KDD, and instantly receive actionable threat intelligence. The system translates raw mathematical anomaly scores into an intuitive percentage-based risk metric, distinguishing between normal baseline traffic and potentially critical threats. Furthermore, SENTINEL includes a dedicated analytics lab that provides deep visual insights through 2D PCA anomaly mapping, feature distribution comparisons, and correlation analysis, enabling analysts to investigate exactly why specific traffic was flagged.

While the current prototype effectively demonstrates the core machine learning business logic and provides a polished user interface, it is presently structured as an MVP (Minimum Viable Product). The underlying architecture exhibits several areas requiring significant technical refactoring before production deployment. Current limitations include synchronous machine learning training on the main UI thread, inefficient state management using JSON serialization for large DataFrames, and duplicated frontend styling code. The immediate development roadmap is heavily focused on resolving these technical bottlenecks. Planned improvements include modularizing the Python backend, implementing proper Streamlit caching mechanisms to prevent UI freezing during inference, establishing a centralized theme configuration, and setting up persistent database integration. Ultimately, SENTINEL aims to evolve from a robust proof-of-concept into a highly scalable, real-time network defense tool capable of processing live NetFlow streams and seamlessly integrating with enterprise SIEM environments. By continually refining both the data science pipeline and the software engineering architecture, this application will empower security operation centers to proactively defend against increasingly sophisticated, AI-driven cyber threats across complex digital infrastructures.

---

## 🚀 Key Features

* **Unsupervised Threat Detection:** Uses Scikit-learn's `IsolationForest` to find zero-day anomalies based on statistical deviation rather than known signatures.
* **Instant Intelligence:** Upload network traffic CSVs and get instant threat classification without labeled data.
* **Deep Analytics Lab:** Includes 2D PCA Anomaly Mapping, normal vs. anomalous feature distribution comparisons, and feature-to-anomaly correlation charts.
* **Exportable Reports:** Download full analysis results or strictly flagged threat data as CSV files.

---

## ⚠️ Current Technical State & Known Architectural Flaws

This project is currently in the MVP phase. As a proof-of-concept, the UI and business logic function successfully, but the codebase contains several technical debts that are documented here for future refactoring:

1. **State Management Inefficiencies:** The app currently moves Pandas DataFrames between pages by serializing them to JSON and back (`result_df.to_json()`). This is highly memory-inefficient and will crash with large network traffic logs. 
2. **Synchronous ML Execution:** The `IsolationForest` model is fit directly on the main UI thread without caching (`@st.cache_data`). This causes the interface to freeze during large dataset processing.
3. **DRY (Don't Repeat Yourself) Violations:** CSS styling, page configurations, and the random data generation script are copy-pasted across multiple Python files (`app.py`, `1_detect.py`, `2_analytics.py`).
4. **Data Leakage Risk:** Missing values are currently imputed using the median of the *entire* uploaded batch, rather than fitting an imputer on a historically "normal" training baseline and transforming the live data.
5. **UI Component Hacks:** Top navigation is simulated using customized Streamlit buttons and `st.switch_page()`, causing minor re-render flickering, rather than using Streamlit's native multi-page navigation API.

---

## 🗺️ Upcoming Sprints & Refactoring Roadmap

### Phase 1: Code Architecture & Optimization (Immediate)
* Refactor all inline HTML/CSS into a centralized `style.css` or the `core/theme.py` file.
* Update Streamlit Session State to hold native Python objects (DataFrames) directly to avoid JSON overhead.
* Wrap all ML training and inference functions in `@st.cache_data` to prevent UI freezing on re-runs.
* Move data generation and preprocessing logic into modularized scripts (e.g., `scripts/data_processing.py`).

### Phase 2: ML Pipeline & Feature Expansion
* Fix the data imputation leakage by properly separating fit/transform stages for scalers and imputers.
* Integrate Random Forest/XGBoost to allow for **Multi-class attack classification** (identifying DDoS, Port Scans, etc.).
* Implement target/frequency encoding to properly handle categorical features like IP Addresses and Protocols.

### Phase 3: Production Readiness
* Direct PCAP/NetFlow streaming support for true real-time analysis.
* Webhook APIs to push alerts directly to SIEM platforms like Splunk or Elastic Security.

---

## 📁 Project Structure

```text
Network-Traffic-Anomaly-Detection-system/
├── app.py                  # Main entry point & Landing Page
├── pages/
│   ├── 1_detect.py         # Detection Engine (File upload, ML inference, Metrics)
│   ├── 2_analytics.py      # Analytics Lab (PCA, Histograms, Correlations)
│   └── 3_model.py          # Model Intelligence (Algorithm specs, limitations, roadmap)
├── core/                   # Core business logic, UI themes, and state management
├── scripts/                # Data processing and training scripts
├── notebooks/              # Jupyter notebooks for exploratory data analysis
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
