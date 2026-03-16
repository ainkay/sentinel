"""
Representation learning utilities for network traffic analysis.
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple, Union

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler


DataLike = Union[pd.DataFrame, np.ndarray]


def _coerce_numeric_matrix(data: DataLike) -> Tuple[np.ndarray, Optional[list[str]]]:
    """Convert supported input types into a numeric matrix."""
    if isinstance(data, pd.DataFrame):
        numeric_df = data.select_dtypes(include=["number"]).copy()
        if numeric_df.empty:
            raise ValueError("Representation learning requires numeric features.")
        return numeric_df.to_numpy(dtype=float), numeric_df.columns.tolist()

    matrix = np.asarray(data, dtype=float)
    if matrix.ndim == 1:
        matrix = matrix.reshape(-1, 1)
    if matrix.ndim != 2:
        raise ValueError("Input data must be one- or two-dimensional.")
    return matrix, None


def _prepare_matrix(data: DataLike) -> Tuple[np.ndarray, SimpleImputer, StandardScaler, Optional[list[str]]]:
    """Impute and scale numeric input for downstream ML algorithms."""
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


def run_pca(data: DataLike, n_components: int = 2) -> Dict[str, Any]:
    """Project numeric traffic features into a lower-dimensional PCA space."""
    scaled, imputer, scaler, feature_names = _prepare_matrix(data)
    max_components = max(1, min(n_components, scaled.shape[0], scaled.shape[1]))

    pca = PCA(n_components=max_components, random_state=42)
    components = pca.fit_transform(scaled)
    columns = [f"PC{i + 1}" for i in range(max_components)]

    return {
        "components": pd.DataFrame(components, columns=columns),
        "explained_variance_ratio": pca.explained_variance_ratio_,
        "model": pca,
        "imputer": imputer,
        "scaler": scaler,
        "feature_names": feature_names,
    }


def run_autoencoder(
    data: DataLike,
    encoding_dim: int = 2,
    epochs: int = 20,
    batch_size: int = 32,
    random_state: int = 42,
) -> Dict[str, Any]:
    """
    Learn a compact latent representation.

    TensorFlow is used when available. If it is not installed, the function
    falls back to a PCA-based reconstruction surrogate so the module remains
    importable in lightweight environments.
    """
    scaled, imputer, scaler, feature_names = _prepare_matrix(data)
    latent_dim = max(1, min(encoding_dim, scaled.shape[1]))

    try:
        import tensorflow as tf
        from tensorflow import keras

        tf.keras.utils.set_random_seed(random_state)

        inputs = keras.Input(shape=(scaled.shape[1],))
        encoded = keras.layers.Dense(max(latent_dim * 2, 4), activation="relu")(inputs)
        bottleneck = keras.layers.Dense(latent_dim, activation="linear", name="latent")(encoded)
        decoded = keras.layers.Dense(max(latent_dim * 2, 4), activation="relu")(bottleneck)
        outputs = keras.layers.Dense(scaled.shape[1], activation="linear")(decoded)

        autoencoder = keras.Model(inputs=inputs, outputs=outputs)
        encoder = keras.Model(inputs=inputs, outputs=bottleneck)
        autoencoder.compile(optimizer="adam", loss="mse")
        autoencoder.fit(
            scaled,
            scaled,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            verbose=0,
        )

        latent_features = encoder.predict(scaled, verbose=0)
        reconstructed = autoencoder.predict(scaled, verbose=0)
        reconstruction_error = np.mean(np.square(scaled - reconstructed), axis=1)

        return {
            "latent_features": pd.DataFrame(
                latent_features,
                columns=[f"latent_{index + 1}" for index in range(latent_features.shape[1])],
            ),
            "reconstruction_error": _normalize(reconstruction_error),
            "model": autoencoder,
            "encoder": encoder,
            "imputer": imputer,
            "scaler": scaler,
            "feature_names": feature_names,
            "method": "tensorflow_autoencoder",
        }
    except Exception:
        pca = PCA(n_components=latent_dim, random_state=random_state)
        latent_features = pca.fit_transform(scaled)
        reconstructed = pca.inverse_transform(latent_features)
        reconstruction_error = np.mean(np.square(scaled - reconstructed), axis=1)

        return {
            "latent_features": pd.DataFrame(
                latent_features,
                columns=[f"latent_{index + 1}" for index in range(latent_features.shape[1])],
            ),
            "reconstruction_error": _normalize(reconstruction_error),
            "model": pca,
            "encoder": None,
            "imputer": imputer,
            "scaler": scaler,
            "feature_names": feature_names,
            "method": "pca_fallback",
        }