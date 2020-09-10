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
    Time = [ datetime.datetime.strptime(date + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I020 ]

    # 價格由字串轉數值
    Price = [ int(line[3]) for line in I020 ]
    
    # 量能由字串轉數值
    Amount = [ int(line[6]) for line in I020 ]
    
    # 設定算起始時間 、 計算週期 
    StartTime =datetime.datetime.strptime(date + ' 084500',"%Y%m%d %H%M%S")
    Cycle = datetime.timedelta( 0 , 60 ) # 60 代表週期為60秒 若要改成5分鐘 則修改為300即可計算5分鐘的量能
    Volume_Time_Array = []
    Volume_Array = []
    lastAmount=0
    # 開始計算量能
    for i in range(len(Price)):
        time = Time[i]
        price = Price[i]
        amount = Amount[i]
        if time >= StartTime + Cycle :
            StartTime += Cycle
            Volume_Time_Array.append(StartTime)
            Volume_Array.append(amount-lastAmount)
            lastAmount = amount

    # 定義標頭    
    fig = plt.figure()
    fig.suptitle("Price & Volume Line", fontsize=16)
    
    # 定義圖表物件
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212)
    
    # 繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax1.plot_date( Time, Price, 'k-' )
    
    # 繪製圖案 ( X軸物件, Y軸物件 )
    # ax2.bar( Volume_Time_Array, Volume_Array,width=0.0005)
    # 透過直線圖，也能夠達成相同效果，程式碼如下
    ax2.vlines( Volume_Time_Array,[0], Volume_Array)

    # 定義x軸
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax1.xaxis.set_major_formatter(hfmt)
    ax2.xaxis.set_major_formatter(hfmt)
    
    # 顯示繪製圖表
    plt.show()

    # 僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break