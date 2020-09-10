# -*- coding: utf-8 -*-

# 載入必要套件
from indicator import GetHistoryData
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime,sys
strptime=datetime.datetime.strptime

# 取得資料
# Date='20190902'
Date=sys.argv[1]
Product=sys.argv[2]
ExercisePrice=sys.argv[3]   # 履約價

FilePath='C:/Data/'
Broker='Simulator'
Table='Match'
# 商品年分
Year=Product[4]
# 期貨近月月份代號
Month=Product[3]
# 選擇權月份契約對照表
CallMonthTable=['A','B','C','D','E','F','G','H','I','J','K','L']
PutMonthTable=['M','N','O','P','Q','R','S','T','U','V','W','X']
# 找出相對應的買賣權月份代號
CallMonth=Month
PutMonth=PutMonthTable[CallMonthTable.index(Month)]

# 取得期貨、選擇權商品名稱
TXFName=Product
CallName='TXO'+ExercisePrice+CallMonth+Year
PutName='TXO'+ExercisePrice+PutMonth+Year

# 取得資料
TXFData=GetHistoryData(FilePath,Broker,Date,TXFName,Table)
CallData=GetHistoryData(FilePath,Broker,Date,CallName,Table)
PutData=GetHistoryData(FilePath,Broker,Date,PutName,Table)

# 取特定時間的資料
TXFData = [ line for line in TXFData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]
CallData = [ line for line in CallData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]
PutData = [ line for line in PutData if strptime(line[0],"%Y/%m/%d %H:%M:%S.%f").strftime('%H%M') < '1345' ]

#取得轉換時間字串至時間格式
TXFTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in TXFData ]
CallTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in CallData ]
PutTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in PutData ]

#價格由字串轉數值
TXFPrice = [ int(line[2]) for line in TXFData ]
CallPrice = [ int(line[2]) for line in CallData ]
PutPrice = [ int(line[2]) for line in PutData ]

#定義圖表物件
ax1 = plt.subplot(311)
ax2 = plt.subplot(312)
ax3 = plt.subplot(313)

#繪製圖案 ( X軸物件, Y軸物件, 線風格 )
ax1.plot_date( TXFTime, TXFPrice, 'k-' , linewidth=1 )
ax2.plot_date( CallTime, CallPrice, 'r-' , linewidth=1 )
ax3.plot_date( PutTime, PutPrice, 'g-' , linewidth=1 )

#定義標頭
ax1.set_title(TXFName)
ax2.set_title(CallName)
ax3.set_title(PutName)

#定義x軸
ax1.get_xaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)
hfmt = mdates.DateFormatter('%H:%M')
ax3.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()



