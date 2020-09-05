import pandas as pd
import numpy as np
from scipy.stats import jarque_bera


def skewness(r):
    """
    Alternative to scipy.stats.skew()

    Args:
        r (:obj: pd.Seried):

    Returns:
        float or pd.Seried
    """
    demeaned_r = r - r.mean()
    # Population standard deviation
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3


def kurtosis():
    """
    Alternative to scipy.stats.kurtosis()

    Args:
        r (:obj: pd.Seried):

    Returns:
        float or pd.Seried
    """
    demeaned_r = r - r.mean()
    # Population standard deviation
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4


def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a pd.Series is normal or not.
    Test is applied at 1% level by default.
    Returns True if the hypothesis of normality is accepted, False otherwise.
    """
    statistic, p_value = jarque_bera(r)
    return p_value > level


def main():
    r = np.random.normal(0, 0.1, size=(10000, 1))
    print(is_normal(r))


if __name__ =="__main__":
    main()
