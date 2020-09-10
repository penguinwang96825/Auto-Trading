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

# 定義威廉指標的週期、超買區、超賣區
WILLRPeriod=14
OverBuy = -20
OverSell = -80

# 預設趨勢為1，假設只有多單進場
Trend=1

# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    Real = KBar1M.GetWILLR(WILLRPeriod)
    # 當威廉指標已經計算完成，才會去進行判斷
    if len(Real) >= WILLRPeriod+1:
        ThisReal = Real[-1]
        LastReal = Real[-2]

        # 進入超賣區 並且回檔
        if Trend==1 and ThisReal > OverSell and LastReal <= OverSell:
            Index=1
            OrderTime=time
            OrderPrice=price            
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            break
        # 進入超買區 並且回檔
        elif Trend==-1 and ThisReal < OverBuy and LastReal >= OverBuy:
            Index=-1
            OrderTime=time
            OrderPrice=price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            break

        


