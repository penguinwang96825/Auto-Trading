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
# 定義中線的週期
BBANDSPeriod=10
# 定義價格停損
StopLoss = 20
# 設定停止進場時間、出場時間、跳出迴圈時間
StopTime = datetime.datetime.strptime(Date+'13:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')
BreakTime = datetime.datetime.strptime(Date+'13:25:00.00','%Y%m%d%H:%M:%S.%f')

# 當日多次進出場
BreakFlag = False
while BreakFlag == False:
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
            
        Upper,Middle,Lower = KBar.GetBBANDS(BBANDSPeriod)
        # 當中線已經計算完成，才會去進行判斷
        if len(Middle) >= BBANDSPeriod+tag:
            Price = KBar.GetClose()
            ThisPrice,ThisUpper,ThisLower,LastPrice,LastUpper,LastLower = Price[-1-tag],Upper[-1-tag],Lower[-1-tag],Price[-2-tag],Upper[-2-tag],Lower[-2-tag]
            
            # 價格與通道下緣黃金交叉
            if LastPrice <= LastLower and ThisPrice > ThisLower:
                Index=1
                OrderTime=time
                OrderPrice=price
                print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
                GO.EndDescribe()
            # 價格與通道上緣死亡交叉
            elif LastPrice >= LastUpper and ThisPrice < ThisUpper:
                Index=-1
                OrderTime=time
                OrderPrice=price
                print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
                GO.EndDescribe()
            # 最後進場時間
            elif time > StopTime:
                print("Today No Order")
                GO.EndDescribe()
        # 當日已結束 不繼續交易
        elif time > BreakTime:
            BreakFlag = True
        
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
                
            Upper,Middle,Lower = KBar.GetBBANDS(BBANDSPeriod)
            # 當中線已經計算完成，才會去進行判斷
            if len(Middle) >= BBANDSPeriod+tag:
                Price = KBar.GetClose()
                ThisPrice,ThisUpper,LastPrice,LastUpper = Price[-1-tag],Upper[-1-tag],Price[-2-tag],Upper[-2-tag]
                # 價格與通道上緣黃金交叉
                if LastPrice <= LastUpper and ThisPrice > ThisUpper:
                    Index=0
                    CoverTime=time
                    CoverPrice=price
                    print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                    GO.EndDescribe()
                # 固定式停損
                elif price <= OrderPrice - StopLoss :
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
                
            Upper,Middle,Lower = KBar.GetBBANDS(BBANDSPeriod)
            # 當中線已經計算完成，才會去進行判斷
            if len(Middle) >= BBANDSPeriod+tag:
                Price = KBar.GetClose()
                ThisPrice,ThisUpper,LastPrice,LastUpper = Price[-1-tag],Upper[-1-tag],Price[-2-tag],Upper[-2-tag]
                # 價格與通道下緣死亡交叉
                if LastPrice >=LastLower and ThisPrice < ThisLower:
                    Index=0
                    CoverTime=time
                    CoverPrice=price            
                    print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                    GO.EndDescribe()
                # 固定式停損
                elif price >= OrderPrice + StopLoss :
                    Index=0
                    CoverTime=time
                    CoverPrice=price            
                    print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                    GO.EndDescribe()
                # 最後出場時間
                elif time > EndTime:
                    Index=0
                    CoverTime=time
                    CoverPrice=price
                    print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                    GO.EndDescribe() 