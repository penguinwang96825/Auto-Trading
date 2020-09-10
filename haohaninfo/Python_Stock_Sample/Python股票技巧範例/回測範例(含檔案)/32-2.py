# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
from backtest_function import GetHistoryData

#將日期以及股票代碼變成參數帶入
date=sys.argv[1]
stockid=sys.argv[2]

#取得成交資訊
Data = GetHistoryData(date,stockid)

#定義相關變數
BigBTrade = []
BigSTrade = []
BigValue= 10000000

#開始進行內外盤計算
for i in range(1,len(Data)):
    time=datetime.datetime.strptime(Data[i][0],"%H%M%S%f")
    price=float(Data[i][2])
    lastprice=float(Data[i-1][2])
    qty=int(Data[i][3])
    value=price*1000*qty
    if value > BigValue :
        if price>lastprice:
            BigBTrade.append([ time , price ])
        elif price<lastprice:
            BigSTrade.append([ time , price ])
        
#開始進行繪圖
#取得轉換時間字串至時間格式
Time = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in Data ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
Time1 = [ mdates.date2num(line) for line in Time ]
#價格由字串轉數值
Price = [ float(line[2]) for line in Data ]

#定義圖表物件
ax = plt.subplot(111)

#定義title
plt.title('Price&BigTrade Line')

# 繪製價格折線圖
ax.plot_date(Time1, Price, 'k-')

# 繪製買方大單點位
if len(BigBTrade)!=0:
    #取得轉換時間字串至時間格式
    BTime=[ line[0] for line in BigBTrade ]
    #將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
    BTime1 = [ mdates.date2num(line) for line in BTime ]
    #取出量能的list
    BValue=[ line[1] for line in BigBTrade ]
    # 將大單點位繪製出來
    ax.plot_date(BTime1, BValue, 'r.',markersize='8')

# 繪製賣方大單點位
if len(BigSTrade)!=0:
    #取得轉換時間字串至時間格式
    STime=[ line[0] for line in BigSTrade ]
    #將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
    STime1 = [ mdates.date2num(line) for line in STime ]
    #取出量能的list
    SValue=[ line[1] for line in BigSTrade ]
    # 將大單點位繪製出來
    ax.plot_date(STime1, SValue, 'g.',markersize='8')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(hfmt)

# 顯示繪製圖表
plt.show()
