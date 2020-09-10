# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import backtest_function

# 取得歷史資料
Data=backtest_function.GetI020()
Data03=backtest_function.GetI030()

# 透過迴圈取得每天的資料
for date in backtest_function.GetDate(Data):
    
    # 取得當日的時間
    I020 = [ line for line in Data if line[0] == date ]
    I030 = [ line for line in Data03 if line[0] == date if int(line[1]) > 84500000000 ]

    # 取得轉換時間字串至時間格式
    Time = [ datetime.datetime.strptime(line[0] + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I020 ]

    # 價格由字串轉數值
    Price = [ int(line[3]) for line in I020 ]
    
    # 委託資訊揭示時間由字串轉數值
    Time030 = [ datetime.datetime.strptime(line[0] + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I030 ]
    
    # 委託買賣平均差由字串轉數值
    BRatio = [ float(line[4])/float(line[3]) for line in I030 ]
    SRatio = [ float(line[6])/float(line[5]) for line in I030 ]
    
    # 定義標頭    
    fig = plt.figure()
    fig.suptitle("Price & Order Line", fontsize=16)
    
    # 定義圖表物件
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax1.plot_date( Time, Price, 'k-' )
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax2.plot_date( Time030, BRatio, 'r-' )
    ax2.plot_date( Time030, SRatio, 'g-' )
    
    # 定義x軸
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(hfmt)
    ax2.xaxis.set_major_formatter(hfmt)
    
    # 顯示繪製圖表
    plt.show()

    # 僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break