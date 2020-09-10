# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record

# 定義交易商品
Product=sys.argv[1]
# 定義券商
Broker='Simulator'

# 定義初始倉位
OrderRecord=Record()
# 定義要進出場的時間(9:00進場 13:30出場)
InTime=datetime.datetime.now().replace( hour=9 , minute=00 , second=00 , microsecond=00 )
OutTime=datetime.datetime.now().replace( hour=13 , minute=30 , second=00 , microsecond=00 )

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 到進場時間後進場
    if Time >= InTime:
        # 進場多單
        OrderRecord.Order('B',Product,Time,Price,1)
        print(Time,'時間到進場')
        GO.EndSubscribe()

# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 到出場時間後出場
    if Time >= OutTime:
        # 空單出場
        OrderRecord.Cover('S',Product,Time,Price,1)
        print(Time,'時間到出場')
        GO.EndSubscribe()
        
print('全部交易紀錄',OrderRecord.GetTradeRecord())