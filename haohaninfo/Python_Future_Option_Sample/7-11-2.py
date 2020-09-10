# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record
from indicator import AccVol
# 定義交易商品
Product=sys.argv[1]
# 定義券商
Broker='Simulator'

# 定義初始倉位
OrderRecord=Record()
# 定義逐筆累計量(1分鐘)
TickVolume=AccVol(1)
# 定義爆量口數
BigOrder=1000

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位、總量欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Amount=int(row[4])
    # 計算逐筆累計量
    TickVolume.Add(Time,Price,Amount)
    PriceDiff,Volume=TickVolume.Get()
    print(Volume,PriceDiff)
    # 定義爆量進場
    if Volume > BigOrder:
        if PriceDiff > 0:
            OrderRecord.Order('B',Product,Time,Price,1)
            print(Time,'爆量',Volume,'多單進場')
            GO.EndSubscribe()
        elif PriceDiff < 0:
            OrderRecord.Order('S',Product,Time,Price,1)
            print(Time,'爆量',Volume,'空單進場')
            GO.EndSubscribe()


# 定義要出場的時間(13:30出場)
OutTime=datetime.datetime.now().replace( hour=13 , minute=30 , second=00 , microsecond=00 )
        
# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 到出場時間後出場
    if Time >= OutTime:
        if OrderRecord.GetOpenInterest() == 1:
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()       
        if OrderRecord.GetOpenInterest() == -1:
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()     
            
        
