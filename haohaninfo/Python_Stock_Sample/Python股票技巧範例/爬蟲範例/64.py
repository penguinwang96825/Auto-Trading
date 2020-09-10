from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

type=sys.argv[1]

html=urlopen('https://tw.stock.yahoo.com/d/i/rank.php?t='+type+'&e=tse&n=50')
soup=BeautifulSoup(html,'html.parser')

for i in soup.find_all('td',class_='name'):
    print(i.a.contents)
