# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import talib,numpy
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 趨勢判斷
Trend=0
TrendEndTime=datetime.datetime.strptime(Date+'09:30:00','%Y%m%d%H:%M:%S')
KBar1M=indicator.KBar(date=Date)
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    KBar1M.Add(time,price,qty)
    if time > TrendEndTime:
        startprice = KBar1M.GetOpen()[0]
        endprice = KBar1M.GetClose()[-1]
        if startprice > endprice:
            print('當日只做多單')
            Trend=1
            break
        elif startprice < endprice:
            print('當日只做空單')
            Trend=-1
            break
        else:
            print('當日趨勢不明')
            break