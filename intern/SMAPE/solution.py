import numpy as np


def smape(y_true: np.array, y_pred: np.array) -> float:
    ''' Change metric for corner case'''
    return  np.mean(2 * np.abs(y_true - y_pred) / 
            (np.where(np.abs(y_true) + np.abs(y_pred) == 0, 1, np.abs(y_true) + np.abs(y_pred))))
