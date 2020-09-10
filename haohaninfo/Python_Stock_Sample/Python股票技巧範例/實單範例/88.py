# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function
import sys 

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 取得前日K棒
LastKBar=function.getDayKBarbyNum(Sid,1)
LastClose=LastKBar[-1][4]

# 趨勢判斷
Trend=0
for i in function.getSIDMatch(Date,Sid):
    price=float(i[2])
    if price > LastClose:
        print('開盤向上跳空')
        Trend=1
        break
    elif price < LastClose:
        print('開盤向下跳空')
        Trend=-1
        break
    else:
        print('無跳空缺口')
        break
        
