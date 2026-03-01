"""
SENTINEL Source Module
=====================

Reusable data science components for network anomaly detection.

Modules:
--------
- data_cleaning: Data loading, validation, missing value handling
- feature_engineering: Normalization, scaling, preprocessing
- statistical_analysis: Z-score & IQR-based anomaly detection
- risk_index: Weighted composite risk scoring
"""

from . import data_cleaning
from . import feature_engineering
from . import statistical_analysis
from . import risk_index

__version__ = '2.0.0'
__all__ = ['data_cleaning', 'feature_engineering', 'statistical_analysis', 'risk_index']

