# -*- coding: utf-8 -*-

# 載入必要套件
from indicator import GetHistoryData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime,sys
strptime=datetime.datetime.strptime

# 取得資料
Date=sys.argv[1]
Product=sys.argv[2]
FilePath='C:/Data/'
Broker='Simulator'

# 取得資料
MData=GetHistoryData(FilePath,Broker,Date,Product,'Match')

# 取特定時間的資料
MData = [ line for line in MData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]

# 計算大額成交量資料
BigBuyOrder = [ MData[i] for i in range(1,len(MData)) if \
            int(MData[i][5])-int(MData[i-1][5]) < int(MData[i][6])-int(MData[i-1][6]) and int(MData[i][3]) > 50 ]
SellBuyOrder = [ MData[i] for i in range(1,len(MData)) if \
            int(MData[i][5])-int(MData[i-1][5]) > int(MData[i][6])-int(MData[i-1][6]) and int(MData[i][3]) > 50 ]

#取得轉換時間字串至時間格式
MTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in MData ]
BigBuyTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in BigBuyOrder ]
SellBuyTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in SellBuyOrder ]

#價格由字串轉數值
Price = [ float(line[2]) for line in MData ]
BigBuyPrice = [ float(line[2]) for line in BigBuyOrder ]
SellBuyPrice = [ float(line[2]) for line in SellBuyOrder ]

#定義圖表物件
ax1 = plt.subplot(111)

#繪製圖案 ( X軸物件, Y軸物件, 線風格 )
ax1.plot_date( MTime, Price, 'k-' , linewidth=1 )
ax1.plot_date( BigBuyTime, BigBuyPrice, 'r.' ,markersize=9 )
ax1.plot_date( SellBuyTime, SellBuyPrice, 'g.' ,markersize=9)

#定義標頭
ax1.set_title('Price')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M')
ax1.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()
