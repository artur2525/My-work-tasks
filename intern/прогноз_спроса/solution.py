import numpy as np

def ltv_error(y_true: np.array, y_pred: np.array) -> float:
    '''метрика штрафующая за недобор'''
    error = -1 * (y_true - y_pred) / y_pred
    error = [0.000000001 if f < 0 else f for f in error]
    return np.mean(error)
