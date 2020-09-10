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

# 計算 CDP
CDP=(DailyHigh+DailyLow+DailyClose)/3
AH=CDP+DailyHigh-DailyLow
NH=2*CDP-DailyLow
NL=2*CDP-DailyHigh
AL=CDP-DailyHigh+DailyLow
print('NH',NH,'NL',NL)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得價格欄位
    Price=float(row[2])
    # 突破壓力支撐價位
    if Price > NH:
        print('當前價',Price,'突破壓力價位',NH,'，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()
    elif Price < NL:
        print('當前價',Price,'突破支撐價位',NL,'，代表可能反轉或有趨勢發生')
        GO.EndSubscribe()
