# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 定義股票代碼
Sid=sys.argv[1]

# 一分鐘K棒的物件
KBar1M=indicator.KBar(date=Date)

# 定義量能平均週期
VolumePeriod=20

# 假設只有多單進場，本進場條件毫無意義，僅供測試
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    Index=1
    OrderTime=time
    OrderPrice=price
    print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
    break

    
# 出場判斷
if Index==1:
    # 多單出場判斷
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
            
            # 當目前成交量突破 前N分鐘的平均值 定義為爆量出場
            if ThisQ > LastAvgQ:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                break
elif Index==-1:
    # 空單出場判斷
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
            
            # 當目前成交量突破 前N分鐘的平均值 定義為爆量出場
            if ThisQ > LastAvgQ:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break