from typing import Tuple

import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.metrics import roc_auc_score
import random


def roc_auc_ci(
    classifier: ClassifierMixin,
    X: np.ndarray,
    y: np.ndarray,
    conf: float = 0.95,
    n_bootstraps: int = 10_000,
) -> Tuple[float, float]:
    """Returns confidence bounds of the ROC-AUC"""

    # operation with sampling
    y_res = y
    size = len(y)
    y_pred = classifier.predict_proba(X)[:, 1]

    def bootstrap(y_res: np.ndarray, y_pred: np.ndarray) -> float:
        while True:
            mask = np.random.choice(range(0, size), size=size, replace = True)
            if len(np.unique(y_res[mask])) > 1: break
        return roc_auc_score(y_res[mask], y_pred[mask])
    scores = []
    for _ in range(n_bootstraps):
        score = bootstrap(y_res, y_pred)
        scores.append(score)

    alpha = conf
    lcb, ucb = np.quantile(scores, q=[(1 - alpha)/2, alpha + (1 - alpha)/2])

    return (lcb, ucb)
