# -*- coding: UTF-8 -*-
# 載入相關套件
import datetime,function,indicator
import sys 

# 取得當天日期
Date=datetime.datetime.now().strftime("%Y%m%d")
# 測試股票下單
Sid=sys.argv[1]
# 定義要使用的券商、張數
#BrokerID='Capital'
#OrderNum='1'

# 取得前日K棒
LastKBar=function.getDayKBarbyNum(Sid,1)
LastClose=LastKBar[-1][4]

# 進場判斷
Index=0
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    if price < LastClose:
        print('開盤向下跳空')
        Index=1
        OrderTime=time
        OrderPrice=price
        # 若要實單交易 可以將註解取消
        #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
        #OrderPrice=OrderInfo[0][4]
        #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        break
    elif price > LastClose:
        print('開盤向上跳空')
        Index=-1
        OrderTime=time
        OrderPrice=price   
        # 若要實單交易 可以將註解取消
        #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
        #OrderPrice=OrderInfo[0][4]
        #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        break
    else:
        print('無跳空缺口')
        break
        

# 停損停利比率
StopLossRatio=0.02
TakeProfitRatio=0.03
# 設定最後出場時間
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')

# 出場判斷
if Index==1:
    # 多單出場判斷
    StopLoss=OrderPrice*(1-StopLossRatio)
    TakeProfit=OrderPrice*(1+TakeProfitRatio)
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        # 當價格高於停利價
        if price > TakeProfit:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Buy TakeProfit Price:",CoverPrice,"Success!")
            break
        # 當價格低於停損價
        elif price < StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Buy StopLoss Price:",CoverPrice,"Success!")
            break
        # 當時間大於結束時間
        elif time > EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Buy Time Over Price:",CoverPrice,"Success!")
            break
            
            
elif Index==-1:
    # 空單出場判斷
    StopLoss=OrderPrice*(1+StopLossRatio)
    TakeProfit=OrderPrice*(1-TakeProfitRatio)
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        # 當價格低於停利價
        if price < TakeProfit:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
            print(CoverTime,"Cover Sell TakeProfit Price:",CoverPrice,"Success!")
            break
        # 當價格高於停損價
        elif price > StopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Sell StopLoss Price:",CoverPrice,"Success!")
            break
        # 當時間大於結束時間
        elif time > EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Sell Time Over Price:",CoverPrice,"Success!")
            break