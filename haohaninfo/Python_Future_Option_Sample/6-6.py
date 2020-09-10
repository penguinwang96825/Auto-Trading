# -*- coding: utf-8 -*-

import requests,sys
from bs4 import BeautifulSoup 

# 帶入網頁資料參數
# date='2018/06/12'
# product='TX'
# daynight='0'
date=sys.argv[1]
product=sys.argv[2]
daynight=sys.argv[3]

# 取得網頁資料
html=requests.post('https://www.taifex.com.tw/cht/3/futDailyMarketReport',data={ 
        'queryType': '2' ,
        'marketCode': daynight , 
        'commodity_id': product ,
        'queryDate': date ,
        'MarketCode': daynight ,
        'commodity_idt': product
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
        tmplist1 = []
        # 將每個欄位取出
        for td in tr.findChildren(recursive=False):
            tmpobj=td.get_text()
            tmpobj=''.join(tmpobj.split())
            tmplist1.append(tmpobj)
        tmplist.append(tmplist1)  
    # 顯示資訊
    print(soup.h3.get_text())
    print(tmplist)
else:
    print('當天尚無資料')
    