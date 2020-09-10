from bs4 import BeautifulSoup
from urllib.request import urlopen

html=urlopen('http://jow.win168.com.tw/z/zm/zmd/zmdb.djhtm').read().decode('cp950')
soup=BeautifulSoup(html,"html.parser")
table = soup.find('table',class_='t01')


for i in table.find_all('tr'):
    if i.a is not None:
        print(i.a.text)
