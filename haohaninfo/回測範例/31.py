# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#載入成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]
#取得轉換時間字串至時間格式
MTime = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I020 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
MTime1 = [ mdates.date2num(line) for line in MTime ]
#價格由字串轉數值
Price = [ int(line[4]) for line in I020 ]

#定義圖表物件
fig = plt.figure(1)
#定義第一張圖案在圖表的位置
ax1 = fig.add_subplot(211)
# 繪製價格折線圖
ax1.plot_date(MTime1, Price, 'b-')

#載入委託資訊
I030 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I030.csv')][1:]
#I030 = [ line for line in I030 if int(line[0]) > 8450000]
#取得轉換時間字串至時間格式
OTime = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I030 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
OTime1 = [ mdates.date2num(line) for line in OTime ]
#計算委託買方平均口數
BRatio = [ float(line[3])/int(line[2]) for line in I030 ]
#計算委託賣方平均口數
SRatio = [ float(line[5])/int(line[4]) for line in I030 ]

#定義第二張圖案在圖表的位置
ax2 = fig.add_subplot(212)
#繪製委託價格總量差圖
ax2.plot_date(OTime1, BRatio, 'r-')
ax2.plot_date(OTime1, SRatio, 'g-')

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M:%S')
ax1.xaxis.set_major_formatter(hfmt)
ax2.xaxis.set_major_formatter(hfmt)

plt.show()

