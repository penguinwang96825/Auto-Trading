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

# 定義乖離率的週期、正乖離率臨界值、負乖離率臨界值
BIASPeriod=10
Positive=0.05
Negative=-0.05

# 預設趨勢為1，假設只有多單進場
Trend=1

# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)

    BIAS = KBar1M.GetBIAS(BIASPeriod)
    # 當乖離率已經計算完成，才會去進行判斷
    if len(BIAS) >= BIASPeriod:
        BIAS = BIAS[-1]

        # 超過負乖離率臨界值
        if Trend == 1 and BIAS <= Negative:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            break
        # 超過正乖離率臨界值
        elif Trend == -1 and BIAS >= Positive:
            Index=-1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            break
        


