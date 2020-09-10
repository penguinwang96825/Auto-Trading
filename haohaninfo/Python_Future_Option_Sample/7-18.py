# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record

# 定義交易商品
Product=sys.argv[1]
# 定義券商
Broker='Simulator'

# 定義初始倉位
OrderRecord=Record()
# 停損停利點數
StopLoss=10
TakeProfit=10

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 無條件進場多單
    OrderPrice=Price
    OrderRecord.Order('B',Product,Time,Price,1)
    print(Time,'價格',Price,'無條件進場多單')
    GO.EndSubscribe()

# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 停損出場
    if Price <= OrderPrice - StopLoss:
        # 空單出場
        OrderRecord.Cover('S',Product,Time,Price,1)
        print(Time,'價格',Price,'停損出場')
        GO.EndSubscribe()
    # 停利出場
    if Price >= OrderPrice + TakeProfit:
        # 空單出場
        OrderRecord.Cover('S',Product,Time,Price,1)
        print(Time,'價格',Price,'停利出場')
        GO.EndSubscribe()
        
print('全部交易紀錄',OrderRecord.GetTradeRecord())