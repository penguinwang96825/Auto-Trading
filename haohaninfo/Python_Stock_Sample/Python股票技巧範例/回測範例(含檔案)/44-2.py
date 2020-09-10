# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys
from backtest_function import GetHistoryData,DayList

#將股票代碼變成參數帶入
stockid=sys.argv[1]

#定義績效
TotalProfit=[]

#透過每天的日期進行股票歷史回測
for date in DayList():
    
    #取得成交資訊
    Data = GetHistoryData(date,stockid)

    #取得進出場時間以及價格
    OrderTime=Data[0][0]
    OrderPrice=float(Data[0][2])
    CoverTime=Data[-1][0]
    CoverPrice=float(Data[-1][2])

    #計算績效以及總績效
    Profit=CoverPrice-OrderPrice
    TotalProfit+=[Profit]
    
    print(date,sid,'Buy OrderTime',OrderTime,'OrderPrice',OrderPrice,'CoverTime',CoverTime,'CoverPrice',CoverPrice,'Profit',Profit)
    
#顯示總績效
print('Total Profit',sum(TotalProfit))
    