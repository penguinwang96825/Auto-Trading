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

# 計算選擇權合成期貨價格
EP=int(ExercisePrice)
CallP=float(CallData[0][2])
PutP=float(PutData[0][2])
TmpData=CallData[1:]+PutData[1:]
TmpData.sort()
SyntheticData=[] # 合成期貨陣列
for row in TmpData:
    if row[1]==CallName:
        CallP=float(row[2])
        SyntheticP=CallP-PutP+EP
        SyntheticData.append([row[0],'Synthetic',SyntheticP])
    elif row[1]==PutName:
        PutP=float(row[2])
        SyntheticP=CallP-PutP+EP
        SyntheticData.append([row[0],'Synthetic',SyntheticP])

#取得轉換時間字串至時間格式
TXFTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in TXFData ]
SyntheticTime = [ strptime(line[0],"%Y/%m/%d %H:%M:%S.%f") for line in SyntheticData ]

#價格由字串轉數值
TXFPrice = [ int(line[2]) for line in TXFData ]
SyntheticPrice = [ float(line[2]) for line in SyntheticData ]

#定義圖表物件
ax = plt.subplot(111)

#繪製圖案 ( X軸物件, Y軸物件, 線風格 )
ax.plot_date( TXFTime, TXFPrice, 'k-' , linewidth=1 )
ax.plot_date( SyntheticTime, SyntheticPrice, 'r-' , linewidth=1 )

#定義標頭
ax.set_title('')

#定義x軸
hfmt = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(hfmt)

#顯示繪製圖表
plt.show()



