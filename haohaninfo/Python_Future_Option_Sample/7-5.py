# -*- coding: utf-8 -*-
import sys,haohaninfo 
from indicator import getOptionDailyInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProduct=sys.argv[1]
# 定義交易商品
Product=sys.argv[2]
# 定義券商
Broker='Simulator'

# 取得選擇權未平倉資料
Data=getOptionDailyInfo(WebProduct,1)
# 找出未平倉量最高的買賣權
Call=[ i for i in Data if i[4]=='Call']
Put=[ i for i in Data if i[4]=='Put']
Call.sort(key = lambda x: int(x[-1]))
Put.sort(key = lambda x: int(x[-1]))
# 壓力價位
Ceil=float(Call[-1][3])
# 支撐價位
Floor=float(Put[-1][3])
print('壓力：',Ceil,'支撐：',Floor)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得價格欄位
    Price=float(row[2])
    # 突破壓力價位
    if Price > Ceil:
        print('當前價突破壓力價位，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()
    elif Price < Floor:
        print('當前價突破支撐價位，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()