"""
Data Cleaning Module
Handles data loading, validation, missing value treatment, and duplicate removal.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, List


def load_data(filepath: str) -> pd.DataFrame:
    """Load CSV data and perform basic validation."""
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    return df


def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
    """Remove duplicate rows."""
    before = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep='first')
    after = len(df_clean)
    duplicates_removed = before - after
    print(f"Duplicates removed: {duplicates_removed}")
    return df_clean


def detect_missing_values(df: pd.DataFrame) -> Dict:
    """Detect and report missing values."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    result = {
        'columns_with_missing': missing[missing > 0].index.tolist(),
        'missing_counts': missing[missing > 0].to_dict(),
        'missing_percentages': missing_pct[missing_pct > 0].to_dict()
    }
    return result


def handle_missing_values(df: pd.DataFrame, strategy: str = 'median', 
                         numeric_cols: List[str] = None) -> pd.DataFrame:
    """
    Handle missing values in numeric columns.
    
    Parameters:
    - strategy: 'median', 'mean', or 'drop'
    - numeric_cols: List of columns to impute. If None, auto-detect numeric.
    """
    df_clean = df.copy()
    
    if numeric_cols is None:
        numeric_cols = df_clean.select_dtypes(include=['number']).columns.tolist()
    
    if strategy == 'median':
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                df_clean[col].fillna(df_clean[col].median(), inplace=True)
    elif strategy == 'mean':
        for col in numeric_cols:
            if df_clean[col].isnull().any():
                df_clean[col].fillna(df_clean[col].mean(), inplace=True)
    elif strategy == 'drop':
        df_clean.dropna(subset=numeric_cols, inplace=True)
    
    return df_clean


def extract_numeric_data(df: pd.DataFrame, handle_inf: bool = True) -> pd.DataFrame:
    """
    Extract numeric columns and handle infinite values.
    """
    numeric_df = df.select_dtypes(include=['number']).copy()
    
    if handle_inf:
        numeric_df = numeric_df.replace([np.inf, -np.inf], np.nan)
    
    numeric_df = numeric_df.dropna(axis=1, how='all')
    numeric_df = numeric_df.fillna(numeric_df.median())
    
    return numeric_df


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics for numeric columns."""
    return df.describe()


def detect_outliers_simple(series: pd.Series, method: str = 'iqr', 
                          threshold: float = 1.5) -> np.ndarray:
    """
    Simple outlier detection using IQR or Z-score (manual).
    
    Returns boolean array where True = outlier.
    """
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        return (series < lower_bound) | (series > upper_bound)
    
    elif method == 'zscore':
        mean = series.mean()
        std = series.std()
        z_scores = np.abs((series - mean) / std)
        return z_scores > threshold
    
    return np.zeros(len(series), dtype=bool)
