from bs4 import BeautifulSoup
from urllib.request import urlopen
import sys

id=sys.argv[1]

html=urlopen('https://www.moneydj.com/z/zh/zha/ZH00.djhtm?A='+id)
soup=BeautifulSoup(html,'html.parser')

for i in soup.find_all('td',id="oAddCheckbox"):
   print(i.find('a').contents)
