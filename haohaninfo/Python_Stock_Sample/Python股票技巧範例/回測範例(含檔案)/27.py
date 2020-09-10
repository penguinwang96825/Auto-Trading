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
MAarray = []
MA = []
MAValue = 0
InitTime = datetime.datetime.strptime('090000000000',"%H%M%S%f")
Cycle = 60
MAlen = 10

#開始進行MA計算
for i in Data:
    time=datetime.datetime.strptime(i[0],"%H%M%S%f")
    price=float(i[2])
    if len(MAarray)==0:
        MAarray+=[price]
    else:
        if time < InitTime + datetime.timedelta(0,Cycle):
            MAarray[-1]=price
        else:
            if len(MAarray)==MAlen:
                MAarray=MAarray[1:]+[price]
            else:
                MAarray+=[price]   
            InitTime += datetime.timedelta(0,Cycle)
    MAValue=float(sum(MAarray))/len(MAarray)
    MA.append([time.strftime("%H:%M:%S"),MAValue])

print(MA)
