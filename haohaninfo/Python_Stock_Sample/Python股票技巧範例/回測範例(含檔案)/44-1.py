# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys
from backtest_function import GetHistoryData

#將日期以及股票代碼變成參數帶入
date=sys.argv[1]
stockid=sys.argv[2]

#取得成交資訊
Data = GetHistoryData(date,stockid)

#取得進出場時間以及價格
OrderTime=Data[0][0]
OrderPrice=float(Data[0][2])
CoverTime=Data[-1][0]
CoverPrice=float(Data[-1][2])

print(stockid,'Buy OrderTime',OrderTime,'OrderPrice',OrderPrice,'CoverTime',CoverTime,'CoverPrice',CoverPrice,'Profit',CoverPrice-OrderPrice)