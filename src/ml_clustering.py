"""
Behavioral clustering utilities for network traffic analysis.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


DataLike = Union[pd.DataFrame, np.ndarray]


def _coerce_numeric_matrix(data: DataLike) -> Tuple[np.ndarray, Optional[list[str]]]:
    """Convert supported input types into a numeric matrix."""
    if isinstance(data, pd.DataFrame):
        numeric_df = data.select_dtypes(include=["number"]).copy()
        if numeric_df.empty:
            raise ValueError("Clustering requires numeric traffic features.")
        return numeric_df.to_numpy(dtype=float), numeric_df.columns.tolist()

    matrix = np.asarray(data, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if matrix.ndim != 2:
        raise ValueError("Input data must be one- or two-dimensional.")
    return matrix, None


def _prepare_matrix(data: DataLike) -> Tuple[np.ndarray, SimpleImputer, StandardScaler, Optional[list[str]]]:
    """Impute and scale numeric input before clustering."""
    matrix, feature_names = _coerce_numeric_matrix(data)
    imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    imputed = imputer.fit_transform(matrix)
    scaled = scaler.fit_transform(imputed)
    return scaled, imputer, scaler, feature_names


def _normalize(values: np.ndarray) -> np.ndarray:
    """Normalize values into the [0, 1] range."""
    minimum = np.min(values)
    maximum = np.max(values)
    if np.isclose(maximum, minimum):
        return np.zeros_like(values, dtype=float)
    return (values - minimum) / (maximum - minimum)


def _frequency_rarity(labels: np.ndarray) -> np.ndarray:
    """Convert cluster frequencies into rarity scores where higher is rarer."""
    labels_series = pd.Series(labels)
    counts = labels_series.value_counts()

    if counts.empty:
        return np.zeros(len(labels), dtype=float)

    non_noise_counts = counts[counts.index != -1]
    reference_size = non_noise_counts.max() if not non_noise_counts.empty else counts.max()
    rarity = np.zeros(len(labels), dtype=float)

    for index, label in enumerate(labels):
        if label == -1:
            rarity[index] = 1.0
        else:
            rarity[index] = 1.0 - (counts[label] / max(reference_size, 1))

    return _normalize(rarity)


def run_kmeans(data: DataLike, k: int = 4) -> Dict[str, Any]:
    """Cluster traffic behavior using K-Means and return rarity metadata."""
    scaled, imputer, scaler, feature_names = _prepare_matrix(data)
    cluster_count = max(2, min(int(k), len(scaled)))

    model = KMeans(n_clusters=cluster_count, n_init=10, random_state=42)
    labels = model.fit_predict(scaled)
    centers = model.cluster_centers_
    assigned_centers = centers[labels]
    distances = np.linalg.norm(scaled - assigned_centers, axis=1)

    return {
        "labels": labels,
        "cluster_centers": centers,
        "distances": _normalize(distances),
        "rarity_scores": _frequency_rarity(labels),
        "model": model,
        "processed_data": scaled,
        "imputer": imputer,
        "scaler": scaler,
        "feature_names": feature_names,
    }


def run_dbscan(data: DataLike, eps: float = 0.8, min_samples: int = 10) -> Dict[str, Any]:
    """Cluster traffic behavior using DBSCAN to surface sparse regions."""
    scaled, imputer, scaler, feature_names = _prepare_matrix(data)
    model = DBSCAN(eps=eps, min_samples=min_samples)
    labels = model.fit_predict(scaled)

    return {
        "labels": labels,
        "rarity_scores": _frequency_rarity(labels),
        "model": model,
        "processed_data": scaled,
        "imputer": imputer,
        "scaler": scaler,
        "feature_names": feature_names,
    }