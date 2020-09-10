# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 定義要操作的股票
Sid=sys.argv[1]

# 設定固定時間進場
StartTime = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')

# 設定趨勢
Trend=1

# 進場策略
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    # 現在時間 大於 進場時間
    if time > StartTime:
        if Trend == 1: 
            Index=1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            break
        elif Trend == -1:
            Index=-1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            break
