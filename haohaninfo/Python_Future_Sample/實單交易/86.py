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
# K棒物件
KBar = indicator.KBar(Date,'time',1)
# 定義趨勢判斷的時間
StartTime=datetime.datetime.strptime(Date+'09:00:00','%Y%m%d%H:%M:%S')

# 進場前判斷
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    tag=KBar.TimeAdd(time,price,qty)
    
    # 如果時間到達指定的時間
    if time > StartTime:
        # 則取出當前最高以及最低
        High=max(KBar.GetHigh())
        Low=min(KBar.GetLow())
        Spread=High-Low
        GO.EndDescribe()

# 進場判斷 
Index=0
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    tag=KBar.TimeAdd(time,price,qty)
    
    if price > High:
        Index=1
        OrderTime=time
        OrderPrice=price    
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        GO.EndDescribe()
    elif price < Low:
        Index=-1
        OrderTime=time
        OrderPrice=price    
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        GO.EndDescribe()
                
                
                