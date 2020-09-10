# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]

# 一分鐘K棒的物件
KBar1M=indicator.KBar(date=Date)

# 定義量能平均週期
VolumePeriod=20

# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    QMA = KBar1M.GetQMA(VolumePeriod)
    # 當慢線已經計算完成，才會去進行判斷
    if len(QMA) > VolumePeriod+1:
        # 當前分鐘成交量
        ThisQ=KBar1M.GetVolume()[-1]
        # 之前平均的量平均
        LastAvgQ=QMA[-2]
        
        # 當目前成交量突破 前N分鐘的平均值 定義為爆量進場
        if ThisQ > LastAvgQ:
            Close=KBar1M.GetClose()[-1]
            Open=KBar1M.GetClose()[-1]
            # 如果爆量的當下 收盤價大於開盤價則做多
            if Close > Open :
                Index=1
                OrderTime=time
                OrderPrice=price            
                print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
                break
            # 如果爆量的當下 收盤價大於開盤價則做空
            elif Close < Open:
                Index=-1
                OrderTime=time
                OrderPrice=price            
                print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
                break

