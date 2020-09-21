import sys
import csv
import data_handler
import requests
import grequests
import warnings
import time
import random
import pandas as pd
import numpy as np
from crawler_config import USER_AGENT_LIST
from multiprocessing import Pool
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
global USER_AGENT_LIST
warnings.filterwarnings("ignore")


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True


def crawl_reuters_url_to_list(category):
    """
    Args:
        category (:obj: str):
            "europe-stocks", "businessnews", "worldnews", "domesticnews",
            "technologynews", "centralbanks", "innovationnews", "aerospace-defence",
            "autos-upclose", "esgnews", "stocksnews", "gca-foreignexchange",
            "gc07", "exchange-traded-funds", "specialreports", "euro-zone",
            "china-news", "japan", "politicsnews", "sciencenews", "medianews",
            "environmentnews", "mcbreakingviews", "personalfinance"
        save (:obj: str):
            Save file path.

    Returns:
        article_url_list (:obj: list):
    """
    save = "./data/{}_reuters_url.txt".format(category)
    print("Start crawling urls from every pages in Reuters...")
    file = open(save, 'wb')
    article_url_list = []
    page = 0
    pbar = tqdm()
    while True:
        page += 1
        url = "https://uk.reuters.com/news/archive/{}?view=page&page={}&pageSize=10".format(category, page)
        base_url = "https://uk.reuters.com"
        USER_AGENT = random.choice(USER_AGENT_LIST)
        headers = {'user-agent': USER_AGENT, 'Connection': 'close'}
        try:
            res = requests.get(url, headers=headers)
        except:
            # https://blog.csdn.net/a1007720052/article/details/83383220
            print("Connection refused by the server...")
            print("Let me sleep for 10 seconds")
            print("Zzzzz...")
            time.sleep(10)
            print("Was a nice sleep, now let me continue...")
            continue
        soup = BeautifulSoup(res.text, "html.parser")
        try:
            if soup.find("head").find("title").text.rstrip().lstrip() == "An Error has occured | Reuters.com":
                break
            elif soup.find("head") == None:
                break
            else:
                articles = soup.find_all("article", "story")
                for article in articles:
                    article_url = article.find("div", "story-content").find("a").get("href")
                    article_url = base_url + article_url
                    file.write((article_url+"\n").encode())
                    article_url_list.append(article_url)
                pbar.update()
        except TimeoutException:
            break
    pbar.close()
    file.close()
    return article_url_list


def get_content_from_url(url):
    USER_AGENT = random.choice(USER_AGENT_LIST)
    headers = {'user-agent': USER_AGENT}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.find("h1").text
    date = soup.find("meta", {"name": "REVISION_DATE"}).get("content")
    content = [sent.text for sent in soup.find_all("p", text=True)]
    content = "".join(content)
    return [date, title, content, url]


class FeedbackCounter:
    """
    Object to provide a feedback callback keeping track of total calls.
    Reference from http://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
    """
    def __init__(self, list_len):
        self.counter = 0
        self.list_len = list_len

    def feedback(self, r, bar_length=100, **kwargs):
        self.counter += 1
        for _ in range(self.list_len):
            percent = self.counter/self.list_len
            hashes = '█' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()
        return r


class AsynchronousCrawler:
    def __init__(self, lst, cat):
        self.urls = lst
        self.cat = cat
        self.fbc = FeedbackCounter(len(lst))

    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def asynchronous(self):
        return grequests.map(
            (grequests.get(
                u, callback=self.fbc.feedback,
                headers={'user-agent': random.choice(USER_AGENT_LIST), 'Connection': 'close'}) for u in self.urls),
                exception_handler=self.exception, size=10)

    def collate_responses(self, results):
        return [self.parse(x) for x in results if x is not None]

    def parse(self, res):
        try:
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.find("h1").text
            date = soup.find("meta", {"name": "REVISION_DATE"}).get("content")
            cat = soup.find("div", "ArticleHeader-info-container-3-6YG").find("a").text
            content = [sent.text for sent in soup.find_all("p", text=True)]
            content = "".join(content)
        except:
            date, title, content, cat = None, None, None, None
        return [date, title, content, res.url, cat]


def crawl_reuters_url_to_df(category, reuters_url, n=500):
    """
    Args:
        category (:obj: str):
            "europe-stocks", "businessnews", "worldnews", "domesticnews",
            "technologynews", "centralbanks", "innovationnews", "aerospace-defence",
            "autos-upclose", "esgnews", "stocksnews", "gca-foreignexchange",
            "gc07", "exchange-traded-funds", "specialreports", "euro-zone",
            "china-news", "japan", "politicsnews", "sciencenews", "medianews",
            "environmentnews", "mcbreakingviews", "personalfinance"
        reuters_url (:obj: list):
            List contains urls.
        n (:obj: int):
            Slice size of list.
    """

    category = "domesticnews"
    data = pd.DataFrame(columns=["Date", "Title", "Article", "URL", "Category"])
    reuters_url = open("./data/{}_reuters_url.txt".format(category)).readlines()
    for i in range(0, len(reuters_url), n):
        url_lists_temp = [x.rstrip().lstrip() for x in reuters_url[i:i+n]]
        url_lists_temp = [x.rstrip().lstrip() for x in url_lists_temp]
        crawler = AsynchronousCrawler(url_lists_temp, category)
        res = crawler.asynchronous()
        results = crawler.collate_responses(res)
        df = pd.DataFrame(results, columns=["Date", "Title", "Article", "URL", "Category"])
        print()
        print(df)
        data = pd.concat([data, df], axis=0)
        print("Let me sleep for 60 seconds")
        print("Zzzzz...")
        data.to_csv("./data/{}_reuters.csv".format(category))
        time.sleep(60)
    return data


if __name__ == "__main__":
    ls = [
        "euro-zone", "china-news", "japan", "politicsnews", "sciencenews", "medianews",
        "environmentnews", "mcbreakingviews", "personalfinance", "aerospace-defence"
    ]
    for l in ls:
        print(l)
        crawl_reuters_url_to_list(l)
