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

# 定義RSI指標、快線、慢線的週期
RSIPeriod=14
FastPeriod=5
SlowPeriod=15

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
        RSI = KBar1M.GetRSI(RSIPeriod)
        SlowMA = KBar1M.GetSMA(SlowPeriod)
        # 當RSI指標及慢線皆已計算完成，才會去進行判斷
        if len(RSI) >= RSIPeriod and len(SlowMA) >= SlowPeriod+1:
            RSI = RSI[-1]
            FastMA = KBar1M.GetSMA(FastPeriod)
            ThisFastMA = FastMA[-1]
            ThisSlowMA = SlowMA[-1]
            LastFastMA = FastMA[-2]
            LastSlowMA = SlowMA[-2]
            # RSI指標趨勢偏空且均線死亡交叉
            if RSI < 50 and LastFastMA >= LastSlowMA and ThisFastMA < ThisSlowMA:
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
        RSI = KBar1M.GetRSI(RSIPeriod)
        SlowMA = KBar1M.GetSMA(SlowPeriod)
        # 當RSI指標及慢線皆已計算完成，才會去進行判斷
        if len(RSI) >= RSIPeriod and len(SlowMA) >= SlowPeriod+1:
            RSI = RSI[-1]
            FastMA = KBar1M.GetSMA(FastPeriod)
            ThisFastMA = FastMA[-1]
            ThisSlowMA = SlowMA[-1]
            LastFastMA = FastMA[-2]
            LastSlowMA = SlowMA[-2]
            # RSI指標趨勢偏多且均線黃金交叉
            if RSI > 50 and LastFastMA <= LastSlowMA and ThisFastMA > ThisSlowMA:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break



