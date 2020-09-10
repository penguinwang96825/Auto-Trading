# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#取得成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

BPoint=[]
SPoint=[]
for i in range(1,len(I020)):
 diffBOrder=int(I020[i][7])-int(I020[i-1][7])
 diffSOrder=int(I020[i][8])-int(I020[i-1][8])
 if diffBOrder==1 and diffSOrder>=30:
  BPoint+=[I020[i]]
 if diffSOrder==1 and diffBOrder>=30:
  SPoint+=[I020[i]]



#取得轉換時間字串至時間格式
Time = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I020 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
Time1 = [ mdates.date2num(line) for line in Time ]
#價格由字串轉數值
Price = [ int(line[4]) for line in I020 ]

#取得轉換時間字串至時間格式
BPTime = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in BPoint ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
BPTime1 = [ mdates.date2num(line) for line in BPTime ]
#價格由字串轉數值
BPPrice = [ int(line[4]) for line in BPoint ]

#取得轉換時間字串至時間格式
SPTime = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in SPoint ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
SPTime1 = [ mdates.date2num(line) for line in SPTime ]
#價格由字串轉數值
SPPrice = [ int(line[4]) for line in SPoint ]

#定義圖表物件
ax = plt.figure(1) 		#第一張圖片              
ax = plt.subplot(111)	#該張圖片僅一個圖案
#以上兩行，可簡寫如下一行
#fig,ax = plt.subplots()

#定義title
plt.title('Price Line')
plt.xlabel('Time')
plt.ylabel('Price')

#繪製圖案
#plot_date(X軸物件, Y軸物件, 線風格)
ax.plot_date(Time1, Price, 'k-')
ax.plot_date(BPTime1, BPPrice, 'r.',markersize='8')
ax.plot_date(SPTime1, SPPrice, 'g.',markersize='8')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()
