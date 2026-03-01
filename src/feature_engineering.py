"""
Feature Engineering Module
Data normalization, scaling, and preprocessing utilities.
"""

import numpy as np
import pandas as pd
from typing import Tuple


class StandardScaler:
    """
    Manual StandardScaler implementation for educational purposes.
    Scales features to have mean=0 and std=1.
    """
    def __init__(self):
        self.mean_ = None
        self.std_ = None
    
    def fit(self, X: np.ndarray) -> 'StandardScaler':
        """Compute mean and std from training data."""
        self.mean_ = np.mean(X, axis=0)
        self.std_ = np.std(X, axis=0)
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """Apply standardization."""
        return (X - self.mean_) / (self.std_ + 1e-8)
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform in one step."""
        return self.fit(X).transform(X)


def scale_features(df: pd.DataFrame, columns: list = None) -> Tuple[pd.DataFrame, dict]:
    """
    Scale numeric features using StandardScaler.
    Returns scaled DataFrame and scaler parameters.
    """
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    df_scaled = df.copy()
    scaler_params = {}
    
    for col in columns:
        mean = df[col].mean()
        std = df[col].std()
        df_scaled[col] = (df[col] - mean) / (std + 1e-8)
        scaler_params[col] = {'mean': mean, 'std': std}
    
    return df_scaled, scaler_params


def normalize_features(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Min-Max normalization to [0, 1] range.
    """
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()
    
    df_norm = df.copy()
    
    for col in columns:
        min_val = df[col].min()
        max_val = df[col].max()
        df_norm[col] = (df[col] - min_val) / (max_val - min_val + 1e-8)
    
    return df_norm


def select_numeric_features(df: pd.DataFrame) -> list:
    """Return list of numeric column names."""
    return df.select_dtypes(include=['number']).columns.tolist()


def remove_constant_features(df: pd.DataFrame) -> pd.DataFrame:
    """Remove columns with zero variance."""
    numeric_cols = select_numeric_features(df)
    for col in numeric_cols:
        if df[col].std() == 0:
            df = df.drop(col, axis=1)
    return df
