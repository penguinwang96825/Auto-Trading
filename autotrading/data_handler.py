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


def remove_unnamed_col(df):
    return df.drop(df.columns[df.columns.str.contains('unnamed', case=False)], axis=1)


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


class Tfidf:
    """
    Term Frequency - Inverse Document Frequency
    """
    def __init__(self, docs):
        self.docs = docs
        self.docs_words = [d.replace(",", "").split(" ") for d in docs]
        self.vocab = set(itertools.chain(*self.docs_words))
        self.v2i = {v: i for i, v in enumerate(self.vocab)}
        self.i2v = {i: v for v, i in self.v2i.items()}
        # [n_vocab, n_doc]
        self.tf = self.get_tf()
        # [n_vocab, 1]
        self.idf = self.get_idf()
        # [n_vocab, n_doc]
        self.tf_idf = self.tf * self.idf

    def get_tf(self, method="log"):
        tf_methods = {
            "log": lambda x: np.log(1+x),
            "augmented": lambda x: 0.5 + 0.5 * x / np.max(x, axis=1, keepdims=True),
            "boolean": lambda x: np.minimum(x, 1),
            "log_avg": lambda x: (1 + safe_log(x)) / (1 + safe_log(np.mean(x, axis=1, keepdims=True))),
        }
        # Term frequency: how frequent a word appears in a doc
        _tf = np.zeros((len(self.vocab), len(self.docs)), dtype=np.float64)
        for i, d in enumerate(self.docs_words):
            counter = Counter(d)
            for v in counter.keys():
                _tf[self.v2i[v], i] = counter[v] / counter.most_common(1)[0][1]

        weighted_tf = tf_methods.get(method, None)
        if weighted_tf is None:
            raise ValueError
        return weighted_tf(_tf)

    def get_idf(self, method="log"):
        idf_methods = {
            "log": lambda x: 1 + np.log(len(self.docs) / (x+1)),
            "prob": lambda x: np.maximum(0, np.log((len(self.docs) - x) / (x+1))),
            "len_norm": lambda x: x / (np.sum(np.square(x))+1),
        }
        # Inverse document frequency
        df = np.zeros((len(self.i2v), 1))
        for i in range(len(self.i2v)):
            d_count = 0
            for d in self.docs_words:
                d_count += 1 if self.i2v[i] in d else 0
            df[i, 0] = d_count

        idf_fn = idf_methods.get(method, None)
        if idf_fn is None:
            raise ValueError
        return idf_fn(df)

    def cosine_similarity(self, q, _tf_idf):
        unit_q = q / np.sqrt(np.sum(np.square(q), axis=0, keepdims=True))
        unit_ds = _tf_idf / np.sqrt(np.sum(np.square(_tf_idf), axis=0, keepdims=True))
        similarity = unit_ds.T.dot(unit_q).ravel()
        return similarity

    def docs_score(self, q, len_norm=False):
        q_words = q.replace(",", "").split(" ")

        # Add unknown words
        unknown_v = 0
        for v in set(q_words):
            if v not in self.v2i:
                self.v2i[v] = len(self.v2i)
                self.i2v[len(self.v2i)-1] = v
                unknown_v += 1
        if unknown_v > 0:
            _idf = np.concatenate((self.idf, np.zeros((unknown_v, 1), dtype=np.float)), axis=0)
            _tf_idf = np.concatenate((self.tf_idf, np.zeros((unknown_v, self.tf_idf.shape[1]), dtype=np.float)), axis=0)
        else:
            _idf, _tf_idf = self.idf, self.tf_idf
        counter = Counter(q_words)
        q_tf = np.zeros((len(_idf), 1), dtype=np.float)
        for v in counter.keys():
            q_tf[self.v2i[v], 0] = counter[v]

        q_vec = q_tf * _idf

        q_scores = self.cosine_similarity(q_vec, _tf_idf)
        if len_norm:
            len_docs = [len(d) for d in self.docs_words]
            q_scores = q_scores / np.array(len_docs)
        return q_scores

    def get_keywords(self, n=2, m=10):
        for c in range(m):
            col = self.tf_idf[:, c]
            idx = np.argsort(col)[-n:]
            print("doc{}, top{} keywords {}".format(c, n, [self.i2v[i] for i in idx]))

    def show_tfidf(self):
        tfidf = self.tf_idf.T
        vocab = [self.i2v[i] for i in range(len(self.i2v))]
        # [n_vocab, n_doc]
        plt.figure(figsize=(15, 5))
        plt.imshow(tfidf, cmap="YlGn", vmin=tfidf.min(), vmax=tfidf.max())
        plt.xticks(np.arange(tfidf.shape[1]), vocab, fontsize=6, rotation=90)
        plt.yticks(np.arange(tfidf.shape[0]), np.arange(1, tfidf.shape[1]+1), fontsize=6)
        plt.tight_layout()
        plt.show()

    def print_instance_attributes(self):
        for attribute, value in self.__dict__.items():
            print(attribute, '=', value)


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
    tfidf = Tfidf(docs)
    tfidf.show_tfidf()


if __name__ =="__main__":
    main()
