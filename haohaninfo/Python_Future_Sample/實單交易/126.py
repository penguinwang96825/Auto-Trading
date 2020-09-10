# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]
# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# 設定計算價格高低點的期間
TreceStartTime = datetime.datetime.strptime(Date+'08:45:00.00','%Y%m%d%H:%M:%S.%f')
TreceEndTime = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')
# 設定停止進場時間、出場時間
StopTime = datetime.datetime.strptime(Date+'12:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')
# 設定 高低點價差的倍數、固定式停損點數、最大獲利點數、移動式停損點數
N = 0.1
FixStopLoss = 10
MaxEarn = 40
MoveStopLoss = 15
# 先定義區間高低點為極端值
MaxPrice = 0
MinPrice = 999999
Gap = 0  

# 進場前判斷
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    # 計算價格高低點
    if time >= TreceStartTime and time <= TreceEndTime:
        MaxPrice = max(MaxPrice,price)
        MinPrice = min(MinPrice,price)
        Gap = (MaxPrice - MinPrice) * N
    elif time > TreceEndTime:
        MaxPrice = max(MaxPrice,price)
        MinPrice = min(MinPrice,price)
        Gap = (MaxPrice - MinPrice) * N
        GO.EndDescribe()

# 進場策略
Index=0
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    # 進場判斷
    if time < StopTime:
        # 多單進場
        if price >= MaxPrice + Gap:
            Index=1
            OrderTime=time
            OrderPrice=price
            MaxPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 空單進場
        elif price <= MinPrice - Gap:
            Index=-1
            OrderTime=time
            OrderPrice=price
            MinPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
    # 超過可進場時間 當日不做交易
    else:
        print("Today No Order")
        GO.EndDescribe()

# 持有多單
if Index == 1:        
    # 出場策略
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        # 更新進場後最高價
        MaxPrice = max(MaxPrice,price)
        # 固定式停損
        if price <= OrderPrice-FixStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 移動式停損
        elif MaxPrice-OrderPrice >= MaxEarn and price <= MaxPrice-MoveStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 超過最後出場時間
        elif time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
# 持有空單
elif Index == -1:
    # 出場策略
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        # 更新進場後最低價
        MinPrice = min(MinPrice,price)
        # 固定式停損
        if price >= OrderPrice+FixStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 移動式停損
        elif OrderPrice-MinPrice >= MaxEarn and price >= MinPrice+MoveStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 超過最後出場時間
        elif time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()

