from typing import List
import numpy as np



def recall_at_k(labels: List[int], scores: List[float], k=5) -> float:
    '''top k metrics'''

    sorted_predictions = sorted(
        zip(scores, labels), key=lambda x: x[0], reverse=True)
    labels = np.array([x[1] for x in sorted_predictions])
    tp = len(labels[:k][labels[:k] == 1])
    fn = len(labels[k:][labels[k:] == 1])
    df = tp / (tp + fn)

    return df


def precision_at_k(labels: List[int], scores: List[float], k=5) -> float:
    '''top k metrics'''
    sorted_predictions = sorted(
        zip(scores, labels), key=lambda x: x[0], reverse=True)
    labels = np.array([x[1] for x in sorted_predictions])
    tp = len(labels[:k][labels[:k] == 1])
    fp = len(labels[:k][labels[:k] == 0])
    df = tp / (tp + fp)

    return df


def specificity_at_k(labels: List[int], scores: List[float], k=5) -> float:
    '''top k metrics'''
    sorted_predictions = sorted(
        zip(scores, labels), key=lambda x: x[0], reverse=True)
    labels = np.array([x[1] for x in sorted_predictions])
    tn = len(labels[k:][labels[k:] == 0])
    fp = len(labels[:k][labels[:k] == 0])
    if tn + fp == 0:
        return 0
    
    df = tn / (tn + fp)

    return df


def f1_at_k(labels: List[int], scores: List[float], k=5) -> float:
    '''top k metrics'''
    pres = precision_at_k(labels, scores, k)
    rec = recall_at_k(labels, scores, k)
    if pres + rec == 0:
        return 0
    
    df = (2 * pres * rec) / (pres + rec)

    return df