"""Solution for Similar Items task"""
from typing import Dict
from typing import List
from typing import Tuple
from itertools import combinations
import numpy as np
from scipy.spatial.distance import cosine


class SimilarItems:
    """Similar items class"""

    @staticmethod
    def similarity(embeddings: Dict[int, np.ndarray]) -> Dict[Tuple[int, int], float]:
        """Calculate pairwise similarities between each item
        in embedding.

        Args:
            embeddings (Dict[int, np.ndarray]): Items embeddings.

        Returns:
            Tuple[List[str], Dict[Tuple[int, int], float]]:
            List of all items + Pairwise similarities dict
            Keys are in form of (i, j) - combinations pairs of item_ids
            with i < j.
            Round each value to 8 decimal places.
        """

        pair_sims = dict(zip(tuple(combinations(embeddings.keys(), 2)),
                             [round(1 - cosine(embeddings[x[0]], embeddings[x[1]]), 8) for x in
                              list(combinations(embeddings.keys(), 2))]))

        return pair_sims

    @staticmethod
    def knn(
        sim: Dict[Tuple[int, int], float], top: int
    ) -> Dict[int, List[Tuple[int, float]]]:
        """Return closest neighbors for each item.

        Args:
            sim (Dict[Tuple[int, int], float]): <similarity> method output.
            top (int): Number of top neighbors to consider.

        Returns:
            Dict[int, List[Tuple[int, float]]]: Dict with top closest neighbors
            for each item.
        """

        knn_dict = dict()
        asd = np.unique(list(sim.keys()))

        for i in asd:
            a_vect = np.array(list(sim.keys()))
            ind = list(np.where(np.any(a_vect == i, axis=1))[0])
            val = np.array(list(sim.values()))[ind]
            knn_dict[i] = list(
                zip(list(a_vect[ind][a_vect[ind] != i]), list(val)))
            
        knn_dict = {int(x): sorted(knn_dict[x],
                                   key=lambda x: x[1], reverse=True)[:top] for x in knn_dict}

        return knn_dict

    @staticmethod
    def knn_price(
        knn_dict: Dict[int, List[Tuple[int, float]]],
        prices: Dict[int, float],
    ) -> Dict[int, float]:
        """Calculate weighted average prices for each item.
        Weights should be positive numbers in [0, 2] interval.

        Args:
            knn_dict (Dict[int, List[Tuple[int, float]]]): <knn> method output.
            prices (Dict[int, float]): Price dict for each item.

        Returns:
            Dict[int, float]: New prices dict, rounded to 2 decimal places.
        """
        prices_new = dict()
        for x in prices:
            list_ = [k[0] for k in knn_dict[x]]
            norm = np.array([k[1] + 1 for k in knn_dict[x]])
            prices_new[x] = round(sum(np.array([prices[k] for
                                            k in list_]) * norm)/sum(norm), 2)


        return prices_new

    @staticmethod
    def transform(
        embeddings: Dict[int, np.ndarray],
        prices: Dict[int, float],
        top: int,
    ) -> Dict[int, float]:
        """Transforming input embeddings into a dictionary
        with weighted average prices for each item.

        Args:
            embeddings (Dict[int, np.ndarray]): Items embeddings.
            prices (Dict[int, float]): Price dict for each item.
            top (int): Number of top neighbors to consider.

        Returns:
            Dict[int, float]: Dict with weighted average prices for each item.
        """
        knn_price_dict = SimilarItems().similarity(embeddings)
        knn_price_dict = SimilarItems().knn(knn_price_dict, top)
        knn_price_dict = SimilarItems().knn_price(knn_price_dict, prices)

        return knn_price_dict