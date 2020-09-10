# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function
import talib,numpy
import sys 

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 取得前日K棒
LastKBar=function.getDayKBarbyNum(Sid,20)
LastClose=numpy.array([ i[4] for i in LastKBar ])
DayMA=talib.MA(LastClose,timeperiod=20)[-1]

# 趨勢判斷
Trend=0
for i in function.getSIDMatch(Date,Sid):
    price=float(i[2])
    if price > DayMA:
        print('開盤大於20日MA')
        Trend=1
        break
    elif price < DayMA:
        print('開盤小於20日MA')
        Trend=-1
        break
    else:
        print('開盤等於20日MA')
        break
        
