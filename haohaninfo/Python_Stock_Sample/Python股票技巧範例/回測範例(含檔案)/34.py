# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys
import datetime
from backtest_function import GetHistoryData

#將日期以及股票代碼變成參數帶入
date=sys.argv[1]
stockid=sys.argv[2]

#取得成交資訊
Data = GetHistoryData(date,stockid)

#定義相關變數
KBar = []
InitTime = datetime.datetime.strptime('090000000000',"%H%M%S%f")
Cycle = 60

#開始進行K線計算
for i in range(len(Data)):
    time=datetime.datetime.strptime(Data[i][0],"%H%M%S%f")
    price=float(Data[i][2])
    qty=int(Data[i][3])
    if len(KBar)==0:
        KBar.append([InitTime,price,price,price,price,qty])
    else:
        if time < InitTime + datetime.timedelta(0,Cycle):
            if price > KBar[-1][2]:
                KBar[-1][2] = price
            elif price < KBar[-1][3]:
                KBar[-1][3] = price
            KBar[-1][4] = price
            KBar[-1][5] += qty
        else:
            InitTime += datetime.timedelta(0,Cycle)
            KBar.append([InitTime,price,price,price,price,qty])

print(KBar)
