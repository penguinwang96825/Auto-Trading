# -*- coding: UTF-8 -*-

#載入相關套件及函數
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
from matplotlib.finance import candlestick_ohlc

#時間轉數值
def TimetoNumber(time):
 time=time.zfill(8)
 sec=int(time[:2])*360000+int(time[2:4])*6000+int(time[4:6])*100+int(time[6:8])
 return sec

#數值轉時間
def NumbertoTime(sec):
 TOS=str(sec%100).zfill(2)
 TTime=sec/100
 TS=str(TTime%60).zfill(2)
 TTime=TTime/60
 TM=str(TTime%60).zfill(2)
 TTime=TTime/60
 TH=str(TTime%60).zfill(2)
 return TH+TM+TS

#取得成交資訊
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#設定K線初始變數
STime = TimetoNumber('08450000')
#設定K線週期
Cycle = 6000
OHLC=[]
lastAmount=0

#計算每分鐘OHLC
for i in I020:
 time = TimetoNumber(i[0])
 price = int(i[4])
 amount = int(i[6])
 if len(OHLC)==0:
  OHLC+=[[mdates.date2num(datetime.datetime.strptime(NumbertoTime(STime+Cycle),"%H%M%S")),price,price,price,price,0]]
 if time<STime+Cycle:
  if price>OHLC[-1][2]:
   OHLC[-1][2]=price
  if price<OHLC[-1][3]:
   OHLC[-1][3]=price
  OHLC[-1][4]=price
 else:
  OHLC[-1][5]=amount-lastAmount
  lastAmount=amount
  STime+=Cycle
  OHLC+=[[mdates.date2num(datetime.datetime.strptime(NumbertoTime(STime+Cycle),"%H%M%S")),price,price,price,price,0]]


#定義圖表物件
fig = plt.figure(1)
#定義第一張圖案在圖表的位置
ax1 = fig.add_subplot(111)

#繪製K線圖
candlestick_ohlc(ax1, OHLC, width=0.0005, colorup='r', colordown='g')

#設定K線圖佔圖表版面比例
pad = 0.25
yl = ax1.get_ylim()
ax1.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

#定義時間陣列、量陣列
Time= [ line[0] for line in OHLC ]
Qty= [ line[5] for line in OHLC ]

#設定兩張圖表重疊
ax2 = ax1.twinx()
#繪製量能圖
ax2.bar(Time, Qty, color='gray', width = 0.0005, alpha = 0.75)
#將量能圖定位在K線圖下方
ax2.set_position(matplotlib.transforms.Bbox([[0.125,0.11],[0.9,0.275]]))

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(hfmt)

plt.show()