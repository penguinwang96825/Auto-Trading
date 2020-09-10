# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record
from indicator import KBar
# 定義交易商品
Product=sys.argv[1]
# 定義券商
# Broker='Masterlink_Future'
Broker='Simulator'

# 定義K棒物件
Today=datetime.datetime.now().strftime('%Y%m%d')
KBar1M=KBar(Today,1)
# 定義初始倉位
OrderRecord=Record()
# 定義突破n分鐘的高低點
BeforeTime=30
# 定義持倉最久時間(180分鐘)
HoldTime=datetime.timedelta(minutes=180)
# 移動停損點數
StopLoss=30

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格、量欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    # 將資料填入K棒
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    # 到進場時間後判斷進場
    High=KBar1M.GetHigh()
    if len(High) >= BeforeTime:
        # 取前15分鐘的高低點
        Ceil=max(High[-BeforeTime:-1])
        Floor=min(KBar1M.GetLow()[-BeforeTime:-1])
        Spread=Ceil-Floor
        # 判斷價格是否突破高低點進場
        if Price > Ceil + Spread * 0.2:
            # 進場後判斷最高價變數
            AfterOrder=Price
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 進場紀錄
            OrderRecord.Order('B',Product,Time,Price,1)
            print(Time,Price,'突破高點',Ceil+ Spread * 0.2,'順勢做多')
            GO.EndSubscribe()
        elif Price < Floor - Spread * 0.2:
            # 進場後判斷最高價變數
            AfterOrder=Price
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 進場紀錄
            OrderRecord.Order('S',Product,Time,Price,1)
            print(Time,Price,'突破低點',Floor-Spread * 0.2,'順勢做空')
            GO.EndSubscribe()


# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格、量欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    # 將資料填入K棒
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    if OrderRecord.GetOpenInterest() == 1:
        # 到出場時間後出場
        if Time >= LastOverTime:
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()       
        # 判斷移動停損
        elif Price > AfterOrder :
            AfterOrder = Price
        elif Price <= AfterOrder - StopLoss:
            # 空單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,'價格',Price,'進場後最高價',AfterOrder,'移動停損出場')
            GO.EndSubscribe()
    if OrderRecord.GetOpenInterest() == -1:
        # 到出場時間後出場
        if Time >= LastOverTime:
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()      
        # 判斷移動停損
        elif Price < AfterOrder :
            AfterOrder = Price
        elif Price >= AfterOrder + StopLoss:
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,'價格',Price,'進場後最低價',AfterOrder,'移動停損出場')
            GO.EndSubscribe()

print('全部交易紀錄',OrderRecord.GetTradeRecord())