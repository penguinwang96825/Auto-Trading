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

# 定義中線的週期
BBANDSPeriod=10

# 設定最後出場時間
time = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')

# 當時間小於
while time<EndTime:
    # 進場判斷，該策略沒有預設趨勢
    Index=0
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
            ThisLower = Lower[-1]
            LastPrice = Price[-2]
            LastUpper = Upper[-2]
            LastLower = Lower[-2]
            
            # 價格與通道下緣黃金交叉
            if LastPrice <= LastLower and ThisPrice > ThisLower:
                Index=1
                OrderTime=time
                OrderPrice=price
                # 若要實單交易 可以將註解取消
                #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
                #OrderPrice=OrderInfo[0][4]
                #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')   
                print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
                break
            # 價格與通道上緣死亡交叉
            elif LastPrice >= LastUpper and ThisPrice < ThisUpper:
                Index=-1
                OrderTime=time
                OrderPrice=price
                # 若要實單交易 可以將註解取消
                #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
                #OrderPrice=OrderInfo[0][4]
                #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')    
                print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
                break
            # 時間到後則不進場直接結束策略
            elif time > EndTime:
                print("Time Over")
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
                    # 若要實單交易 可以將註解取消
                    #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
                    #OrderPrice=OrderInfo[0][4]
                    #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
                    print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                    break
                elif time > EndTime:
                    Index=0
                    CoverTime=time
                    CoverPrice=price
                    # 若要實單交易 可以將註解取消
                    #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
                    #OrderPrice=OrderInfo[0][4]
                    #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
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
                    # 若要實單交易 可以將註解取消
                    #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
                    #OrderPrice=OrderInfo[0][4]
                    #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')                       
                    print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                    break
                elif time > EndTime:
                    Index=0
                    CoverTime=time
                    CoverPrice=price   
                    # 若要實單交易 可以將註解取消
                    #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
                    #OrderPrice=OrderInfo[0][4]
                    #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')                       
                    print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                    break