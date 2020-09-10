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

# 定義RSI指標、快線、慢線的週期
RSIPeriod=14
FastPeriod=5
SlowPeriod=15

# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    RSI = KBar1M.GetRSI(RSIPeriod)
    SlowMA = KBar1M.GetSMA(SlowPeriod)
    # 當RSI指標及慢線皆已計算完成，才會去進行判斷
    if len(RSI) >= RSIPeriod and len(SlowMA) >= SlowPeriod+1:
        RSI = RSI[-1]
        FastMA = KBar1M.GetSMA(FastPeriod)
        ThisFastMA = FastMA[-1]
        ThisSlowMA = SlowMA[-1]
        LastFastMA = FastMA[-2]
        LastSlowMA = SlowMA[-2]

        # RSI指標趨勢偏多且均線黃金交叉
        if RSI > 50 and LastFastMA <= LastSlowMA and ThisFastMA > ThisSlowMA:
            Index=1
            OrderTime=time
            OrderPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            break
        # RSI指標趨勢偏空且均線死亡交叉
        elif RSI < 50 and LastFastMA >= LastSlowMA and ThisFastMA < ThisSlowMA:
            Index=-1
            OrderTime=time
            OrderPrice=price   
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')                
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            break

# 設定最後出場時間
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')
            
# 出場判斷
if Index==1:
    # 多單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        SlowMA = KBar1M.GetSMA(SlowPeriod)
        # 當慢線已經計算完成，才會去進行判斷
        if len(SlowMA) > SlowPeriod+1:
            FastMA = KBar1M.GetSMA(FastPeriod)
            ThisFastMA = FastMA[-1]
            ThisSlowMA = SlowMA[-1]
            LastFastMA = FastMA[-2]
            LastSlowMA = SlowMA[-2]
            RSI = KBar1M.GetRSI(RSIPeriod)
            RSI = RSI[-1]
            # 死亡交叉
            if LastFastMA >= LastSlowMA and ThisFastMA < ThisSlowMA:
                Index=0
                CoverTime=time
                CoverPrice=price
                # 若要實單交易 可以將註解取消
                #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
                #OrderPrice=OrderInfo[0][4]
                #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')    
                print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
                break
            elif RSI < 50:
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
        SlowMA = KBar1M.GetSMA(SlowPeriod)
        # 當慢線已經計算完成，才會去進行判斷
        if len(SlowMA) > SlowPeriod+1:
            FastMA = KBar1M.GetSMA(FastPeriod)
            ThisFastMA = FastMA[-1]
            ThisSlowMA = SlowMA[-1]
            LastFastMA = FastMA[-2]
            LastSlowMA = SlowMA[-2]
            RSI = KBar1M.GetRSI(RSIPeriod)
            RSI = RSI[-1]
            # 黃金交叉
            if LastFastMA <= LastSlowMA and ThisFastMA > ThisSlowMA:
                Index=0
                CoverTime=time
                CoverPrice=price     
                # 若要實單交易 可以將註解取消
                #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
                #OrderPrice=OrderInfo[0][4]
                #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')                
                print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
                break
            elif RSI > 50:
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

