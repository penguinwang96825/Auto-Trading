# -*- coding: UTF-8 -*-

#載入相關套件及函數
import sys,datetime,numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from talib.abstract import *
from backtest_function import GetHistoryTAKBar

#將日期以及股票代碼變成參數帶入
date=sys.argv[1]
stockid=sys.argv[2]

# 取得 TALib 格式的 K線
TAKBar=GetHistoryTAKBar(date,stockid)
# 計算MA技術指標
TAKBar['MA'] = MA(TAKBar,timeperiod=10,matype=1)

#將datetime時間格式轉換為繪圖專用的時間格式，透過mdates.date2num函數
Time1 = mdates.date2num(TAKBar['time'])

#定義圖表物件        
ax = plt.subplot(111)	#該張圖片僅一個圖案

#繪製圖案
ax.plot_date(Time1, TAKBar['close'], 'k-')
ax.plot_date(Time1, TAKBar['MA'], 'r-')

#定義title
plt.title('Stock '+stockid+' Price MA Line')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()
