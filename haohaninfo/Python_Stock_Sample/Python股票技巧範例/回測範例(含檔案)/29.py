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
Volumn = []
InitTime = datetime.datetime.strptime('090000000000',"%H%M%S%f")
Cycle = 60

#開始進行量能計算
for i in range(len(Data)):
    time=datetime.datetime.strptime(Data[i][0],"%H%M%S%f")
    qty=int(Data[i][3])
    if len(Volumn)==0:
        Volumn.append([InitTime,qty])
    else:
        if time < InitTime + datetime.timedelta(0,Cycle):
            Volumn[-1][1] += qty
        else:
            InitTime += datetime.timedelta(0,Cycle)
            Volumn.append([InitTime,qty])

#開始進行繪圖
#取得轉換時間字串至時間格式
Time = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in Data ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
Time1 = [ mdates.date2num(line) for line in Time ]
#價格由字串轉數值
Price = [ float(line[2]) for line in Data ]

#定義圖表物件
fig = plt.figure(1) 		#第一張圖片 Q             
ax1 = fig.add_subplot(211)

#定義title
plt.title('Price&Volumn Line')

# 繪製價格折線圖
ax1.plot_date(Time1, Price, 'k-')

#取得轉換時間字串至時間格式
QTime=[ line[0] for line in Volumn ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
QTime1 = [ mdates.date2num(line) for line in QTime ]
#取出量能的list
QValue=[ line[1] for line in Volumn ]

#定義第二張圖案在圖表的位置
ax2 = fig.add_subplot(212)
# 透過直方圖來進行量能繪製
ax2.bar(QTime, QValue,width=0.0005)
#透過直線圖，也能夠達成相同效果，程式碼如下
# ax2.vlines(QTime,[0],QValue)

#定義x軸
hfmt = mdates.DateFormatter('%H:%M:%S')
ax1.xaxis.set_major_formatter(hfmt)
ax2.xaxis.set_major_formatter(hfmt)

# 顯示繪製圖表
plt.show()
