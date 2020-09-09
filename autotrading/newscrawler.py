import data_handler
import requests
import grequests
import warnings
import time
import random
import pandas as pd
import numpy as np
from multiprocessing import Pool
from tqdm import tqdm
from bs4 import BeautifulSoup
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


def crawl_reuters_pages():
    file = open("./data/reuters_url.txt", 'wb')
    article_url_list = []
    page = 0
    pbar = tqdm()
    while True:
        page += 1
        url = "https://uk.reuters.com/news/archive/businessnews?view=page&page={}&pageSize=10".format(page)
        base_url = "https://uk.reuters.com"
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        try:
            articles = soup.find_all("article", "story")
            for article in articles:
                article_url = article.find("div", "story-content").find("a").get("href")
                article_url = base_url + article_url
                file.write((article_url+"\n").encode())
                article_url_list.append(article_url)
            pbar.update()
        except:
            print(page)
            break
    tqdm.close()
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
    """Object to provide a feedback callback keeping track of total calls."""
    def __init__(self):
        self.counter = 0

    def feedback(self, r, **kwargs):
        self.counter += 1
        print("{0} fetched, {1} total.".format(r.url, self.counter))
        return r


class AsynchronousCrawler:
    def __init__(self, lst):
        self.urls = lst
        self.fbc = FeedbackCounter()

    def exception(self, request, exception):
        print("Problem: {}: {}".format(request.url, exception))

    def asynchronous(self):
        return grequests.map(
            (grequests.get(u, callback=self.fbc.feedback) for u in self.urls),
            exception_handler=self.exception, size=10)

    def collate_responses(self, results):
        return [self.parse(x.text) for x in results if x is not None]

    def parse(self, response_text):
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.find("h1").text
        date = soup.find("meta", {"name": "REVISION_DATE"}).get("content")
        content = [sent.text for sent in soup.find_all("p", text=True)]
        content = "".join(content)
        return [date, title, content, url]


if __name__ == "__main__":
    reuters_url = open("./data/reuters_url.txt").readlines()
    url_lists = [x.rstrip().lstrip() for x in reuters_url]
    crawler = AsynchronousCrawler(url_lists)
    res = crawler.asynchronous()
    results = crawler.collate_responses(res)
    data = pd.DataFrame(results)
    data.to_csv("./data/reuters.csv")
