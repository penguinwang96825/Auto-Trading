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
# 定義RSI指標、MA快線、MA慢線的週期
RSIPeriod=20
FastPeriod=8
SlowPeriod=12
# 定義RSI進場 停利 停損
RSI_Order_Point=50
RSI_TakeProfit=35
RSI_StopLoss=20
# 設定停止進場時間、出場時間
StopTime = datetime.datetime.strptime(Date+'12:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')

# 進場判斷
Index=0
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
    SlowMA = KBar.GetSMA(SlowPeriod)
    # 當RSI指標及慢線皆已計算完成，才會去進行判斷
    if len(RSI) >= RSIPeriod+tag and len(SlowMA) >= SlowPeriod+1+tag:
        RSI = RSI[-1-tag]
        FastMA = KBar.GetSMA(FastPeriod)
        ThisFastMA,ThisSlowMA,LastFastMA,LastSlowMA = FastMA[-1-tag],SlowMA[-1-tag],FastMA[-2-tag],SlowMA[-2-tag]

        # RSI指標趨勢偏多且均線黃金交叉
        if RSI > RSI_Order_Point and RSI < RSI_Order_Point + RSI_TakeProfit and LastFastMA <= LastSlowMA and ThisFastMA > ThisSlowMA:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # RSI指標趨勢偏空且均線死亡交叉
        elif RSI < RSI_Order_Point and RSI > RSI_Order_Point - RSI_TakeProfit and LastFastMA >= LastSlowMA and ThisFastMA < ThisSlowMA:
            Index=-1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 最後進場時間
        elif time > StopTime:
            print("Today No Order")
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
        if len(RSI) >= RSIPeriod+tag:
            RSI = RSI[-1-tag]
            # RSI指標停利
            if RSI > RSI_Order_Point + RSI_TakeProfit :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            elif RSI < RSI_Order_Point - RSI_StopLoss :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 最後出場時間
            elif time > EndTime:
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
        if len(RSI) >= RSIPeriod+tag:
            RSI = RSI[-1-tag]
            # RSI指標趨勢偏多
            if RSI < RSI_Order_Point - RSI_TakeProfit:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            elif RSI > RSI_Order_Point + RSI_StopLoss :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 最後出場時間
            elif time > EndTime:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
       
