# -*- coding: utf-8 -*-
import sys,haohaninfo
from indicator import getFutureDailyInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProduct=sys.argv[1]
# 定義交易商品
Product=sys.argv[2]
# 定義券商
Broker='Simulator'

# 取得最前一日的行情資料、近月商品
LastDailyInfo=getFutureDailyInfo(WebProduct,1)[0]
# 取得前日收盤價
LastDailyClosePrice=int(LastDailyInfo[6])

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得第一筆報價即跳出該迴圈
    Price=float(row[2])
    # 結束訂閱報價
    GO.EndSubscribe()

# 判斷開盤跳空
if Price > LastDailyClosePrice:
    print('向上跳空',Price - LastDailyClosePrice,'點')
elif Price < LastDailyClosePrice:
    print('向上跳空',LastDailyClosePrice - Price,'點')
else:
    print('無跳空缺口')
    

