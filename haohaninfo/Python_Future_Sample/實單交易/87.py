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
# 定義快線、慢線、MACD的週期
FastPeriod=12
SlowPeriod=24
MACDPeriod=7
# 預設趨勢為1，假設只有多單進場
Trend=1

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
    
    DIF,MACD,OSC = KBar.GetMACD(FastPeriod,SlowPeriod,MACDPeriod)
    # 當DIF與MACD的差額已經計算完成，才會去進行判斷
    if len(OSC) > SlowPeriod + MACDPeriod:
        ThisOSC = OSC[-1-tag]
        LastOSC = OSC[-2-tag]

       # OSC 大於 0 做多
        if Trend == 1 and LastOSC <= 0 and ThisOSC > 0:
            Index=1
            OrderTime=time
            OrderPrice=price   
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
       # OSC 小於 0 做空
        elif Trend == -1 and LastOSC >= 0 and ThisOSC < 0:
            Index=-1
            OrderTime=time
            OrderPrice=price   
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
