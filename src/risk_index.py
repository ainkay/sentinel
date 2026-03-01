"""
Risk Index Module
Weighted composite risk scoring from multiple anomaly indicators.
"""

import numpy as np
import pandas as pd
from typing import Dict


def normalize_score(score: np.ndarray, min_val: float = None, 
                   max_val: float = None) -> np.ndarray:
    """
    Normalize scores to [0, 1] range.
    """
    if min_val is None:
        min_val = score.min()
    if max_val is None:
        max_val = score.max()
    
    if max_val == min_val:
        return np.zeros_like(score)
    
    return (score - min_val) / (max_val - min_val)


def compute_weighted_risk_index(indicators: Dict[str, np.ndarray],
                                weights: Dict[str, float] = None) -> np.ndarray:
    """
    Compute weighted composite risk index from multiple indicators.
    
    Parameters:
    - indicators: Dict of indicator_name -> scores (numpy array)
    - weights: Dict of indicator_name -> weight (should sum to 1)
    
    Returns:
    - Composite risk score in [0, 100]
    
    Example:
        indicators = {
            'zscore_anomaly': zscore_scores,
            'iqr_anomaly': iqr_scores,
            'deviation': deviation_scores
        }
        weights = {'zscore_anomaly': 0.4, 'iqr_anomaly': 0.3, 'deviation': 0.3}
        risk = compute_weighted_risk_index(indicators, weights)
    """
    if weights is None:
        # Equal weights
        weights = {k: 1.0 / len(indicators) for k in indicators.keys()}
    
    # Ensure weights sum to 1
    total_weight = sum(weights.values())
    weights = {k: v / total_weight for k, v in weights.items()}
    
    n_samples = len(next(iter(indicators.values())))
    composite_score = np.zeros(n_samples)
    
    for indicator_name, scores in indicators.items():
        normalized = normalize_score(scores, 0, 1)
        weight = weights.get(indicator_name, 0)
        composite_score += normalized * weight
    
    # Scale to 0-100
    return composite_score * 100


def categorize_risk(risk_score: np.ndarray, 
                   thresholds: Dict[str, float] = None) -> np.ndarray:
    """
    Categorize risk scores into risk levels.
    
    Parameters:
    - risk_score: Array of risk scores (0-100)
    - thresholds: Dict with 'low', 'medium', 'high', 'critical' keys
    
    Returns:
    - Array of risk category strings
    """
    if thresholds is None:
        thresholds = {
            'low': 25,
            'medium': 50,
            'high': 75,
            'critical': 100
        }
    
    categories = []
    for score in risk_score:
        if score < thresholds['low']:
            categories.append('LOW')
        elif score < thresholds['medium']:
            categories.append('MEDIUM')
        elif score < thresholds['high']:
            categories.append('HIGH')
        else:
            categories.append('CRITICAL')
    
    return np.array(categories)


def create_risk_dataframe(data: pd.DataFrame, risk_scores: np.ndarray,
                         thresholds: Dict[str, float] = None) -> pd.DataFrame:
    """
    Create result DataFrame with risk columns.
    
    Parameters:
    - data: Original data DataFrame
    - risk_scores: Risk scores (0-100)
    - thresholds: Optional risk thresholds
    
    Returns:
    - DataFrame with appended risk columns
    """
    result = data.copy()
    result['risk_score'] = np.round(risk_scores, 2)
    result['risk_category'] = categorize_risk(risk_scores, thresholds)
    
    # Boolean flag for anomalies (high or critical)
    result['is_anomaly'] = result['risk_category'].isin(['HIGH', 'CRITICAL'])
    
    return result


def anomaly_summary_stats(df: pd.DataFrame, risk_col: str = 'risk_score',
                         category_col: str = 'risk_category') -> Dict:
    """Generate summary statistics about detected anomalies."""
    total = len(df)
    anomalies = (df[category_col].isin(['HIGH', 'CRITICAL'])).sum()
    
    return {
        'total_records': total,
        'anomalies_detected': anomalies,
        'anomaly_percentage': (anomalies / total * 100) if total > 0 else 0,
        'average_risk_score': df[risk_col].mean(),
        'max_risk_score': df[risk_col].max(),
        'min_risk_score': df[risk_col].min(),
        'critical_count': (df[category_col] == 'CRITICAL').sum(),
        'high_count': (df[category_col] == 'HIGH').sum(),
        'medium_count': (df[category_col] == 'MEDIUM').sum(),
        'low_count': (df[category_col] == 'LOW').sum()
    }


def flagged_anomalies(df: pd.DataFrame, risk_col: str = 'risk_score',
                     threshold: float = 50) -> pd.DataFrame:
    """Get anomalous records sorted by risk."""
    return df[df[risk_col] >= threshold].sort_values(risk_col, ascending=False)
