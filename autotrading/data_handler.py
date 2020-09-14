import sys
import json
import sqlite3
import joblib
import requests
import itertools
import glob
import datetime
import warnings
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
from collections import deque
from collections import Counter
from dateutil.relativedelta import relativedelta
from sqlalchemy import create_engine
from transformers import pipeline
from textblob import TextBlob
from api_key_config import API_Config
global API_Config
warnings.filterwarnings("ignore")


def progressbar(iter, prefix="", size=100, file=sys.stdout):
    # Reference from https://stackoverflow.com/questions/3160699/python-progress-bar
    count = len(iter)
    def show(t):
        x = int(size*t/count)
        # file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), int(100*t/count), 100))
        file.write("{}[{}{}] {}%\r".format(prefix, "█"*x, "."*(size-x), int(100*t/count)))
        file.flush()
    show(0)
    for i, item in enumerate(iter):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()


def crawl_forex_data(currency, start_date="2015-09-04", end_date="2020-09-04"):
    """
    Crawl forex data from https://marketdata.tradermade.com
    """
    api_key = API_Config.TRADE_MADE_API_KEY
    url = "https://marketdata.tradermade.com/api/v1/timeseries"
    querystring = {
        "currency": currency,
        "api_key": api_key,
        "start_date": start_date,
        "end_date": end_date
        }
    res = requests.get(url, params=querystring).text
    res = json.loads(res)
    data = pd.DataFrame(res.get("quotes"))
    data["date"] = data["date"].apply(lambda x: pd.to_datetime(x))
    data["date"] = data["date"].apply(lambda x: x.date())
    data.columns = ["Close", "Date", "High", "Low", "Open"]
    data = data[["Date", "Open", "High", "Low", "Close"]]
    data = data.astype(object).where(pd.notnull(data), None)
    data.set_index(keys="Date", drop=True, inplace=True)
    database_path = 'sqlite:///data/data.db'
    engine = create_engine(database_path, echo=False)
    data.to_sql(currency, con=engine, if_exists='replace')
    engine.dispose()
    return data


def crawl_stock_data(symbol):
    """
    Crawl forex data from yahoo finance API.
    """
    data = yf.download(symbol, progress=False)
    database_path = 'sqlite:///data/data.db'
    engine = create_engine(database_path, echo=False)
    data.to_sql(symbol, con=engine, if_exists='replace')
    engine.dispose()
    return data


def read_stock_table_from_db(table):
    """
    Read stock table from database using sqlalchemy.
    """
    database_path = 'sqlite:///data/data.db'
    engine = create_engine(database_path, echo=False)
    data = pd.read_sql_table(table, database_path)
    engine.dispose()
    data.set_index(keys="Date", drop=True, inplace=True)
    return data


def read_forex_table_from_db(table):
    """
    Read forex table from database using sqlalchemy.
    "EURUSD", "USDJPY", "GBPUSD", "USDCHF"
    """
    database_path = 'sqlite:///data/data.db'
    engine = create_engine(database_path, echo=False)
    data = pd.read_sql_table(table, database_path)
    engine.dispose()
    data.set_index(keys="Date", drop=True, inplace=True)
    return data


def read_twitter_table_from_db(table="tweets"):
    """
    Read tweets table from database.
    """
    database_path = 'sqlite:///data/twitter.db'
    engine = create_engine(database_path, echo=False)
    data = pd.read_sql_table(table, database_path)
    engine.dispose()
    data.set_index(keys="Date", drop=True, inplace=True)
    return data


def crawl_sp500_component_stocks_table():
    data, _ = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    return data


def create_sp500_stock_tables_into_db():
    """
    Only "BRK.B" and "BF.B" will fail.
    """
    data = crawl_sp500_component_stocks_table()
    symbol_list = list(data.Symbol)
    fail_list = []
    for symbol in progressbar(symbol_list):
        try:
            data = crawl_stock_data(symbol)
            if data.shape[0] == 0:
                fail_list.append(symbol)
        except:
            fail_list.append(symbol)
            print("Cannot crawl {}.".format(symbol))
    print("Fail: ", fail_list)


def create_currency_pairs_into_db():
    """
    The major pairs are the four most heavily traded currency pairs in the forex market.
    The four major pairs are the EUR/USD, USD/JPY, GBP/USD, USD/CHF.
    These four major pairs are deliverable currencies and are part of the g10 currency group.
    """
    currency_pairs = ["EURUSD", "USDJPY", "GBPUSD", "USDCHF"]
    for currency in currency_pairs:
        try:
            _ = crawl_forex_data(currency)
        except:
            print("Cannot crawl {}.".format(currency))


def reconstruct(df, prediction_delay=7):

    def fillnan4df(df):
        data = df.copy()
        data = data.groupby(df.index)["Text"].agg(list)
        index = pd.date_range(start=str(data.index.min()), end=str(data.index.max()), freq='D')
        data.index = pd.DatetimeIndex(data.index)
        data = data.reindex(index, fill_value=None)
        data = pd.DataFrame(data)
        return data

    def add_function(row, prediction_delay=7):
        total = []
        for i in range(prediction_delay):
            if str(row[i]) != "nan":
                total += row[i]
            elif np.dtype(np.float) != type(row[i]):
                total += row[i]
        return total

    def eliminate_nan_in_list(content_list):
        return [content for content in content_list if type(content) != np.dtype(np.float)]

    data = fillnan4df(df)
    prev_news = deque(maxlen=prediction_delay)

    news_seperate_ndays = []
    for idx, news in enumerate(data.Text):
        prev_news.append(news)
        if len(prev_news) == prediction_delay:
            n_days_news = list(prev_news)
            news_seperate_ndays.append(n_days_news)

    # Collect data from previous prediction_delay days
    start_date = pd.to_datetime(df.index.min()) + relativedelta(days=+(prediction_delay-1))
    end_date = pd.to_datetime(df.index.max())
    index = pd.date_range(start_date, end_date, freq='D')
    data = pd.DataFrame(news_seperate_ndays, index=index)
    data = data.apply(add_function, axis=1)
    data = pd.DataFrame(data, columns=["tweets"])

    return data


def expand_sentiment_score(text_data):
    sentiment_scores, subjectivity_scores = [], []
    for tweet_row in tqdm(list(text_data.tweets)):
        polarity_list, subjectivity_list = [], []
        for tweet in tweet_row:
            blob = TextBlob(tweet)
            polarity_list.append(round(blob.sentiment.polarity, 4))
            subjectivity_list.append(round(blob.sentiment.subjectivity, 4))
        polarity_mean = np.mean(polarity_list)
        subjectivity_mean = np.mean(subjectivity_list)
        sentiment_scores.append(polarity_mean)
        subjectivity_scores.append(subjectivity_mean)
    text_data["polarity"] = np.array(sentiment_scores)
    text_data["subjectivity"] = np.array(subjectivity_scores)
    return text_data





def main():
    docs = [
        "it is a good day, I like to stay here",
        "I am happy to be here",
        "I am bob",
        "it is sunny today",
        "I have a party today",
        "it is a dog and that is a cat",
        "there are dog and cat on the tree",
        "I study hard this morning",
        "today is a good day",
        "tomorrow will be a good day",
        "I like coffee, I like book and I like apple",
        "I do not like it",
        "I am kitty, I like bob",
        "I do not care who like bob, but I like kitty",
        "It is coffee time, bring your cup",
    ]
    docs_words = [d.replace(",", "").split(" ") for d in docs]
    vocab = set(itertools.chain(*docs_words))
    v2i = {v: i for i, v in enumerate(vocab)}
    i2v = {i: v for v, i in v2i.items()}
    print(v2i)
    print(i2v)


if __name__ =="__main__":
    main()
