import sys
import json
import sqlite3
import joblib
import requests
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine


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
    data = yf.download(symbol)
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
    """
    database_path = 'sqlite:///data/data.db'
    engine = create_engine(database_path, echo=False)
    data = pd.read_sql_table(table, database_path)
    engine.dispose()
    data.set_index(keys="Date", drop=True, inplace=True)
    return data


def crawl_sp500_component_stocks_table():
    data, _ = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    return data


def create_sp500_stock_tables_into_db():
    data = crawl_sp500_component_stocks_table()
    symbol_list = list(data.Symbol)
    fail_list = []
    for symbol in progressbar(symbol_list):
        try:
            _ = crawl_stock_data(symbol)
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


def main():
    df = read_stock_table_from_db("GOOG")


if __name__ =="__main__":
    main()
