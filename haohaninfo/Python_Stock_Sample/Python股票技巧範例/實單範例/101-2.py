# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys
import numpy

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 一分鐘K棒的物件
KBar1M=indicator.KBar(date=Date)

# 定義趨勢判斷的時間
StartTime=datetime.datetime.strptime(Date+'09:30:00','%Y%m%d%H:%M:%S')

#取得前幾日的最高最低
DayNum=5
DayK=function.getDayKBarbyNum(Sid,DayNum)
DayHigh=max([ i[2] for i in DayK ])
DayLow=min([ i[3] for i in DayK ])
print('Day High:',DayHigh,'Day Low',DayLow)

# 進場判斷     
Index=0  
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    if price > DayHigh:
        Index=1
        OrderTime=time
        OrderPrice=price
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        break
    elif price < DayLow:
        Index=-1
        OrderTime=time
        OrderPrice=price
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        break