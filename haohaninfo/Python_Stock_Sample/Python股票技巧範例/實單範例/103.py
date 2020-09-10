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

# 定義中線的週期
BBANDSPeriod=10

# 預設趨勢為1，假設只有多單進場
Trend=1
        
# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)

    Upper,Middle,Lower = KBar1M.GetBBANDS(BBANDSPeriod)
    # 當中線已經計算完成，才會去進行判斷
    if len(Middle) >= BBANDSPeriod:
        Price = KBar1M.GetClose()
        ThisPrice = Price[-1]
        ThisUpper = Upper[-1]
        ThisLower = Lower[-1]
        LastPrice = Price[-2]
        LastUpper = Upper[-2]
        LastLower = Lower[-2]
        
        # 價格與通道下緣黃金交叉
        if Trend == 1 and LastPrice <= LastLower and ThisPrice > ThisLower:
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            break
        # 價格與通道上緣死亡交叉
        elif Trend == -1 and LastPrice >= LastUpper and ThisPrice < ThisUpper:
            Index=-1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            break
        
