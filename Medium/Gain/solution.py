from typing import List
import numpy as np

def cumulative_gain(relevance: List[float], k: int) -> float:
    """Score is cumulative gain at k (CG@k)

    Parameters
    ----------
    relevance:  `List[float]`
        Relevance labels (Ranks)
    k : `int`
        Number of elements to be counted

    Returns
    -------
    score : float
    """
    score = np.sum(relevance[:k])
    return score

def discounted_cumulative_gain(relevance: List[float], k: int, method: str = "standard") -> float:
    """Discounted Cumulative Gain
    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    try:
        if method == "standard":
            score = []
            for j, i in enumerate(relevance[:k]):
                score.append(i/np.log2(j + 1+1))
            score = np.sum(score)
        if method == "industry":
            score = []
            for j, i in enumerate(relevance[:k]):
                score.append((2**i - 1)/np.log2(j + 1+1))
            score = np.sum(score)

        return score

    except:
        raise ValueError()

def normalized_dcg(relevance: List[float], k: int, method: str = "standard") -> float:
    """Normalized Discounted Cumulative Gain.

    Parameters
    ----------
    relevance : `List[float]`
        Video relevance list
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values
        `standard` - adds weight to the denominator
        `industry` - adds weights to the numerator and denominator
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    try:
        if method == "standard":
            score = []
            for j, i in enumerate(relevance[:k]):
                score.append((i/np.log2(j + 1 + 1)))
            score_full = []
            for j, i in enumerate(sorted(relevance, reverse=True)[:k]):
                score_full.append((i/np.log2(j + 1 + 1)))
            score = np.sum(score) / np.sum(score_full)
        if method == "industry":
            score = []
            for j, i in enumerate(relevance[:k]):
                score.append(((2**i) - 1) / np.log2(j + 1 + 1))
            score_full = []
            for j, i in enumerate(sorted(relevance, reverse=True)[:k]):
                score_full.append(((2**i) - 1) / np.log2(j + 1 + 1))
            score = np.sum(score) / np.sum(score_full)

        return score
        
    except:
        raise ValueError()

def avg_ndcg(list_relevances: List[List[float]], k: int, method: str = 'standard') -> float:
    """Average nDCG

    Parameters
    ----------
    list_relevances : `List[List[float]]`
        Video relevance matrix for various queries
    k : `int`
        Count relevance to compute
    method : `str`, optional
        Metric implementation method, takes the values 
        `standard` - adds weight to the denominator\
        `industry` - adds weights to the numerator and denominator\
        `raise ValueError` - for any value

    Returns
    -------
    score : `float`
        Metric score
    """
    try:
        scores = []
        if method == "standard":
            for relevance in list_relevances:
                score = []
                for j, i in enumerate(relevance[:k]):
                    score.append((i/np.log2(j + 1 + 1)))
                score_full = []
                for j, i in enumerate(sorted(relevance, reverse=True)[:k]):
                    score_full.append((i/np.log2(j + 1 + 1)))
                score = np.sum(score) / np.sum(score_full)
                scores.append(score)
        if method == "industry":
            for relevance in list_relevances:
                score = []
                for j, i in enumerate(relevance[:k]):
                    score.append(((2**i) - 1) / np.log2(j + 1 + 1))
                score_full = []
                for j, i in enumerate(sorted(relevance, reverse=True)[:k]):
                    score_full.append(((2**i) - 1) / np.log2(j + 1 + 1))
                score = np.sum(score) / np.sum(score_full)
                scores.append(score)

        return np.sum(np.array(scores)/len(list_relevances))
        
    except:
        raise ValueError()
