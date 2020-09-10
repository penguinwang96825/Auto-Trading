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
ax1 = fig.add_subplot(111)
# 繪製價格折線圖
ax1.plot_date(MTime1, Price, 'b-')

#取得轉換時間字串至時間格式
UpDnTime=[ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I080 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
UpDnTime1 = [ mdates.date2num(line) for line in UpDnTime ]
#取得下五檔加權平均價
DnAvgP=[ ( int(line[2])*int(line[3])+int(line[4])*int(line[5])+int(line[6])*int(line[7])+int(line[8])*int(line[9])+int(line[10])*int(line[11]) ) / (int(line[3])+int(line[5])+int(line[7])+int(line[9])+int(line[11])) for line in I080 ]
#取得上五檔加權平均價
UpAvgP=[ (int(line[12])*int(line[13])+int(line[14])*int(line[15])+int(line[16])*int(line[17])+int(line[18])*int(line[19])+int(line[20])*int(line[21]) ) /(int(line[13])+int(line[15])+int(line[17])+int(line[19])+int(line[21])) for line in I080 ]

#進行上下平均價格線圖繪製
ax1.plot_date(UpDnTime1, DnAvgP, 'g-')
ax1.plot_date(UpDnTime1, UpAvgP, 'r-')

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M:%S')
ax1.xaxis.set_major_formatter(hfmt)

plt.show()

