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
CData=GetHistoryData(FilePath,Broker,Date,Product,'Commission')

# 取特定時間的資料(委託檔揭示時間從8點30開始，所以需要從8點45開始繪圖)
MData = [ line for line in MData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]
CData = [ line for line in CData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' \
           and strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') > '0845'  ]

#取得轉換時間字串至時間格式
MTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in MData ]
CTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in CData ]

#價格由字串轉數值
Price = [ float(line[2]) for line in MData ]
BuyOrderAverage = [ float(line[3])/float(line[2]) for line in CData ]
SellOrderAverage = [ float(line[5])/float(line[4]) for line in CData ]

#定義圖表物件
ax1 = plt.subplot(211)
ax2 = plt.subplot(212)

#繪製圖案 ( X軸物件, Y軸物件, 線風格 )
ax1.plot_date( MTime, Price, 'k-' , linewidth=1 )
ax2.plot_date( CTime, BuyOrderAverage, 'r-' , linewidth=1 )
ax2.plot_date( CTime, SellOrderAverage, 'g-' , linewidth=1 )

#定義標頭
ax1.set_title('Price')
ax2.set_title('Order Average')

#定義x軸
ax1.get_xaxis().set_visible(False)
hfmt = mdates.DateFormatter('%H:%M')
ax2.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()



