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

# 假設只有多單進場，本進場條件毫無意義，僅供測試
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    Index=1
    OrderTime=time
    OrderPrice=price
    print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
    GO.EndDescribe()
    
# 移動停損點數
StopLoss=20

# 出場判斷
if Index==1:
    # 紀錄當前最高價
    TmpHigh = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpHigh-StopLoss
    # 多單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty)
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
        
        # 如果價格屬於當前最高價
        if price > TmpHigh:
            # 重新計算移動停損點
            TmpHigh=price
            TrailingStop = TmpHigh-StopLoss
        elif price <= TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
     
elif Index==-1:
    # 紀錄當前最低價
    TmpLow = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpLow+StopLoss
    # 空單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty)
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
        
        # 如果價格屬於當前最低價
        if price < TmpLow:
            # 重新計算移動停損點
            TmpLow=price
            TrailingStop = TmpLow+StopLoss
        elif price >= TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()