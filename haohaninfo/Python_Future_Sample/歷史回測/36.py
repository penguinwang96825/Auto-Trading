# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import backtest_function

# 取得歷史資料
Data=backtest_function.GetI020()

# 透過迴圈取得每天的資料
for date in backtest_function.GetDate(Data):
    
    # 取得當日的時間
    I020 = [ line for line in Data if line[0] == date ]

    # 取得轉換時間字串至時間格式
    Time = [ datetime.datetime.strptime(line[0] + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I020 ]

    # 價格由字串轉數值
    Price = [ int(line[3]) for line in I020 ]
    
    # 數量由字串轉數值
    Qty = [ int(line[4]) for line in I020 ]
    
    # 取得內外盤差額
    BSPower = 0
    BSPower_Time_Array = []
    BSPower_Array = []
    for i in range(1,len(Price)):
        time = Time[i]
        lastprice = Price[i-1]
        price = Price[i]
        qty = Qty[i]
        if price > lastprice:
            BSPower += qty
            BSPower_Time_Array.append(time)
            BSPower_Array.append(BSPower)
        elif price < lastprice:
            BSPower -= qty
            BSPower_Time_Array.append(time)
            BSPower_Array.append(BSPower)
    
   
    # 定義標頭    
    fig = plt.figure()
    fig.suptitle("Price & Order Line", fontsize=16)
    
    # 定義圖表物件
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax1.plot_date( Time, Price, 'k-' )
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax2.plot_date( BSPower_Time_Array, BSPower_Array, 'r-' )
    
    # 定義x軸
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(hfmt)
    ax2.xaxis.set_major_formatter(hfmt)
    
    # 顯示繪製圖表
    plt.show()

    # 僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break