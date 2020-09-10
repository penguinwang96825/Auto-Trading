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
    
    # 總量、買筆、賣筆由字串轉數值
    BigX = [ [datetime.datetime.strptime(I020[i][0] + ' ' +I020[i][1],"%Y%m%d %H%M%S%f"),int(I020[i][3]),int(I020[i][6])-int(I020[i-1][6]),int(I020[i][7])-int(I020[i-1][7]),int(I020[i][8])-int(I020[i-1][8])] for i in range(1,len(I020)) ]
        
    # 取得大單
    B_Time_Big = []
    S_Time_Big = []
    B_Big = []
    S_Big = []
    for line in BigX:
        time = line[0]
        price = line[1]
        qty = line[2]
        b = line[3]
        s = line[4]
        if qty > 60:
            if b == 1:
                B_Time_Big.append(time)
                B_Big.append(price)
            elif s == 1:
                S_Time_Big.append(time)
                S_Big.append(price)

    # 定義標頭    
    fig = plt.figure()
    fig.suptitle("Price BigOrder Line", fontsize=16)
    
    # 定義圖表物件
    ax1 = plt.subplot(111)
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax1.plot_date( Time, Price, 'k-' )
    ax1.plot_date( B_Time_Big, B_Big, 'r.' )
    ax1.plot_date( S_Time_Big, S_Big, 'g.' )
    
    # 定義x軸
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(hfmt)
    
    # 顯示繪製圖表
    plt.show()

    # 僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break