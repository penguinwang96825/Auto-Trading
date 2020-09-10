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

#定義x軸時間格式
hfmt = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(hfmt)

plt.show()
