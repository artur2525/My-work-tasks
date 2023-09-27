from typing import List, Tuple
from typing import Tuple

import numpy as np
from scipy.stats import ttest_ind


def quantile_ttest(
    control: List[float],
    experiment: List[float],
    alpha: float = 0.05,
    quantile: float = 0.95,
    n_bootstraps: int = 1000,
) -> Tuple[float, bool]:
    """
    Bootstrapped t-test for quantiles of two samples.
    """
    def bootstrapped_quant(control, experiment, n_bootstraps: int) -> Tuple[List, List]:
        """Bootstrapped median distribution"""
        bootstrapped_quant_co = []
        bootstrapped_quant_ex = []

        for _ in range(n_bootstraps):
            mask_con = np.random.choice(
                range(0, len(control)), size=len(control), replace=True)
            mask_exp = np.random.choice(
                range(0, len(experiment)), size=len(experiment), replace=True)

            bootstrapped_quant_co.append(
                np.quantile(control[mask_con], quantile))
            bootstrapped_quant_ex.append(
                np.quantile(experiment[mask_exp], quantile))

        return bootstrapped_quant_co, bootstrapped_quant_ex

    bootstrapped_quant_co, bootstrapped_quant_ex = bootstrapped_quant(
        control, experiment, n_bootstraps)
    _, p_value = ttest_ind(bootstrapped_quant_co, bootstrapped_quant_ex)
    result = p_value < alpha

    return p_value, bool(result)