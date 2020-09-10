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
LastKBar=function.getDayKBarbyNum(Sid,21)
LastClose=numpy.array([ i[4] for i in LastKBar ])
DayRSI=talib.RSI(LastClose,timeperiod=20)[-1]

# 趨勢判斷
Trend=0
if DayRSI>50:
    print('當日只做多單')
    Trend=1
elif DayRSI<50:
    print('當日只做空單')
    Trend=-1
else:
    print('當日趨勢不明')

