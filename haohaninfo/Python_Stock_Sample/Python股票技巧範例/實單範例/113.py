# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 定義股票代碼
Sid=sys.argv[1]

# 一分鐘K棒的物件
KBar1M=indicator.KBar(date=Date)

# 定義快線、慢線、MACD的週期
FastPeriod=12
SlowPeriod=24
MACDPeriod=7

# 假設只有多單進場，本進場條件毫無意義，僅供測試
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    Index=1
    OrderTime=time
    OrderPrice=price
    print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
    break


# 出場判斷
if Index==1:
    # 多單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)   
        DIF,MACD,OSC = KBar1M.GetMACD(FastPeriod,SlowPeriod,MACDPeriod)
        # 當DIF與MACD的差額已經計算完成，才會去進行判斷
        if len(OSC) > SlowPeriod + MACDPeriod:
            ThisOSC = OSC[-1]
            LastOSC = OSC[-2]
            # 死亡交叉
            if LastOSC >= 0 and ThisOSC < 0:
                Index=0
                CoverTime=time
                CoverPrice=price
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                break
elif Index==-1:
    # 空單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)   
        DIF,MACD,OSC = KBar1M.GetMACD(FastPeriod,SlowPeriod,MACDPeriod)
        # 當DIF與MACD的差額已經計算完成，才會去進行判斷
        if len(OSC) > SlowPeriod + MACDPeriod:
            ThisOSC = OSC[-1]
            LastOSC = OSC[-2]
            # 黃金交叉
            if LastOSC <= 0 and ThisOSC > 0:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break
