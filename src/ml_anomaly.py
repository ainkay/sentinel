"""
Machine learning anomaly detection utilities.

This module provides an Isolation Forest wrapper for unlabeled network flow
analysis while keeping the interface simple for the Streamlit application.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


DataLike = Union[pd.DataFrame, np.ndarray]
ModelBundle = Dict[str, Any]


def _coerce_numeric_matrix(data: DataLike) -> Tuple[np.ndarray, Optional[list[str]]]:
    """Convert supported inputs into a 2D numeric matrix."""
    if isinstance(data, pd.DataFrame):
        numeric_df = data.select_dtypes(include=["number"]).copy()
        if numeric_df.empty:
            raise ValueError("Isolation Forest requires at least one numeric feature.")
        return numeric_df.to_numpy(dtype=float), numeric_df.columns.tolist()

    matrix = np.asarray(data, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if matrix.ndim != 2:
        raise ValueError("Input data must be one- or two-dimensional.")
    return matrix, None


def _transform_data(data: DataLike, model: ModelBundle) -> np.ndarray:
    """Apply the fitted imputer and scaler from a trained model bundle."""
    matrix, _ = _coerce_numeric_matrix(data)
    imputed = model["imputer"].transform(matrix)
    return model["scaler"].transform(imputed)


def _normalize(values: np.ndarray) -> np.ndarray:
    """Normalize scores into the [0, 1] range."""
    values = np.asarray(values, dtype=float)
    minimum = np.min(values)
    maximum = np.max(values)
    if np.isclose(maximum, minimum):
        return np.zeros_like(values, dtype=float)
    return (values - minimum) / (maximum - minimum)


def train_isolation_forest(
    data: DataLike,
    contamination: float = 0.05,
    n_estimators: int = 200,
    random_state: int = 42,
) -> ModelBundle:
    """Fit an Isolation Forest model on numeric traffic features."""
    matrix, feature_names = _coerce_numeric_matrix(data)

    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()

    imputed = imputer.fit_transform(matrix)
    scaled = scaler.fit_transform(imputed)

    model = IsolationForest(
        contamination=contamination,
        n_estimators=n_estimators,
        random_state=random_state,
    )
    model.fit(scaled)

    return {
        "model": model,
        "imputer": imputer,
        "scaler": scaler,
        "feature_names": feature_names,
        "contamination": contamination,
        "n_estimators": n_estimators,
        "random_state": random_state,
    }


def predict_anomalies(data: DataLike, model: Optional[ModelBundle] = None) -> np.ndarray:
    """Predict anomalous records where ``True`` indicates an anomaly."""
    fitted_model = model or train_isolation_forest(data)
    transformed = _transform_data(data, fitted_model)
    predictions = fitted_model["model"].predict(transformed)
    return predictions == -1


def get_anomaly_scores(data: DataLike, model: Optional[ModelBundle] = None) -> np.ndarray:
    """Return normalized anomaly severity scores in the [0, 1] range."""
    fitted_model = model or train_isolation_forest(data)
    transformed = _transform_data(data, fitted_model)

    # Lower score_samples values indicate stronger anomalies, so invert them.
    raw_scores = -fitted_model["model"].score_samples(transformed)
    return _normalize(raw_scores)