# -*- coding: utf-8 -*-

# 載入必要套件
from indicator import GetHistoryData,KBar
import datetime,sys
strptime=datetime.datetime.strptime
from talib import SMA,BBANDS

# 取得資料
# Date='20190902'
# Product='TXFI9'
Date=sys.argv[1]
Product=sys.argv[2]
FilePath='C:/Data/'
Broker='Simulator'
Table='Match'
Data=GetHistoryData(FilePath,Broker,Date,Product,Table)

# 取特定時間的資料
Data = [ line for line in Data if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]

# 定義1分K棒的物件
MinuteKBar=KBar(Date,1)
# 計算K棒
for line in Data:
    time=strptime(line[0],"%Y/%m/%d %H:%M:%S.%f")
    price=int(line[2])
    qty=int(line[3])
    MinuteKBar.AddPrice(time,price,qty)

# 計算技術指標
CloseArray=MinuteKBar.GetClose()
# 移動平均線計算(5分K)
SMAArray=SMA(CloseArray,timeperiod=5)
print(SMAArray[:10])
# 移動平均線計算(5分K)
UpperArray,MiddleArray,LowerArray=BBANDS(CloseArray,timeperiod=5)
print(UpperArray[:10])
print(MiddleArray[:10])
print(LowerArray[:10])
