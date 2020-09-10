# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 定義股票代碼
Sid=sys.argv[1]

# 定義內外盤指標
BSPower2= indicator.BSPower2()

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
        ask=float(i[5])
        bid=float(i[6])
        BSPower2.Add(price,qty,ask,bid)
        sig = BSPower2.Get()
        # 內外盤反轉 出場
        if sig[0] < sig[1]:
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
        ask=float(i[5])
        bid=float(i[6])
        BSPower2.Add(price,qty,ask,bid)
        sig = BSPower2.Get()
        # 內外盤反轉 出場
        if sig[0] > sig[1]:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            break