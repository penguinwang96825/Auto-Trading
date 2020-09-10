# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 一分鐘K棒的物件
KBar1M=indicator.KBar(date=Date)

# 定義快線、慢線的週期
FastPeriod=5
SlowPeriod=15

# 預設趨勢為1，假設只有多單進場
Trend=1

# 進場判斷
CrossTime=None
Interval=datetime.timedelta(minutes=5)
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    SlowMA = KBar1M.GetSMA(SlowPeriod)
    # 當慢線已經計算完成，才會去進行判斷
    if len(SlowMA) > SlowPeriod+1:
        FastMA = KBar1M.GetSMA(FastPeriod)
        ThisFastMA = FastMA[-1]
        ThisSlowMA = SlowMA[-1]
        LastFastMA = FastMA[-2]
        LastSlowMA = SlowMA[-2]

        # 黃金交叉
        if Trend==1 and LastFastMA <= LastSlowMA and ThisFastMA > ThisSlowMA:
            # 判斷是否第二次交叉 並且超過指定時間間隔
            if CrossTime is None:
                CrossTime=time+Interval
            elif time > CrossTime :
                Index=1
                OrderTime=time
                OrderPrice=price   
                print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
                break
        # 死亡交叉
        elif Trend==-1 and LastFastMA >= LastSlowMA and ThisFastMA < ThisSlowMA:
            # 判斷是否第二次交叉 並且超過指定時間間隔
            if CrossTime is None:
                CrossTime=time+Interval
            elif time > CrossTime :
                Index=-1
                OrderTime=time
                OrderPrice=price 
                print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
                break
