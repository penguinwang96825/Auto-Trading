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
    
# 移動停損比率
TrailingStopRatio=0.02

# 出場判斷
if Index==1:
    # 紀錄當前最高價
    TmpHigh = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpHigh * (1-TrailingStopRatio)
    # 多單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        
        # 如果價格屬於當前最高價
        if price > TmpHigh:
            # 重新計算移動停損點
            TmpHigh=price
            TrailingStop = TmpHigh * (1-TrailingStopRatio)
        elif price < TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            break
     
elif Index==-1:
    # 紀錄當前最高價
    TmpLow = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpLow * (1+TrailingStopRatio)
    # 空單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        
        # 如果價格屬於當前最高價
        if price < TmpLow:
            # 重新計算移動停損點
            TmpLow=price
            TrailingStop = TmpLow * (1+TrailingStopRatio)
        elif price > TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            break
                