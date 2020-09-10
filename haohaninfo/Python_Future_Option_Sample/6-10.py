# -*- coding: utf-8 -*-

import requests,sys
from bs4 import BeautifulSoup 

# 帶入網頁資料參數
# date='2019/09/23'
# product='TXO'
# daynight='0'
date=sys.argv[1]
product=sys.argv[2]
daynight=sys.argv[3]

# 取得網頁資料
html=requests.post('https://www.taifex.com.tw/cht/3/optDailyMarketReport',data={ 
        'queryType': '1',
        'marketCode': daynight,	
        'commodity_id': product,
        'queryDate': date ,	
        'MarketCode': daynight,		
        'commodity_idt': product
        })

# 將網頁資料解析
soup=BeautifulSoup(html.text,'html.parser')

# 判斷是否有資料才進行資料讀取
if '查無資料' not in str(soup):
    tmplist=[]
    # 將每行獨立取出
    for tr in soup.find_all('tr'):
        tmpobj=tr.get_text().split()
        if len(tmpobj)>0 and tmpobj[0]==product:
            tmplist.append(tmpobj)  
    # 顯示資訊
    print(soup.h3.get_text())
    print(tmplist)
else:
    print('當天尚無資料')
    