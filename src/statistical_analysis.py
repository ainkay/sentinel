"""
Statistical Analysis Module
Z-score and IQR-based anomaly detection methods.
"""

import numpy as np
import pandas as pd
from typing import Tuple


def compute_zscore(series: pd.Series) -> np.ndarray:
    """
    Compute Z-scores manually without sklearn.
    Z = (X - mean) / std
    """
    mean = series.mean()
    std = series.std()
    z_scores = (series - mean) / (std + 1e-8)
    return z_scores.values


def zscore_anomaly_detection(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """
    Z-score based anomaly detection.
    
    Points with |Z| > threshold are marked as anomalies.
    Typically, threshold=3 means ~0.3% of data (3-sigma rule).
    
    Parameters:
    - data: 1D or 2D array
    - threshold: Z-score threshold (default 3)
    
    Returns:
    - Boolean array where True = anomaly
    """
    if data.ndim == 1:
        z_scores = np.abs(compute_zscore(pd.Series(data)))
        return z_scores > threshold
    else:
        # For 2D data, compute per-feature anomalies then aggregate
        anomalies = np.zeros(data.shape[0], dtype=bool)
        for col_idx in range(data.shape[1]):
            col_data = data[:, col_idx]
            mean = np.mean(col_data)
            std = np.std(col_data)
            z = np.abs((col_data - mean) / (std + 1e-8))
            anomalies |= (z > threshold)
        return anomalies


def compute_iqr(series: pd.Series) -> Tuple[float, float, float]:
    """
    Compute Interquartile Range (IQR).
    
    Returns:
    - Q1 (25th percentile)
    - Q3 (75th percentile)
    - IQR = Q3 - Q1
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1, Q3, IQR


def iqr_anomaly_detection(series: pd.Series, multiplier: float = 1.5) -> np.ndarray:
    """
    IQR-based outlier detection.
    
    Outliers are points outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR].
    
    Parameters:
    - series: Pandas Series
    - multiplier: IQR multiplier (default 1.5 for standard boxplot)
    
    Returns:
    - Boolean array where True = outlier
    """
    Q1, Q3, IQR = compute_iqr(series)
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    return (series < lower_bound) | (series > upper_bound)


def iqr_bounds(series: pd.Series, multiplier: float = 1.5) -> Tuple[float, float]:
    """Get IQR bounds for a series."""
    Q1, Q3, IQR = compute_iqr(series)
    lower = Q1 - multiplier * IQR
    upper = Q3 + multiplier * IQR
    return lower, upper


def multivariate_zscore_detection(data: np.ndarray, threshold: float = 3.0) -> np.ndarray:
    """
    Multivariate Z-score anomaly detection.
    Flags rows where ANY feature has |Z| > threshold.
    
    Parameters:
    - data: 2D array (n_samples, n_features)
    - threshold: Z-score threshold
    
    Returns:
    - Boolean array of shape (n_samples,) where True = anomaly
    """
    anomalies = np.zeros(data.shape[0], dtype=bool)
    
    for j in range(data.shape[1]):
        col = data[:, j]
        mean = np.mean(col)
        std = np.std(col)
        z_scores = np.abs((col - mean) / (std + 1e-8))
        anomalies |= (z_scores > threshold)
    
    return anomalies


def multivariate_iqr_detection(df: pd.DataFrame, multiplier: float = 1.5) -> np.ndarray:
    """
    Multivariate IQR anomaly detection.
    Flags rows where ANY feature is outside IQR bounds.
    
    Parameters:
    - df: Pandas DataFrame with numeric columns
    - multiplier: IQR multiplier
    
    Returns:
    - Boolean array where True = anomaly
    """
    anomalies = np.zeros(len(df), dtype=bool)
    
    for col in df.columns:
        lower, upper = iqr_bounds(df[col], multiplier)
        anomalies |= (df[col] < lower) | (df[col] > upper)
    
    return anomalies


def compute_deviation_scores(data: np.ndarray) -> np.ndarray:
    """
    Compute deviation scores for each point.
    Score = sum of absolute Z-scores across features.
    Higher score = more anomalous.
    
    Parameters:
    - data: 2D array (n_samples, n_features)
    
    Returns:
    - 1D array of deviation scores
    """
    scores = np.zeros(data.shape[0])
    
    for j in range(data.shape[1]):
        col = data[:, j]
        mean = np.mean(col)
        std = np.std(col)
        z_scores = np.abs((col - mean) / (std + 1e-8))
        scores += z_scores
    
    return scores / data.shape[1]  # Average deviation across features


def statistical_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generate statistical summary for numeric data."""
    return df.describe().T
