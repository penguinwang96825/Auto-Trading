# -*- coding: utf-8 -*-

import requests,sys
from bs4 import BeautifulSoup 

# 帶入網頁資料參數
#start_day='2019/09/01'
#end_day='2019/10/01'
start_day=sys.argv[1]
end_day=sys.argv[2]

# 取得網頁資料
html=requests.post('https://www.taifex.com.tw/cht/3/pcRatio',data={ 
            'queryStartDate': start_day,		
            'queryEndDate': end_day,
        })

# 將網頁資料解析
soup=BeautifulSoup(html.text,'html.parser')

# 取得該網頁的行情表格
table=soup.find('table', class_='table_a')

# 判斷是否有資料才進行資料讀取
if table != None:
    tmplist=[]
    # 將每行獨立取出
    for tr in table.find_all('tr'):
        tmplist1 = []
        # 將每個欄位取出
        for td in tr.findChildren(recursive=False):
            tmpobj=td.get_text().replace(',','')
            tmpobj=''.join(tmpobj.split())
            tmplist1.append(tmpobj)
        tmplist.append(tmplist1)  
    # 顯示資訊
    print(tmplist)
else:
    print('當天尚無資料')