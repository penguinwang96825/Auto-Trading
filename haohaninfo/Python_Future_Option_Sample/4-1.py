# -*- coding: utf-8 -*-

# 載入必要套件
from indicator import GetHistoryData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime,sys
strptime=datetime.datetime.strptime

# 取得資料
# Date='20190902'
# Product='TXFI9'
Date=sys.argv[1]
Product=sys.argv[2]
FilePath='C:/Data/'
Broker='Simulator'
Table='Match'
Data=GetHistoryData(FilePath,Broker,Date,Product,Table)

# 取特定時間的資料
Data = [ line for line in Data if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]

#取得轉換時間字串至時間格式
Time = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in Data ]

#價格由字串轉數值
Price = [ int(line[2]) for line in Data ]

#定義圖表物件
ax = plt.subplot(111)

#繪製圖案 ( X軸物件, Y軸物件, 線風格 )
ax.plot_date( Time, Price, 'k-' , linewidth=1 )

#定義標頭
ax.set_title('Price Line')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()



