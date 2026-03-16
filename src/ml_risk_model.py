"""
Distance-based anomaly scoring and ensemble ML risk aggregation.
"""

from __future__ import annotations

from typing import Dict, Optional

import numpy as np


def _normalize(values: np.ndarray) -> np.ndarray:
    """Normalize values into the [0, 1] range."""
    values = np.asarray(values, dtype=float)
    minimum = np.min(values)
    maximum = np.max(values)
    if np.isclose(maximum, minimum):
        return np.zeros_like(values, dtype=float)
    return (values - minimum) / (maximum - minimum)


def euclidean_distance_score(data: np.ndarray, cluster_centers: np.ndarray) -> np.ndarray:
    """
    Measure deviation as minimum Euclidean distance to any cluster center.

    The input data and cluster centers should be expressed in the same feature
    space, typically the standardized feature space used during clustering.
    """
    matrix = np.asarray(data, dtype=float)
    centers = np.asarray(cluster_centers, dtype=float)

    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if centers.ndim == 1:
        centers = centers.reshape(-1, 1)

    distances = np.linalg.norm(matrix[:, None, :] - centers[None, :, :], axis=2)
    minimum_distance = np.min(distances, axis=1)
    return _normalize(minimum_distance)


def mahalanobis_distance_score(data: np.ndarray) -> np.ndarray:
    """Measure deviation from the global traffic centroid using Mahalanobis distance."""
    matrix = np.asarray(data, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)

    center = np.mean(matrix, axis=0)
    covariance = np.cov(matrix, rowvar=False)

    if np.ndim(covariance) == 0:
        covariance = np.array([[float(covariance)]])

    regularized_covariance = covariance + np.eye(covariance.shape[0]) * 1e-6
    inverse_covariance = np.linalg.pinv(regularized_covariance)
    centered = matrix - center

    distances = np.sqrt(np.einsum("ij,jk,ik->i", centered, inverse_covariance, centered))
    return _normalize(distances)


def compute_ml_risk_score(
    statistical_risk_score: np.ndarray,
    isolation_forest_score: np.ndarray,
    cluster_rarity_score: np.ndarray,
    distance_deviation_score: np.ndarray,
    weights: Optional[Dict[str, float]] = None,
) -> np.ndarray:
    """
    Combine statistical and ML-derived indicators into a final risk score.

    Returns values in the [0, 100] range.
    """
    statistical = np.asarray(statistical_risk_score, dtype=float)
    isolation = np.asarray(isolation_forest_score, dtype=float)
    cluster_rarity = np.asarray(cluster_rarity_score, dtype=float)
    distance = np.asarray(distance_deviation_score, dtype=float)

    if weights is None:
        weights = {
            "statistical": 0.35,
            "isolation_forest": 0.30,
            "cluster_rarity": 0.15,
            "distance_deviation": 0.20,
        }

    total_weight = sum(weights.values())
    normalized_weights = {key: value / total_weight for key, value in weights.items()}

    if np.nanmax(statistical) > 1.0:
        statistical = statistical / 100.0
    else:
        statistical = _normalize(statistical)

    isolation = _normalize(isolation)
    cluster_rarity = _normalize(cluster_rarity)
    distance = _normalize(distance)

    ensemble_score = (
        statistical * normalized_weights["statistical"]
        + isolation * normalized_weights["isolation_forest"]
        + cluster_rarity * normalized_weights["cluster_rarity"]
        + distance * normalized_weights["distance_deviation"]
    )

    return np.clip(ensemble_score * 100.0, 0.0, 100.0)