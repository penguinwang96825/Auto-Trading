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

# 定義趨勢判斷的時間
StartTime=datetime.datetime.strptime(Date+'09:30:00','%Y%m%d%H:%M:%S')

# 進場前判斷
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    # 如果時間到達指定的時間
    if time > StartTime:
        # 則取出當前最高以及最低
        High=max(KBar1M.GetHigh())
        Low=min(KBar1M.GetLow())
        Spread=High-Low
        break

# 進場判斷 
Index=0      
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    if price > High:
        Index=1
        OrderTime=time
        OrderPrice=price    
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        break
    elif price < Low:
        Index=-1
        OrderTime=time
        OrderPrice=price    
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        break
                
                
                