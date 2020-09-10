# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#時間轉數值
def TimetoNumber(time):
 time=time.zfill(8)
 sec=int(time[:2])*360000+int(time[2:4])*6000+int(time[4:6])*100+int(time[6:8])
 return sec

#載入成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#定義量能變數
STime = TimetoNumber('08450000')
Cycle = 6000						#週期為60秒
lastAmount = 0 
Qty=[]

#計算每分鐘量能
for i in I020:
 time=i[0]
 amount=int(i[6])
 if TimetoNumber(time)<STime+Cycle:
  continue
 else:
  Qty.extend([[time,amount-lastAmount]])  
  STime+=Cycle
  lastAmount = amount

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
QTime=[ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in Qty ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
QTime1 = [ mdates.date2num(line) for line in QTime ]
#取出量能的list
QValue=[ line[1] for line in Qty ]

#定義第二張圖案在圖表的位置
ax2 = fig.add_subplot(212)
#透過直方圖來進行量能繪製
#ax2.bar(QTime, QValue,width=0.0005)
#透過直線圖，也能夠達成相同效果，程式碼如下
ax2.vlines(QTime,[0],QValue)

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M:%S')
ax1.xaxis.set_major_formatter(hfmt)
ax2.xaxis.set_major_formatter(hfmt)

plt.show()

