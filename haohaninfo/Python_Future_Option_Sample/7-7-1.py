# -*- coding: utf-8 -*-
import sys,haohaninfo 
from indicator import getFutureDailyInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProduct=sys.argv[1]
# 定義交易商品
Product=sys.argv[2]
# 定義券商
Broker='Simulator'

# 取得期貨行情資料
DailyInfo=getFutureDailyInfo(WebProduct,1)[0]
DailyTime,DailyHigh,DailyLow,DailyClose=DailyInfo[0],float(DailyInfo[4]),float(DailyInfo[5]),float(DailyInfo[6])

# 計算 Pivot Point
PP=(DailyHigh+DailyLow+DailyClose)/3
R3=DailyHigh+(2*(PP-DailyLow))
R2=PP+DailyHigh-DailyLow
R1=(PP*2)-DailyLow
S1=(PP*2)-DailyHigh
S2=PP-DailyHigh+DailyLow
S3=DailyLow+(2*(DailyHigh-PP))
print('R1',R1,'S1',S1)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得價格欄位
    Price=float(row[2])
    # 突破壓力支撐價位
    if Price > R1:
        print('當前價',Price,'突破Pivot Point R1壓力價位',R1,'，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()
    elif Price < S1:
        print('當前價',Price,'突破Pivot Point S1支撐價位',S1,'，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()



