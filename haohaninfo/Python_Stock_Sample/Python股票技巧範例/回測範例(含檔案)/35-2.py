# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import datetime
from backtest_function import GetHistoryKBar

#將日期以及股票代碼變成參數帶入
date=sys.argv[1]
stockid=sys.argv[2]

#取得成交資訊
KBar = GetHistoryKBar(date,stockid)

#將第一個欄位調整成繪圖格式
KBar = [ [mdates.date2num(line[0]),line[1],line[2],line[3],line[4],line[5]] for line in KBar ]

#定義圖表物件
fig = plt.figure(1)
#定義第一張圖案在圖表的位置
ax1 = fig.add_subplot(111)

#繪製K線圖
candlestick_ohlc(ax1, KBar, width=0.0005, colorup='r', colordown='g')

#設定K線圖佔圖表版面比例
pad = 0.25
yl = ax1.get_ylim()
ax1.set_ylim(yl[0]-(yl[1]-yl[0])*pad,yl[1])

#定義時間陣列、量陣列
Time= [ line[0] for line in KBar ]
Qty= [ line[5] for line in KBar ]

#設定兩張圖表重疊
ax2 = ax1.twinx()
#繪製量能圖
ax2.bar(Time, Qty, color='gray', width = 0.0005, alpha = 0.75)
#將量能圖定位在K線圖下方
ax2.set_ylim([0,max(Qty)*4])

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(hfmt)

plt.show()
