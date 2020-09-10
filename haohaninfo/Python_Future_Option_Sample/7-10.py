# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record
from indicator import KBar
# 定義交易商品
Product=sys.argv[1]
# 定義券商
Broker='Simulator'

# 定義K棒物件
Today=datetime.datetime.now().strftime('%Y%m%d')
KBar1M=KBar(Today,1)
# 定義初始倉位
OrderRecord=Record()
# 定義要進出場的時間(9:15進場 13:30出場)
InTime=datetime.datetime.now().replace( hour=9 , minute=15 , second=00 , microsecond=00 )
OutTime=datetime.datetime.now().replace( hour=13 , minute=30 , second=00 , microsecond=00 )

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    # 到進場時間後判斷進場
    if Time >= InTime:
        High=KBar1M.GetHigh()
        if len(High) >= 15:
            # 取前15分鐘的高低點
            Ceil=max(High[-15:-1])
            Floor=min(KBar1M.GetLow()[-15:-1])
            # 判斷價格是否突破高低點進場
            if Price > Ceil:
                OrderRecord.Order('B',Product,Time,Price,1)
                print(Time,Price,'突破高點',Ceil,'順勢做多')
                GO.EndSubscribe()
            elif Price < Floor:
                OrderRecord.Order('S',Product,Time,Price,1)
                print(Time,Price,'突破低點',Floor,'順勢做空')
                GO.EndSubscribe()
        
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

print('全部交易紀錄',OrderRecord.GetTradeRecord())