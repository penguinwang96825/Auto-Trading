# -*- coding: utf-8 -*-

import requests,datetime,sys
from bs4 import BeautifulSoup 

# date='2018/06/12'
# product='TX'
date=sys.argv[1]
product=sys.argv[2]

# 取得網頁資料
html=requests.post('https://www.taifex.com.tw/cht/3/futContractsDate',data={ 
        'queryType': '1',
        'doQuery': '1',
        'queryDate': '2019/09/19',
        'commodityId': 'TXF',
        'goDay': '',
        'dateaddcnt':'' 
        })
        
# 將網頁資料解析
soup=BeautifulSoup(html.text,'html.parser')

# 取得該網頁的行情表格
table=soup.find('table', class_='table_f')

# 判斷是否有資料才進行資料讀取
if table != None:
    tmplist=[]
    # 將每行獨立取出
    for tr in table.find_all('tr'):
        # 將每行每個欄位取出
        tmpobj=tr.get_text()
        tmpobj=tmpobj.replace(',','').split()
        tmplist.append(tmpobj)
else:
    print('當天尚無資料')

# 篩選特定行數、欄位資料
tmplist=[ i[-13:] for i in tmplist][3:-4]
# tmplist=[ i[-13:] for i in tmplist][-1]

print(tmplist)