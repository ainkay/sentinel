# SENTINEL Anomaly Detection System - Restructured for Academic Sprint

## Project Overview

SENTINEL is a Streamlit-based network intrusion detection system that combines **statistical anomaly detection** with an intuitive web interface. This restructuring aligns the codebase with **Data Science academic best practices** while maintaining the original UI design.

---

## Architecture

### New Folder Structure

```
sentinel/
├── app.py                          # Main Streamlit app (landing page)
├── pages/
│   ├── 1_detect.py                # Detection interface
│   ├── 2_analytics.py             # Analytics & visualization
│   └── 3_model.py                 # Model documentation
├── src/                           # ← NEW: Core data science modules
│   ├── __init__.py
│   ├── data_cleaning.py           # Data loading, validation, missing values
│   ├── feature_engineering.py     # Scaling, normalization, preprocessing
│   ├── statistical_analysis.py    # Z-score, IQR, outlier detection
│   └── risk_index.py              # Weighted composite risk scoring
├── notebooks/                     # ← NEW: Jupyter notebooks for learning
│   ├── 01_python_fundamentals.ipynb
│   ├── 02_numpy_pandas.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_visualization.ipynb
│   ├── 05_outlier_detection.ipynb
│   └── 06_risk_index.ipynb
├── requirements.txt
└── README.md
```

---

## Core Modules (src/)

### 1. `data_cleaning.py`
Reusable functions for data preparation:
- `load_data()` - Load CSV files
- `detect_missing_values()` - Identify missing data
- `handle_missing_values()` - Impute missing data (median/mean/drop)
- `remove_duplicates()` - Remove duplicate records
- `extract_numeric_data()` - Extract numeric columns, handle inf
- `get_summary_statistics()` - Compute descriptive stats
- `detect_outliers_simple()` - Basic IQR/Z-score outlier detection

### 2. `feature_engineering.py`
Data preprocessing and feature transformation:
- `StandardScaler` - Manual implementation (educational)
- `scale_features()` - Standardize to mean=0, std=1
- `normalize_features()` - Min-Max normalization to [0,1]
- `select_numeric_features()` - Identify numeric columns
- `remove_constant_features()` - Remove zero-variance columns

### 3. `statistical_analysis.py`
**Statistical anomaly detection methods** (no sklearn):
- `compute_zscore()` - Manual Z-score computation
- `zscore_anomaly_detection()` - Flag points with |Z| > threshold
- `compute_iqr()` - Compute Q1, Q3, IQR
- `iqr_anomaly_detection()` - Flag points outside [Q1-1.5×IQR, Q3+1.5×IQR]
- `multivariate_zscore_detection()` - Multi-feature Z-score detection
- `multivariate_iqr_detection()` - Multi-feature IQR detection
- `compute_deviation_scores()` - Average absolute Z-scores
- `statistical_summary()` - Generate comparison statistics

### 4. `risk_index.py`
**Weighted composite risk scoring**:
- `normalize_score()` - Min-Max normalize scores to [0,1]
- `compute_weighted_risk_index()` - Combine multiple indicators
  - Combines Z-score and IQR methods
  - Returns scores 0-100
- `categorize_risk()` - Classify into LOW/MEDIUM/HIGH/CRITICAL
- `create_risk_dataframe()` - Add risk columns to results
- `anomaly_summary_stats()` - Generate statistics summary
- `flagged_anomalies()` - Extract high-risk records

---

## Anomaly Detection Strategy

### Old Approach (Replaced)
- Single `IsolationForest` model
- Black-box predictions
- Less interpretable

### New Approach (SENTINEL v2)
**Dual-Method Statistical Detection:**

1. **Z-Score Based Detection** (Distribution-aware)
   - Formula: Z = (X - mean) / std
   - Threshold: |Z| > 2.5 (98% of normal data)
   - Good for normally distributed data
   - Sensitive to extreme values

2. **IQR Based Detection** (Robust method)
   - Formula: Outliers outside [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
   - Advantage: Robust to extreme outliers
   - Good for skewed distributions
   - Doesn't assume normality

3. **Weighted Risk Index** (Combined scoring)
   - Combines both methods: Risk = 0.5×Z + 0.5×IQR (adjustable)
   - Returns single score 0-100
   - Easy interpretation: 75+ = CRITICAL

### Why This Approach?
✅ **Transparent** - Understand exactly why something is flagged
✅ **Robust** - Redundant detection reduces false positives
✅ **No ML overhead** - Fast, no model training required
✅ **Educational** - Learn statistical foundations
✅ **Customizable** - Adjust weights for your threat model

---

## Streamlit Pages Refactored

### pages/1_detect.py
**Changes:**
- ✅ Removed direct `IsolationForest` logic
- ✅ Imports data/statistical functions from `src/`
- ✅ Uses new risk index computation
- ✅ Keeps original UI/CSS intact

**Flow:**
```python
# Upload/demo data → Extract numeric → Normalize → Compute anomalies → Risk scoring → Display
```

### pages/2_analytics.py
**Changes:**
- ✅ Removed sklearn `StandardScaler` dependency (uses `src.feature_engineering`)
- ✅ Demo data generation uses new statistical methods
- ✅ PCA still available (from sklearn) for visualization
- ✅ All charts/layout unchanged

---

## Jupyter Notebooks (Learning Resources)

### 01_python_fundamentals.ipynb
Learn Python basics:
- Variables, data types, operators
- Conditionals (if/elif/else)
- Loops (for, while)
- Functions with defaults
- List comprehensions
- Dictionaries

### 02_numpy_pandas.ipynb
Master numerical computing:
- NumPy array creation and operations
- Vectorization vs loops
- Pandas DataFrame creation and manipulation
- Series indexing and filtering
- Integration of NumPy + Pandas

### 03_data_cleaning.ipynb
Prepare real data:
- Missing value detection/handling
- Duplicate removal
- Handling infinite values
- Summary statistics
- Data quality reporting
- **Imports and uses `src.data_cleaning` functions**

### 04_visualization.ipynb
Visualize patterns:
- Histograms for distribution comparison
- Boxplots for quartile analysis
- Scatter plots for relationships
- Time series plotting
- Correlation heatmaps
- Cumulative distribution functions

### 05_outlier_detection.ipynb
Learn statistical detection:
- Z-score computation (manual)
- IQR calculation (manual)
- Single-feature anomaly detection
- Multivariate detection
- Method comparison
- **Imports and uses `src.statistical_analysis` functions**

### 06_risk_index.ipynb
Combine indicators:
- Individual score computation
- Weighted combination
- Risk categorization
- Summary statistics
- Detection performance metrics
- **Imports and uses `src.risk_index` functions**

---

## Backward Compatibility

### What's Preserved
✅ **UI/UX** - Original design, layout, CSS, colors
✅ **Functionality** - All detection features working
✅ **Outputs** - Same CSV exports, same visualizations
✅ **Session state** - Data persistence across pages

### What's Changed
- Detection algorithm (IsolationForest → Statistical methods)
- Result score ranges (now 0-100 normalized)
- Backend architecture (modular `src/` imports)
- Dependency tree (fewer sklearn imports)

### Verification
- Run `streamlit run app.py` to verify UI works
- Upload sample data to test detection
- Compare old/new outputs for feature consistency

---

## Using the Modules

### In Streamlit Pages

```python
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import data_cleaning, feature_engineering, statistical_analysis, risk_index

# Load data
df = data_cleaning.extract_numeric_data(raw_df)

# Detect anomalies
zscore_results = statistical_analysis.multivariate_zscore_detection(scaled_data, threshold=2.5)
iqr_results = statistical_analysis.multivariate_iqr_detection(df, multiplier=1.5)

# Compute risk
indicators = {'zscore': zscore_scores, 'iqr': iqr_scores}
risk = risk_index.compute_weighted_risk_index(indicators, weights)
```

### In Jupyter Notebooks

```python
import sys
sys.path.insert(0, '../')  # Go up one directory to sentinel/

from src import statistical_analysis, risk_index

# Use functions directly for learning
z_scores = statistical_analysis.compute_zscore(data_series)
anomalies = statistical_analysis.iqr_anomaly_detection(data_series, multiplier=1.5)
```

---

## Configuration & Customization

### Adjust Detection Sensitivity

**In src/statistical_analysis.py:**
```python
# Z-score threshold (higher = less sensitivity)
threshold = 3.0  # Strict (0.3% of data)
threshold = 2.5  # Default (1.2% of data)
threshold = 2.0  # Lenient (4.6% of data)
```

**In src/statistical_analysis.py:**
```python
# IQR multiplier (higher = less sensitivity)
multiplier = 1.5  # Standard (boxplot default)
multiplier = 2.0  # More lenient
multiplier = 1.0  # Strict
```

### Adjust Risk Weights

**In pages/1_detect.py:**
```python
weights = {
    'zscore': 0.5,  # Change to 0.7 for distribution sensitivity
    'iqr': 0.5      # Change to 0.3 for robustness
}
```

---

## Requirements

```
streamlit>=1.0.0
pandas>=1.3.0
numpy>=1.20.0
plotly>=5.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
scikit-learn>=0.24.0      # For PCA visualization only
```

Note: Core detection **does NOT require scikit-learn**. It's only used for:
- PCA visualization in analytics page
- Optional Isolation Forest enhancement

---

## Testing the Restructuring

### 1. Verify imports work
```bash
python -c "from src import data_cleaning; print('✓ Imports working')"
```

### 2. Test Streamlit app
```bash
streamlit run app.py
```

### 3. Run Jupyter notebooks
```bash
jupyter notebook notebooks/01_python_fundamentals.ipynb
```

### 4. Check detection quality
- Upload sample data to 1_detect.py
- Compare old vs new results
- Verify F1-score metrics

---

## Academic Benefits

### For Students
- **Learning by doing**: Notebooks teach progressively
- **Code reuse**: Import src modules in notebooks
- **Transparency**: Understand every detection step
- **Best practices**: Professional module organization

### For Instructors
- **Curriculum integration**: Each notebook is a lesson
- **Assessment ready**: Students can modify/extend code
- **Production-ready**: Real use case (IDS)
- **Scalable**: Easy to add new detection methods

### For Research
- **Benchmarking**: Compare against other methods
- **Customization**: Adjust weights/thresholds
- **Ablation studies**: Test each component
- **Publication ready**: Clean, documented code

---

## File-by-File Summary

| File | Type | Purpose | Status |
|------|------|---------|--------|
| `app.py` | Streamlit | Landing page | ✅ Unchanged |
| `pages/1_detect.py` | Streamlit | Detection UI | ✅ Refactored |
| `pages/2_analytics.py` | Streamlit | Analytics visualizations | ✅ Refactored |
| `pages/3_model.py` | Streamlit | Model info | ✅ Unchanged |
| `src/data_cleaning.py` | Module | Data preparation | ✅ NEW |
| `src/feature_engineering.py` | Module | Preprocessing | ✅ NEW |
| `src/statistical_analysis.py` | Module | Anomaly detection | ✅ NEW |
| `src/risk_index.py` | Module | Risk scoring | ✅ NEW |
| `notebooks/*.ipynb` | Jupyter | Learning materials | ✅ NEW (6 notebooks) |

---

## Next Steps

### To enhance further:
1. Add database storage for results
2. Implement confidence intervals
3. Add model explainability (SHAP)
4. Create ensemble methods
5. Add real-time streaming support
6. Develop comparison dashboard

### To extend learning:
1. Add more statistical methods (Mahalanobis distance)
2. Implement clustering-based detection (DBSCAN)
3. Add time-series specific methods
4. Create feature importance analysis
5. Develop interactive threshold tuning

---

## References

- **Z-Score**: σ = 1 (68%), 2σ = 95%, 3σ = 99.7%
- **IQR Method**: Standard boxplot definition (Tukey, 1977)
- **Risk Scoring**: Weighted ensemble approach
- **Network Anomalies**: CICIDS2017, NSL-KDD datasets compatible

---

## Support & Questions

For questions about:
- **Architecture**: See this README and src/ docstrings
- **Learning**: Work through notebooks in order
- **Implementation**: Check Streamlit pages for examples
- **Customization**: Modify src/ function parameters

---

**SENTINEL v2.0** - Built for understanding, designed for production.

Last Updated: March 2026
Status: ✅ Production Ready for Academic Use
