from typing import Tuple, Dict, List
import numpy as np


def bootstrap(y_true: np.ndarray, y_prob: np.ndarray):
    size = len(y_prob) + 1
    while True:
        mask = np.random.choice(range(0, size),
                                size=size, replace=True)
        if len(np.unique(mask)) > 1:
            break
    threes = []
    indec = np.insert(y_prob, 0, 1)
    for i in mask:
        y_proba = np.flip(np.cumsum(y_prob == indec[-i]))
        recall, precision, specificity = metrics(y_true, y_proba)
        threes.append([indec[i], recall, precision, specificity])

    threes = np.nan_to_num(threes)
    return threes


def metrics(y_true_, y_proba_):

    tp = np.sum((y_true_ == 1) & (y_proba_ == 1))
    fp = np.sum((y_true_ == 0) & (y_proba_ == 1))
    tn = np.sum((y_true_ == 0) & (y_proba_ == 0))
    fn = np.sum((y_true_ == 1) & (y_proba_ == 0))
    specificity = tn / (tn + fp)
    recall = tp / (tp + fn)
    precision = tp / (tp + fp)
    return recall, precision, specificity


def create_curve(y_true, y_prob):

    threes = []
    indec = np.insert(y_prob, 0, 1)
    size = len(y_prob) + 1
    for i in range(0, size):
        y_proba = np.flip(np.cumsum(y_prob == indec[-i]))
        recall, precision, specificity = metrics(y_true, y_proba)
        threes.append([indec[i], recall, precision, specificity])

    threes = np.nan_to_num(threes)
    
    return threes


def pr_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    min_precision: float,
) -> Tuple[float, float]:
    """Returns threshold and recall (from Precision-Recall Curve)"""

    curve = create_curve(y_true, y_prob)

    curve = curve[curve[:, 2] >= min_precision]
    curve = curve[np.where(curve[:, 1] == max(curve[:, 1]))]
    curve = curve[np.where(curve[:, 0] == max(curve[:, 0]))]

    threshold_proba, max_recall = curve[0][0], curve[0][1]

    return threshold_proba, max_recall

# x = threshold, y = recall, h = precision, z = specificity


def sr_threshold(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    min_specificity: float,
) -> Tuple[float, float]:
    """Returns threshold and recall (from Specificity-Recall Curve)"""

    curve = create_curve(y_true, y_prob)

    curve = curve[curve[:, 3] >= min_specificity]
    curve = curve[np.where(curve[:, 1] == max(curve[:, 1]))]
    curve = curve[np.where(curve[:, 0] == max(curve[:, 0]))]

    threshold_proba, max_recall = curve[0][0], curve[0][1]

    return threshold_proba, max_recall


def pr_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    conf: float = 0.95,
    n_bootstrap: int = 10_000,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Returns Precision-Recall curve and it's (LCB, UCB)"""

    prec = []
    alpha = conf
    size = len(y_prob) + 1
    curve = create_curve(y_true, y_prob)
    scores_pr = np.flip(curve[:, 2])
    scores_rec = curve[:, 1]
    
    for _ in range(n_bootstrap):
        curve = bootstrap(y_true, y_prob)
        prec.append(curve[:, 2])

    precision_lcb = []
    precision_ucb = []

    for i in range(size):

        precision_lcb.append(np.quantile(np.array(prec)[:, i],
                                         q=(1 - alpha/2)))
        precision_ucb.append(np.quantile(np.array(prec)[:, i],
                                         q=(alpha + (1 - alpha)/2)))

    return scores_rec, scores_pr, np.array(precision_lcb), np.array(precision_ucb)
# x = threshold, y = recall, h = precision, z = specificity


def sr_curve(
    y_true: np.ndarray,
    y_prob: np.ndarray,
    conf: float = 0.95,
    n_bootstrap: int = 10_000,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Returns Specificity-Recall curve and it's (LCB, UCB)"""

    prec = []
    alpha = conf
    size = len(y_prob) + 1
    curve = create_curve(y_true, y_prob)
    scores_spec = curve[:, 3]
    scores_rec = curve[:, 1]

    for _ in range(n_bootstrap):
        curve = bootstrap(y_true, y_prob)
        prec.append(curve[:, 3])

    specificity_lcb = []
    specificity_ucb = []

    for i in range(size):

        specificity_lcb.append(np.quantile(np.array(prec)[:, i],
                                           q=(1 - alpha/2)))

        specificity_ucb.append(np.quantile(np.array(prec)[:, i],
                                           q=(alpha + (1 - alpha)/2)))

    return scores_rec, scores_spec, np.array(specificity_lcb), np.array(specificity_ucb)