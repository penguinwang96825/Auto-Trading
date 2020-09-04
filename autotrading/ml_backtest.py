import os
import math
import talib
import joblib
import warnings
import datetime
import shap
import numpy as np
import pandas as pd
import yfinance as yf
import empyrical as ep
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import seaborn as sns
import xgboost as xgb
from xgboost import XGBClassifier
from IPython.display import display
from matplotlib.ticker import FuncFormatter
from sklearn.naive_bayes import GaussianNB
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
warnings.filterwarnings("ignore")


def generate_feature(data):
    high = data.High.values
    low = data.Low.values
    close = data.Close.values

    feature_df = pd.DataFrame(index=data.index)
    feature_df["ADX"] = ADX = talib.ADX(high, low, close, timeperiod=14)
    feature_df["ADXR"] = ADXR = talib.ADXR(high, low, close, timeperiod=14)
    feature_df["APO"] = APO = talib.APO(close, fastperiod=12, slowperiod=26, matype=0)
    feature_df["AROONOSC"] = AROONOSC = talib.AROONOSC(high, low, timeperiod=14)
    feature_df["CCI"] = CCI = talib.CCI(high, low, close, timeperiod=14)
    feature_df["CMO"] = CMO = talib.CMO(close, timeperiod=14)
    feature_df["DX"] = DX = talib.DX(high, low, close, timeperiod=14)
    feature_df["MINUS_DI"] = MINUS_DI = talib.MINUS_DI(high, low, close, timeperiod=14)
    feature_df["MINUS_DM"] = MINUS_DM = talib.MINUS_DM(high, low, timeperiod=14)
    feature_df["MOM"] = MOM = talib.MOM(close, timeperiod=10)
    feature_df["PLUS_DI"] = PLUS_DI = talib.PLUS_DI(high, low, close, timeperiod=14)
    feature_df["PLUS_DM"] = PLUS_DM = talib.PLUS_DM(high, low, timeperiod=14)
    feature_df["PPO"] = PPO = talib.PPO(close, fastperiod=12, slowperiod=26, matype=0)
    feature_df["ROC"] = ROC = talib.ROC(close, timeperiod=10)
    feature_df["ROCP"] = ROCP = talib.ROCP(close, timeperiod=10)
    feature_df["ROCR100"] = ROCR100 = talib.ROCR100(close, timeperiod=10)
    feature_df["RSI"] = RSI = talib.RSI(close, timeperiod=14)
    feature_df["ULTOSC"] = ULTOSC = talib.ULTOSC(high, low, close, timeperiod1=7, timeperiod2=14, timeperiod3=28)
    feature_df["WILLR"] = WILLR = talib.WILLR(high, low, close, timeperiod=14)

    matrix = np.stack((
        ADX, ADXR, APO, AROONOSC, CCI, CMO, DX, MINUS_DI, ROCR100, ROC,
        MINUS_DM, MOM, PLUS_DI, PLUS_DM, PPO, ROCP, WILLR, ULTOSC, RSI))
    matrix = np.nan_to_num(matrix)
    matrix = matrix.transpose()

    return feature_df, matrix


def triple_barrier(data, ub, lb, max_period, two_class=True):
    """
    Reference from https://www.finlab.tw/generate-labels-stop-loss-stop-profit/

    Args:
        data (:obj: pd.DataFrame):
            Get data from yahoo finance API with columns: `Open`, `High`, `Low`, `Close`, and (optionally) `Volume`.
            If any columns are missing, set them to what you have available,
            e.g. df['Open'] = df['High'] = df['Low'] = df['Close']
        ub (:obj: float):
            Upper bound means profit-taking.
        lb (:obj: float):
            Lower bound means loss-stop.
        max_period (:obj: int):
            Max time to hold the position.
        two_class (:obj: bool):
            Whether or not the binary signal has been generated.

    Returns:
        :obj: pd.DataFrame
            DataFrame object contains four columns.
            triple_barrier_profit, triple_barrier_sell_time, triple_barrier_signal, binary_signal (optional)

    Example::
        data = yf.download("AAPL")
        ret = triple_barrier(data, ub=1.07, lb=0.97, max_period=20, two_class=True)
    """
    def end_price(s):
        return np.append(s[(s / s[0] > ub) | (s / s[0] < lb)], s[-1])[0]/s[0]

    r = np.array(range(max_period))

    def end_time(s):
        return np.append(r[(s / s[0] > ub) | (s / s[0] < lb)], max_period-1)[0]

    price = data.Close
    p = price.rolling(max_period).apply(end_price, raw=True).shift(-max_period+1)
    t = price.rolling(max_period).apply(end_time, raw=True).shift(-max_period+1)
    t = pd.Series([t.index[int(k+i)] if not math.isnan(k+i) else np.datetime64('NaT')
                   for i, k in enumerate(t)], index=t.index).dropna()

    signal = pd.Series(0, p.index)
    signal.loc[p > ub] = 1.0
    signal.loc[p < lb] = -1.0

    ret = pd.DataFrame({
        'triple_barrier_profit': p,
        'triple_barrier_sell_time': t,
        'triple_barrier_signal': signal})
    ret = ret.fillna(0)
    ret["{}d_returns".format(max_period)] = data.Close.pct_change(periods=max_period).fillna(0)
    sign = lambda x: math.copysign(1, x)

    if two_class:
        binary_list = []
        for ind, row in ret.iterrows():
            if row["triple_barrier_signal"] == 0:
                binary_list.append(sign(row["{}d_returns".format(max_period)]))
            else:
                binary_list.append(row["triple_barrier_signal"])
        ret["binary_signal"] = binary_list
        ret["binary_signal"] = ret["binary_signal"].apply(lambda x: 1.0 if x == 1.0 else 0.0)

    return ret


def ml_backtest(data, prediction, cash=1000.0, fee=0.002, plot=True, stats=True):
    """
    Reference from https://gist.github.com/StockBoyzZ/396d48be23fd479a5ca62362b1bc8dc7#file-strategy_test-py
    Reference from https://github.com/kernc/backtesting.py/blob/1512f0e4cd483d7c0c00b6ad6953ca28322b3b7c/backtesting/backtesting.py

    Args:
        data (:obj: pd.DataFrame):
            Get data from yahoo finance API with columns: `Open`, `High`, `Low`, `Close`, and (optionally) `Volume`.
            If any columns are missing, set them to what you have available,
            e.g. df['Open'] = df['High'] = df['Low'] = df['Close']
        prediction (:obj: list):
            Using machine model to predict signal. Predictions in the list are assigned a label {0, 1}.
        cash (:obj: float):
            Initial cash to start with.
        fee (:obj: float):
            Commission ratio.
        plot (:obj: bool):
            Whether or not the performance has been plotted.
        stats (:obj: bool):
            Whether or not the statistics result has been calculated.

    Returns:
        :obj: None
    """
    data["binary_signal"] = prediction
    data["binary_signal"] = data["binary_signal"].apply(lambda x: 1.0 if x == 1.0 else 0.0)
    data['status'] = data.binary_signal.shift(1).fillna(0)
    data['buy_price'] = data.Open[np.where((data.status == 1.0) & (data.status.shift(1) == 0.0))[0]]
    data['sell_price'] = data.Open[np.where((data.status == 0.0) & (data.status.shift(1) == 1.0))[0]]
    data = data.fillna(0.0)

    # Calculate trade return and net trade return
    buy_cost = np.array(data.buy_price[data.buy_price != 0])
    sell_price = np.array(data.sell_price[data.sell_price != 0])
    if len(buy_cost) > len(sell_price) :
        buy_cost = buy_cost[:-1]
    trade_return = sell_price / buy_cost - 1
    net_trade_return = trade_return - fee

    # Put trade return and net trade return into dataframe
    data["trade_return"] = 0.0
    data["net_trade_return"] = 0.0
    sell_dates = data.sell_price[data.sell_price != 0].index
    data.loc[sell_dates, "trade_return"] = trade_return
    data.loc[sell_dates, "net_trade_return"] = net_trade_return

    # Plot performance for every strategies
    data["open_daily_return"] = data.Open / data.Open.shift(1) - 1
    data["strategy_return"] = data.status.shift(1) * data.open_daily_return
    data["strategy_net_return"] = data.strategy_return
    data.loc[sell_dates, "strategy_net_return"] = data.loc[sell_dates, "strategy_net_return"] - fee
    data = data.fillna(0.0)
    data['buy_and_hold_equity'] = (data.open_daily_return + 1).cumprod() * cash
    data['strategy_equity'] = (data.strategy_return + 1).cumprod() * cash
    data['strategy_net_equity'] = (data.strategy_net_return + 1).cumprod() * cash

    def _compute_drawdown_duration_peaks(dd: pd.Series):
        iloc = np.unique(np.r_[(dd == 0).values.nonzero()[0], len(dd) - 1])
        iloc = pd.Series(iloc, index=dd.index[iloc])
        df = iloc.to_frame('iloc').assign(prev=iloc.shift())
        df = df[df['iloc'] > df['prev'] + 1].astype(int)
        # If no drawdown since no trade, avoid below for pandas sake and return nan series
        if not len(df):
            return (dd.replace(0, np.nan),) * 2
        df['duration'] = df['iloc'].map(dd.index.__getitem__) - df['prev'].map(dd.index.__getitem__)
        df['peak_dd'] = df.apply(lambda row: dd.iloc[row['prev']:row['iloc'] + 1].max(), axis=1)
        df = df.reindex(dd.index)
        return df['duration'], df['peak_dd']

    def _data_period(index):
        """Return data index period as pd.Timedelta"""
        values = pd.Series(index[-100:])
        return values.diff().median()

    def _round_timedelta(value, _period=_data_period(data.index)):
        if not isinstance(value, pd.Timedelta):
            return value
        resolution = getattr(_period, 'resolution_string', None) or _period.resolution
        return value.ceil(resolution)

    if stats:
        s = pd.Series(dtype=object)
        s.loc['Start'] = data.index[0]
        s.loc['End'] = data.index[-1]
        s.loc['Duration'] = s.End - s.Start
        s.loc['Equity Final [$]'] = data.strategy_net_equity[-1]
        s.loc['Equity Peak [$]'] = data.strategy_net_equity.max()
        s.loc['Return [%]'] = (data.strategy_equity[-1] - data.strategy_equity[0]) / data.strategy_equity[0] * 100
        s.loc['Net Return [%]'] = (data.strategy_net_equity[-1] - data.strategy_net_equity[0]) / data.strategy_net_equity[0] * 100
        s.loc['Buy & Hold Return [%]'] = (data.buy_and_hold_equity[-1] - data.buy_and_hold_equity[0]) / data.buy_and_hold_equity[0] * 100
        s.loc['Mean Return / Day'] = mean_return = np.mean(trade_return)
        s.loc['Mean Net Return / Day'] = mean_net_return = np.mean(net_trade_return)
        s.loc['# Trades'] = trade_count = len(sell_dates)
        s.loc['# Trades / Year'] = trade_count_per_year = trade_count / (len(data)/252)
        s.loc['Win Rate [%]'] = win_rate = (net_trade_return > 0).sum() / trade_count * 100
        s.loc['Best Trade [%]'] = data.strategy_net_return.max() * 100
        s.loc['Worst Trade [%]'] = data.strategy_net_return.min() * 100
        dd = 1 - data.strategy_net_return / np.maximum.accumulate(data.strategy_net_return)
        dd_dur, dd_peaks = _compute_drawdown_duration_peaks(pd.Series(dd, index=data.index))
        s.loc['Max. Drawdown [%]'] = max_dd = -np.nan_to_num(dd.max()) * 100
        s.loc['Avg. Drawdown [%]'] = -dd_peaks.mean() * 100
        s.loc['Max. Drawdown Duration'] = _round_timedelta(dd_dur.max())
        s.loc['Avg. Drawdown Duration'] = _round_timedelta(dd_dur.mean())
        strategy_ear = (data.strategy_net_return + 1).cumprod()[-1] ** (252/len(data)) - 1
        strategy_std = data.strategy_net_return.std() * (252 ** 0.5)
        s.loc['Sharpe Ratio'] = (strategy_ear - 0.01) / strategy_std
        s.loc['Calmar Ratio'] = strategy_ear / ((-max_dd / 100) or np.nan)
        print(s)

    def plot_drawdown_underwater(returns, ax=None, **kwargs):
        # Reference from https://github.com/quantopian/pyfolio/blob/master/pyfolio/plotting.py
        def percentage(x, pos):
            """
            Adds percentage sign to plot ticks.
            """
            return '%.0f%%' % x

        if ax is None:
            ax = plt.gca()

        y_axis_formatter = FuncFormatter(percentage)
        ax.yaxis.set_major_formatter(FuncFormatter(y_axis_formatter))

        df_cum_rets = ep.cum_returns(returns, starting_value=1.0)
        running_max = np.maximum.accumulate(df_cum_rets)
        underwater = -100 * ((running_max - df_cum_rets) / running_max)
        (underwater).plot(ax=ax, kind='area', color='coral', alpha=0.7, **kwargs)
        ax.set_ylabel('Drawdown')
        ax.set_title('Underwater plot')
        ax.set_xlabel('')
        return ax

    # Plot price and signal
    if plot:
        fig = plt.figure(figsize=(20, 15))
        spec = gridspec.GridSpec(nrows=7, ncols=1, figure=fig)
        ax1 = fig.add_subplot(spec[0:2])
        ax1.plot(data.Close, alpha=0.7)
        ax1.scatter(data.loc[data.buy_price != 0].index, data.loc[data.buy_price != 0, "Close"], marker="^", label="buy", color="green")
        ax1.scatter(data.loc[data.sell_price != 0].index, data.loc[data.sell_price != 0, "Close"], marker="v", label="sell", color="red")
        for i in range(len(data)):
            if data.binary_signal[i] == 1:
                ax1.axvspan(
                    mdates.datestr2num(data.index[i].strftime('%Y-%m-%d')) - 0.5,
                    mdates.datestr2num(data.index[i].strftime('%Y-%m-%d')) + 0.5,
                    facecolor='lightgreen', edgecolor='none', alpha=0.5
                    )
            else:
                ax1.axvspan(
                    mdates.datestr2num(data.index[i].strftime('%Y-%m-%d')) - 0.5,
                    mdates.datestr2num(data.index[i].strftime('%Y-%m-%d')) + 0.5,
                    facecolor='lightcoral', edgecolor='none', alpha=0.5
                    )
        ax1.title.set_text("Close Price")
        ax1.legend()
        ax1.grid()
        ax2 = fig.add_subplot(spec[2:4])
        ax2.plot(data.buy_and_hold_equity, label="Buy & Hold")
        ax2.plot(data.strategy_equity, label="ML Strategy")
        ax2.plot(data.strategy_net_equity, label="ML Strategy with Fee")
        ax2.title.set_text("Equity")
        ax2.legend()
        ax2.grid()
        ax3 = fig.add_subplot(spec[4:6])
        ax3 = plot_drawdown_underwater(data.strategy_net_return, ax=ax3)
        ax3.title.set_text("Time Under Water")
        ax3.grid()
        ax4 = fig.add_subplot(spec[6])
        ax4.plot(data.binary_signal, color='orange')
        ax4.title.set_text("Prediction")
        ax4.grid()
        plt.tight_layout()
        plt.show()


def main():
    # Get data and split into train dataset and test dataset
    data = yf.download("SPY")
    dtrain = data.loc[:"2017-01-01"]
    dtest = data.loc["2017-01-01":]
    train_feature_df, X_train = generate_feature(dtrain)
    y_train = triple_barrier(dtrain, ub=1.07, lb=0.97, max_period=20, two_class=True).binary_signal
    test_feature_df, X_test = generate_feature(dtest)
    y_test = triple_barrier(dtest, ub=1.07, lb=0.97, max_period=20, two_class=True).binary_signal

    # Modelling
    clf = XGBClassifier(learning_rate=0.01, n_estimators=400, random_state=1016)
    # xgb_param = clf.get_xgb_params()
    # cv_result = xgb.cv(
    #     xgb_param, xgb.DMatrix(X_train, label=y_train), num_boost_round=5000, nfold=15, metrics=['auc'],
    #     early_stopping_rounds=50, stratified=True, seed=1016)
    # clf.set_params(n_estimators=cv_result.shape[0])
    clf.fit(train_feature_df, y_train, eval_metric='auc')
    y_pred = clf.predict(test_feature_df)
    print("Accuracy: {}".format(metrics.accuracy_score(y_test, y_pred)))
    print(classification_report(y_test, y_pred))

    # Generate predictions against our training and test data
    pred_train = clf.predict(train_feature_df)
    proba_train = clf.predict_proba(train_feature_df)
    pred_test = clf.predict(test_feature_df)
    proba_test = clf.predict_proba(test_feature_df)

    # Calculate the fpr and tpr for all thresholds of the classification
    train_fpr, train_tpr, train_threshold = metrics.roc_curve(y_train, proba_train[:,1])
    test_fpr, test_tpr, test_threshold = metrics.roc_curve(y_test, proba_test[:,1])

    train_roc_auc = metrics.auc(train_fpr, train_tpr)
    test_roc_auc = metrics.auc(test_fpr, test_tpr)

    # Plot ROC-AUC cureve
    plt.figure(figsize=(15, 10))
    plt.title('Receiver Operating Characteristic')
    plt.plot(train_fpr, train_tpr, 'b', label='Train AUC = %0.2f' % train_roc_auc)
    plt.plot(test_fpr, test_tpr, 'g', label='Test AUC = %0.2f' % test_roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show()

    # Feature importance
    explainer = shap.TreeExplainer(clf)
    shap_values = explainer.shap_values(test_feature_df).round(4)
    shap.summary_plot(shap_values, test_feature_df, plot_type="bar", plot_size=(15, 10))
    shap.summary_plot(shap_values, test_feature_df, plot_size=(15, 10))

    # Backtest for machine learning
    ml_backtest(dtest, y_pred)

    # Save model
    folder_path = "./checkpoints"
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)
    file_name = "./checkpoints/GaussianNB_{}.bin".format(datetime.datetime.today().date())
    joblib.dump(clf, file_name)

    # Get trained model
    file_name = "./checkpoints/GaussianNB_{}.bin".format(datetime.datetime.today().date())
    clf = joblib.load(file_name)
    print("Successful!")


if __name__ == "__main__":
    main()
