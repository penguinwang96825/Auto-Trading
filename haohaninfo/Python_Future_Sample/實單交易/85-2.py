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
# 設定交易趨勢
Trend = 1
# 設定突破的量
OverFill = 1200

# 逐筆計算累計成交量
Index=0
AV = indicator.AccVol(Date,1)
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    amount = int(i[4])
    AV.Add(time,amount)
    if AV.Get()[0] > OverFill :
        price=float(i[2])
        if Trend == 1 : 
            Index=1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        elif Trend == -1 : 
            Index=-1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()