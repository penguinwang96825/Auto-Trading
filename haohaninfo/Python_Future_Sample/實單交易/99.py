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
# 定義RSI指標
RSIPeriod=12

# 本進場條件是RSI>50做多、此外做空，僅供測試
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    tag=KBar.TimeAdd(time,price,qty)
    
    # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
    if tag != 1:
        continue
        
    RSI = KBar.GetRSI(RSIPeriod)
    # 當RSI指標已計算完成，才會去進行判斷
    if len(RSI) > RSIPeriod:
        RSI = RSI[-1-tag]    
        if RSI > 50:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        else:
            Index=-1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
            
# 出場判斷
if Index==1:
    # 多單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty)    
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
        
        RSI = KBar.GetRSI(RSIPeriod)
        # 當RSI指標已計算完成，才會去進行判斷
        if len(RSI) > RSIPeriod:
            RSI = RSI[-1-tag]
            # RSI指標趨勢偏空
            if RSI < 30:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            elif RSI > 80 :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
elif Index==-1:
    # 空單出場判斷
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        tag=KBar.TimeAdd(time,price,qty) 
        
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        if tag != 1:
            continue
            
        RSI = KBar.GetRSI(RSIPeriod)
        # 當RSI指標已計算完成，才會去進行判斷
        if len(RSI) > RSIPeriod :
            RSI = RSI[-1-tag]
            # RSI指標趨勢偏多
            if RSI > 70:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            elif RSI < 20 :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()