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
# 定義乖離率的週期、正乖離率臨界值、負乖離率臨界值
BIASPeriod=10
Positive=0.001
Negative=-0.001
# 設定停止進場時間、出場時間
StopTime = datetime.datetime.strptime(Date+'11:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:00:00.00','%Y%m%d%H:%M:%S.%f')

# 進場策略
Index = 0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    qty = int(i[3])
    # 更新K棒
    tag = KBar.TimeAdd(time,price,qty)
 
    # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
    if tag != 1:
        continue

    BIAS = KBar.GetBIAS(BIASPeriod)
    # 當乖離率已經計算完成，才會去進行判斷
    if len(BIAS) >= BIASPeriod+1+tag:
        # 定義買賣筆數
        B_Order = int(i[5])
        S_Order = int(i[6])
        # 取得乖離率
        ThisBIAS = BIAS[-1-tag]
        LastBIAS = BIAS[-2-tag]
        # 1. 回落正乖離率臨界值，做空單
        # 2. 當買筆大於賣筆，代表賣方平均口數較大，做空單
        # 3. 同時成立做空單
        if LastBIAS >= Positive and ThisBIAS < Positive and B_Order > S_Order :
            Index=-1
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Order Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 1. 回落負乖離率臨界值，做多單
        # 2. 當買筆小於賣筆，代表買方平均口數較大，做多單
        # 3. 同時成立做多單
        elif LastBIAS <= Negative and ThisBIAS > Negative and B_Order < S_Order :
            Index=1
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Order Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 指定時間尚未進場則該日不進場
        elif time > StopTime :
            print("Today No Order")
            GO.EndDescribe()
       
# 出場策略
if Index == 1:
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price = float(i[2])
        qty = int(i[3])
        # 更新K棒
        tag = KBar.TimeAdd(time,price,qty)
     
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        # if tag != 1:
            # continue
     
        BIAS = KBar.GetBIAS(BIASPeriod)
        # 當乖離率已經計算完成，才會去進行判斷
        if len(BIAS) >= BIASPeriod+tag:
            # 定義買賣筆數
            B_Order = int(i[5])
            S_Order = int(i[6])
            # 取得乖離率
            BIAS = BIAS[-1-tag]
            # 持有多單，若乖離率大於正乖離界線則出場
            if  BIAS > Positive :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 累計成交買方筆數 大於 賣方筆數，反轉出場
            elif B_Order > S_Order:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 13:00強制出場
            elif time > EndTime :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                GO.EndDescribe()
elif Index == -1:
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price = float(i[2])
        qty = int(i[3])
        # 更新K棒
        tag = KBar.TimeAdd(time,price,qty)
     
        # 更新K棒才判斷，若要逐筆判斷則 註解下面兩行
        # if tag != 1:
            # continue
     
        BIAS = KBar.GetBIAS(BIASPeriod)
        # 當乖離率已經計算完成，才會去進行判斷
        if len(BIAS) >= BIASPeriod+tag:
            # 定義買賣筆數
            B_Order = int(i[5])
            S_Order = int(i[6])
            # 取得乖離率
            BIAS = BIAS[-1-tag]
            # 持有空單，若乖離率小於負乖離界線則出場
            if BIAS < Negative :
                Index=-1
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 累計成交買方筆數 小於 賣方筆數，反轉出場
            elif B_Order < S_Order:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                GO.EndDescribe()
            # 13:00強制出場
            elif time > EndTime :
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                GO.EndDescribe()




       
