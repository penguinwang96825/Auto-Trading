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
        K,D = KBar1M.GetKD()
        # 當K值已經計算完成，才會去進行判斷
        if len(K) > 9:
            ThisK = K[-1]
            LastK = K[-2]
            ThisD = D[-1]
            LastD = D[-2]
            # 死亡交叉
            if LastK >= LastD and ThisK < ThisD:
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
        K,D = KBar1M.GetKD()
        # 當K值已經計算完成，才會去進行判斷
        if len(K) > 9:
            ThisK = K[-1]
            LastK = K[-2]
            ThisD = D[-1]
            LastD = D[-2]
            # 黃金交叉
            if LastK <= LastD and ThisK > ThisD:
                Index=0
                CoverTime=time
                CoverPrice=price            
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break


        
