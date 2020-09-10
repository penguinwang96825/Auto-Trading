# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from mpl_finance import candlestick_ohlc
import backtest_function

# 取得歷史資料
Data=backtest_function.GetI020()

# 透過迴圈取得每天的資料
for date in backtest_function.GetDate(Data):
    
    # 取得當日的時間
    I020 = [ line for line in Data if line[0] == date ]

    # 計算K線圖
    KBar=backtest_function.ConvertKBar(date,I020)
    KBar=[ [mdates.date2num(line[0]),line[1],line[2],line[3],line[4],line[5]] for line in KBar ]
    
    # 單獨取出K棒時間
    KBarTime=[ line[0] for line in KBar ]
    
    # 定義標頭    
    fig = plt.figure()
    fig.suptitle("OHLC", fontsize=16)
    
    # 定義圖表物件
    ax1 = plt.subplot(111)
    
    # 繪製K線圖
    candlestick_ohlc(ax1, KBar, width=0.0003, colorup='r', colordown='g')  

    # X軸的間隔設為半小時
    plt.xticks(np.arange(min(KBarTime), max(KBarTime), 1/1440*30))
    
    # 定義x軸格式
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(hfmt)
    
    # 顯示繪製圖表
    plt.show()

    # 僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break