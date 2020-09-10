# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]
# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# 設定進出場時間
StartTime = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')
# 設定停損
StopLoss = 30

# 進場策略
Index=0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    # 當前時間 超過 進場時間
    if time >= StartTime:
        # 取最近一筆成交資訊，當作預設成交價格
        data = GO.DescribeLast(Broker, 'commission', Prod)
        time = datetime.datetime.strptime(data[0],'%Y/%m/%d %H:%M:%S.%f')
        # 買賣方平均每筆委託口數
        AvgBuy = int(data[3]) / int(data[2])
        AvgSell = int(data[5]) / int(data[4])
        # 多單進場
        if AvgBuy > AvgSell:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 空單進場
        elif AvgBuy < AvgSell:
            Index=-1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 尚無趨勢
        else:
            continue
    
if Index == 1:    
    # 出場策略
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        # 價格停損
        if price < OrderPrice - StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 當前時間 超過 出場時間
        if time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
if Index == -1:    
    # 出場策略
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        # 價格停損
        if price > OrderPrice + StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()     
        # 當前時間 超過 出場時間
        if time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()           

