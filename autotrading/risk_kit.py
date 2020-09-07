import pandas as pd
import numpy as np
from scipy.stats import jarque_bera
from scipy.stats import norm


def semi_deviation(r):
    is_negative = r < 0
    return r[is_negative].std(ddof=0)


def var_historic(r, level=5):
    """
    In this approach we calculate VaR directly from past returns.
    For example, suppose we want to calculate the 1-day 95% VaR for an equity using 100 days of data.
    The 95th percentile corresponds to the least worst of the worst 5% of returns.
    In this case, because we are using 100 days of data, the VaR simply corresponds to the 5th worst day.
    "How much could I lose in a really bad day?"
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, level=level)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, level)
    else:
        raise TypeError("Expected r to be pd.DataFrame or pd.Series!")


def cvar_historic(r, level=5):
    """
    Computes the Conditional VaR of pd.Series of pd.DataFrame.
    """
    if isinstance(r, pd.Series):
        is_beyond = r <= -var_historic(r, level=level)
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, level=level)
    else:
        raise TypeError("Expected r to be pd.DataFrame or pd.Series!")


def var_gaussian(r, level=5, modified=False):
    """
    Returns Parametric Gaussian VaR of a pd.Series of pd.DataFrame.
    If "modified" is set to True, then the modified VaR is returned, using the Cornish-Fisher modification.
    mVaR represents an empirical expression adjusted for skewness and kurtosis of the empirical distribution.
    Empirical returns are commonly skewed and peaked, such that assuming normal distribution is a bad fit to estimate VaR.
    Therefore, mVaR adjusts for skewness and kurtosis to better reflect the empirical VaR.
    """
    z = norm.ppf(level/100)
    if modified:
        # Modify the z score based on observed skewness and kurtosis
        s = skewness(r)
        k = kurtosis(r)
        z = (z + (z**2-1)*s/6 + (z**3-3*z)*(k-3)/24 - (2*z**3-5*z)*(s**2)/36)
    return -(r.mean() + z*r.std(ddof=0))


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


def annualise_vol(r, periods_per_year):
    return r.std()*(periods_per_year**.05)


def annualise_rets(r, periods_per_year):
    compound_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compound_growth**(periods_per_year/n_periods)-1


def sharpe_ratio(r, risk_free_rate, periods_per_year):
    rf_per_period = (1+risk_free_rate)**(1/periods_per_year)-1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualise_rets(excess_ret, periods_per_year)
    ann_vol = annualise_vol(r, periods_per_year)
    return ann_ex_ret/ann_vol


def main():
    r = np.random.normal(0, 0.1, size=(10000, 1))
    print(is_normal(r))


if __name__ =="__main__":
    main()
