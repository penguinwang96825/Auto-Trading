# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

#時間轉數值函數
def TimetoNumber(time):
 time=time.zfill(8)
 sec=int(time[:2])*360000+int(time[2:4])*6000+int(time[4:6])*100+int(time[6:8])
 return sec

#載入成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#定義MA相關變數
MAarray = []
MA = []
MAValue = 0
STime = TimetoNumber('08450000')
Cycle = 6000
MAlen = 10

#開始進行MA計算
for i in I020:
 time=i[0]
 price=int(i[4])
 if len(MAarray)==0:
  MAarray+=[price]
 else:
  if TimetoNumber(time)<STime+Cycle:
   MAarray[-1]=price
  else:
   if len(MAarray)==MAlen:
    MAarray=MAarray[1:]+[price]
   else:
    MAarray+=[price]   
   STime = STime+Cycle
 MAValue=float(sum(MAarray))/len(MAarray)
 MA.extend([MAValue])

#取得轉換時間字串至時間格式
Time = [ datetime.datetime.strptime(line[0],"%H%M%S%f") for line in I020 ]
#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
Time1 = [ mdates.date2num(line) for line in Time ]
#價格由字串轉數值
Price = [ int(line[4]) for line in I020 ]

#定義圖表物件
ax = plt.figure(1) 		#第一張圖片              
ax = plt.subplot(111)	#該張圖片僅一個圖案
#以上兩行，可簡寫如下一行
#fig,ax = plt.subplots()

#定義title
plt.title('Price&MA Line')
plt.xlabel('Time')
plt.ylabel('Price')

# 繪製價格折線圖
ax.plot_date(Time1, Price, 'k-')
# 繪製MA折線圖
ax.plot_date(Time1, MA, 'r-')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(hfmt)

# 顯示繪製圖表
plt.show()

