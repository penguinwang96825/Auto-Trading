import data_handler
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import jarque_bera
from scipy.stats import norm
from scipy.optimize import minimize


def get_ind_returns(symbol):
    """
    Args:
        symbol (:obj: str or list of str):

    Returns:
        pd.Seried or pd.DataFrame
    """
    if isinstance(symbol, str):
        data = data_handler.read_stock_table_from_db(symbol).Close
        return data.pct_change()
    elif isinstance(symbol, list):
        d = {name: pd.DataFrame() for name in symbol}
        list_of_df = []
        for name, df in d.items():
            df = data_handler.read_stock_table_from_db(name).Close
            list_of_df.append(df)
        data = pd.concat(list_of_df, axis=1, join="inner")
        data.columns = symbol
        return data.pct_change()


def semi_deviation(rets):
    is_negative = rets < 0
    return rets[is_negative].std(ddof=0)


def var_historic(rets, level=5):
    """
    In this approach we calculate VaR directly from past returns.
    For example, suppose we want to calculate the 1-day 95% VaR for an equity using 100 days of data.
    The 95th percentile corresponds to the least worst of the worst 5% of returns.
    In this case, because we are using 100 days of data, the VaR simply corresponds to the 5th worst day.
    "How much could I lose in a really bad day?"
    """
    if isinstance(rets, pd.DataFrame):
        return rets.aggregate(var_historic, level=level)
    elif isinstance(rets, pd.Series):
        return -np.percentile(rets, level)
    else:
        raise TypeError("Expected r to be pd.DataFrame or pd.Series!")


def cvar_historic(rets, level=5):
    """
    Computes the Conditional VaR of pd.Series of pd.DataFrame.
    """
    if isinstance(rets, pd.Series):
        is_beyond = rets <= -var_historic(rets, level=level)
        return -rets[is_beyond].mean()
    elif isinstance(rets, pd.DataFrame):
        return rets.aggregate(cvar_historic, level=level)
    else:
        raise TypeError("Expected r to be pd.DataFrame or pd.Series!")


def var_gaussian(rets, level=5, modified=False):
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
        s = skewness(rets)
        k = kurtosis(rets)
        z = (z + (z**2-1)*s/6 + (z**3-3*z)*(k-3)/24 - (2*z**3-5*z)*(s**2)/36)
    return -(rets.mean() + z*rets.std(ddof=0))


def skewness(rets):
    """
    Alternative to scipy.stats.skew()

    Args:
        rets (:obj: pd.Seried):

    Returns:
        float or pd.Seried
    """
    demeaned_r = rets - rets.mean()
    # Population standard deviation
    sigma_r = rets.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3


def kurtosis(rets):
    """
    Alternative to scipy.stats.kurtosis()

    Args:
        rets (:obj: pd.Seried):

    Returns:
        float or pd.Seried
    """
    demeaned_r = rets - rets.mean()
    # Population standard deviation
    sigma_r = rets.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4


def is_normal(rets, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a pd.Series is normal or not.
    Test is applied at 1% level by default.
    Returns True if the hypothesis of normality is accepted, False otherwise.
    """
    statistic, p_value = jarque_bera(rets)
    return p_value > level


def annualise_ret(rets, periods_per_year):
    """
    https://www.investopedia.com/terms/a/annualized-total-return.asp
    """
    compounded_growth = (1+rets).prod()
    n_periods = rets.shape[0]
    return compounded_growth**(periods_per_year/n_periods)-1


def annualise_vol(rets, periods_per_year):
    """
    https://breakingdownfinance.com/finance-topics/finance-basics/annualize-volatility/
    """
    return rets.std()*(periods_per_year**0.5)


def sharpe_ratio(rets, risk_free_rate, periods_per_year):
    # Convert annual risk free rate to per period
    rf_per_period = (1+risk_free_rate)*(1/periods_per_year)-1
    excess_ret = rets - rf_per_period
    ann_ex_ret = annualise_ret(excess_ret, periods_per_year)
    ann_vol = annualise_vol(rets, periods_per_year)
    return ann_ex_ret/ann_vol


def drawdown(rets, cash=1000):
    """
    Args:
        rets (:obj: pd.DataFrame):

    Returns:
        wealth (:obj: pd.DataFrame)
        peaks (:obj: pd.DataFrame)
        drawdown (:obj: pd.DataFrame)
    """
    wealth_index = cash*(rets+1).cumprod()
    previous_peak = wealth_index.cummax()
    drawdowns = (wealth_index-previous_peak)/previous_peak
    return pd.DataFrame({
        "wealth": wealth_index,
        "peaks": previous_peak,
        "drawdown": drawdowns
    })


def portfolio_return(weights, exp_rets):
    return weights.T @ exp_rets


def portfolio_vol(weights, covmat):
    """
    https://blog.quantinsti.com/calculating-covariance-matrix-portfolio-variance/
    """
    return (weights.T @ covmat @ weights)**0.5


def plot_binary_efficient_frontier(exp_rets, cov, n_points=100):
    if exp_rets.shape[0] != 2 or cov.shape[0] != 2:
        raise ValueError("plot_efficient_frontier_2 can only plot 2-asset frontiers!")
    weights = [np.array([w, 1-w]) for w in np.linspace(0, 1, n_points)]
    rets = [portfolio_return(w, exp_rets) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"Returns": rets, "Volatility": vols})
    plt.figure(figsize=(15, 10))
    plt.scatter(ef.Volatility, ef.Returns)
    plt.show()


def minimize_vol(target_return, exp_rets, cov):
    """
    Get weights that can minimize volatility.

    Args:
        target_return (:obj: float):
        exp_rets (:obj: pd.DataFrame):
        cov (:obj: pd.DataFrame):

    Returns:
        weights (:obj: np.array)
    """
    n = er.shape[0]
    init_guess = np.repeat(1/n, n)
    bounds = ((0.0, 1.0), )*n
    return_is_target = {
        "type": "eq",
        "args": (exp_rets, ),
        "fun": lambda weights, er: target_return - portfolio_return(weights, exp_rets)
    }
    weights_sum_to_one = {
        "type": "eq",
        "fun": lambda weights: np.sum(weights) - 1
    }
    results = minimize(
        fun=portfolio_vol,
        x0=init_guess,
        args=(cov, ),
        method="SLSQP",
        options={"disp": False},
        constraints=(return_is_target, weights_sum_to_one),
        bounds=bounds)
    return results.x


def optimal_weights(exp_rets, cov, n_points=100):
    """
    List of weights to run the optimizer on to minimize the volatility.
    """
    target_rs = np.linspace(exp_rets.min(), exp_rets.max(), n_points)
    weights = [minimize_vol(target_return, er, cov) for target_return in target_rs]
    return weights


def plot_multi_efficient_frontier(exp_rets, cov, n_points=100, show_cml=True, risk_free_rate=0.0):
    weights = optimal_weights(exp_rets, cov, n_points)
    rets = [portfolio_return(w, exp_rets) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"Returns": rets, "Volatility": vols})
    plt.figure(figsize=(15, 10))
    plt.scatter(ef.Volatility, ef.Returns)
    if show_cml:
        plt.xlim(left=0)
        w_msr = maximize_sharpe_ratio(risk_free_rate, exp_rets, cov)
        r_msr = portfolio_return(w_msr, exp_rets)
        vol_msr = portfolio_vol(w_msr, cov)
        # Add CML
        x_cml = [0, vol_msr]
        y_cml = [risk_free_rate, r_msr]
        plt.plot(x_cml, y_cml, color="green", marker="o", linestyle="dashed")
    plt.show()


def maximize_sharpe_ratio(risk_free_rate, exp_rets, cov):
    """
    Max sharpe ratio
    """
    n = exp_rets.shape[0]
    init_guess = np.repeat(1/n, n)
    bounds = ((0.0, 1.0), )*n
    weights_sum_to_one = {
        "type": "eq",
        "fun": lambda weights: np.sum(weights) - 1
    }

    def neg_sharpe_ratio(weights, risk_free_rate, er, cov):
        r = portfolio_return(weights, exp_rets)
        vol = portfolio_vol(weights, cov)
        return -(r - risk_free_rate)/vol

    results = minimize(
        fun=neg_sharpe_ratio,
        x0=init_guess,
        args=(risk_free_rate, exp_rets, cov, ),
        method="SLSQP",
        options={"disp": False},
        constraints=(weights_sum_to_one),
        bounds=bounds)
    return results.x


def main():
    returns = get_ind_returns(symbol=["GOOG", "AAPL", "MSFT", "AMZN"])
    exp_rets = annualise_rets(returns, periods_per_year=252)
    cov = returns.cov()
    plot_multi_efficient_frontier(exp_rets, cov)


if __name__ =="__main__":
    main()
