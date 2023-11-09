from __future__ import annotations
import numpy as np
from dataclasses import dataclass


def mse(y: np.ndarray) -> float:
    """Compute the mean squared error of a vector."""

    y_pred = np.mean(y)
    mse = np.sum((y - y_pred)**2 / len(y))

    return mse


def weighted_mse(y_left: np.ndarray, y_right: np.ndarray) -> float:
    """Compute the weighted mean squared error of two vectors."""

    if len(y_left) + len(y_right) == 0:
        return 0
    mse_wegh = (mse(y_left) * len(y_left) +
                mse(y_right) * len(y_right)) / (len(y_left) + len(y_right))

    return mse_wegh


def split(X: np.ndarray, y: np.ndarray, feature: int) -> float:
    """Find the best split for a node (one feature)"""

    scores = {}
    for x in np.unique(X[:, feature]):
        scores[x] = weighted_mse(
            y[X[:, feature] <= x], y[X[:, feature] > x])

    best_threshold = [i for i in scores if scores[i] == min(scores.values())]

    return best_threshold[0]


def best_split(X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
    """Find the best split for a few feat"""

    scores = {}
    for i in range(0, X.shape[1]):
        scores[i] = split(X, y, i)

    best_threshold = [i for i in scores if scores[i] == min(scores.values())]

    return best_threshold[0], scores[best_threshold[0]]


@dataclass
class Node:
    """Decision tree node."""
    feature: int = 0
    threshold: float = 0
    n_samples: int = 0
    value: float = 0
    mse: float = 0
    left: Node = None
    right: Node = None
