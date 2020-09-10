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

# 假設只有多單進場，本進場條件毫無意義，僅供測試
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    Index=1
    OrderTime=time
    OrderPrice=price
    print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
    break

# 停損停利比率
StopLossRatio=0.02
TakeProfitRatio=0.03
# 出場判斷
if Index==1:
    # 多單出場判斷
    StopLoss=OrderPrice*(1-StopLossRatio)
    TakeProfit=OrderPrice*(1+TakeProfitRatio)
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        # 當價格高於停利價
        if price > TakeProfit:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy TakeProfit Price:",CoverPrice,"Success!")
            break
        # 當價格低於停損價
        elif price < StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy StopLoss Price:",CoverPrice,"Success!")
            break
            
            
elif Index==-1:
    # 空單出場判斷
    StopLoss=OrderPrice*(1+StopLossRatio)
    TakeProfit=OrderPrice*(1-TakeProfitRatio)
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        # 當價格低於停利價
        if price < TakeProfit:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell TakeProfit Price:",CoverPrice,"Success!")
            break
        # 當價格高於停損價
        elif price > StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell StopLoss Price:",CoverPrice,"Success!")
            break