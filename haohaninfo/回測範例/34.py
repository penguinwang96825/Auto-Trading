# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#載入成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]
#載入上下五檔價量資訊
I080 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I080.csv')][1:]
I080 = [ line for line in I080 if int(line[0])>8450000 ]

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

#取得轉換時間字串至時間格式
UpDnTime=[ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I080 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
UpDnTime1 = [ mdates.date2num(line) for line in UpDnTime ]
#取得下五檔委託總量
DnQty=[ (int(line[3])+int(line[5])+int(line[7])+int(line[9])+int(line[11]))*-1 for line in I080 ]
#取得上五檔委託總量
UpQty=[ int(line[13])+int(line[15])+int(line[17])+int(line[19])+int(line[21]) for line in I080 ]


#定義第二張圖案在圖表的位置
ax2 = fig.add_subplot(212)
#繪製上下五檔量能圖
ax2.vlines(UpDnTime1,[0],UpQty,'r')
ax2.vlines(UpDnTime1,DnQty,[0],'g')

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M:%S')
ax1.xaxis.set_major_formatter(hfmt)
ax2.xaxis.set_major_formatter(hfmt)

plt.show()

