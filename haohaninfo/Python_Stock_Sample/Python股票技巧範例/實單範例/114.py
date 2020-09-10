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

# 定義中線的週期
BBANDSPeriod=10

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
        Upper,Middle,Lower = KBar1M.GetBBANDS(BBANDSPeriod)
        # 當中線已經計算完成，才會去進行判斷
        if len(Middle) >= BBANDSPeriod:
            Price = KBar1M.GetClose()
            ThisPrice = Price[-1]
            ThisUpper = Upper[-1]
            LastPrice = Price[-2]
            LastUpper = Upper[-2]                  
            # 價格與通道上緣黃金交叉
            if LastPrice <= LastUpper and ThisPrice > ThisUpper:
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
        Upper,Middle,Lower = KBar1M.GetBBANDS(BBANDSPeriod)
        # 當中線已經計算完成，才會去進行判斷
        if len(Middle) >= BBANDSPeriod:
            Price = KBar1M.GetClose()
            ThisPrice = Price[-1]
            ThisLower = Lower[-1]
            LastPrice = Price[-2]
            LastLower = Lower[-2]                    
            # 價格與通道下緣死亡交叉
            if LastPrice >=LastLower and ThisPrice < ThisLower:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break
