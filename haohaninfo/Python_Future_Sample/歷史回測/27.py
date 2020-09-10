# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import backtest_function

#取得歷史資料
Data=backtest_function.GetI020()

#透過迴圈取得每天的資料
for date in backtest_function.GetDate(Data):
    
    #取得當日的時間
    I020 = [ line for line in Data if line[0] == date ]
    
    #取得轉換時間字串至時間格式
    Time = [ datetime.datetime.strptime(date + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I020 ]

    #價格由字串轉數值
    Price = [ int(line[3]) for line in I020 ]
    
    #定義圖表物件
    ax = plt.subplot(111)

    #繪製圖案 ( X軸物件, Y軸物件, 線風格 )
    ax.plot_date( Time, Price, 'k-' )

    #定義標頭
    plt.title('Price Line')

    #定義x軸
    hfmt = mdates.DateFormatter('%H:%M:%S')
    ax.xaxis.set_major_formatter(hfmt)

    #顯示繪製圖表
    plt.show()

    #僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break