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

# 定義趨勢判斷的時間
StartTime=datetime.datetime.strptime(Date+'09:30:00','%Y%m%d%H:%M:%S')

# 進場前判斷
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    # 如果時間到達指定的時間
    if time > StartTime:
        # 則取出當前最高以及最低
        High=max(KBar1M.GetHigh())
        Low=min(KBar1M.GetLow())
        Spread=High-Low
        break

# 進場判斷 
Index=0      
for i in function.getSIDMatch(Date,Sid):
    time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
    price=float(i[2])
    qty=int(i[3])
    check=KBar1M.Add(time,price,qty)
    
    if price > High:
        Index=1
        OrderTime=time
        OrderPrice=price 
        # 若要實單交易 可以將註解取消
        #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
        #OrderPrice=OrderInfo[0][4]
        #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        break
    elif price < Low:
        Index=-1
        OrderTime=time
        OrderPrice=price  
        # 若要實單交易 可以將註解取消
        #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
        #OrderPrice=OrderInfo[0][4]
        #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')    
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        break
                
# 移動停損比率
TrailingStopRatio=0.02
# 設定最後出場時間
EndTime = datetime.datetime.strptime(Date+'13:20:00.00','%Y%m%d%H:%M:%S.%f')

# 出場判斷
if Index==1:
    # 紀錄當前最高價
    TmpHigh = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpHigh * (1-TrailingStopRatio)
    # 多單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        
        # 如果價格屬於當前最高價
        if price > TmpHigh:
            # 重新計算移動停損點
            TmpHigh=price
            TrailingStop = TmpHigh * (1-TrailingStopRatio)
        # 價格低於移動停損價出場
        elif price < TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'S',bid,OrderNum,'3')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')    
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            break
        # 當時間到最後出場時間強制出場
        elif time>EndTime:
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
    # 紀錄當前最高價
    TmpLow = OrderPrice
    # 初始化移動停損
    TrailingStop = TmpLow * (1+TrailingStopRatio)
    # 空單出場判斷
    for i in function.getSIDMatch(Date,Sid):
        time=datetime.datetime.strptime(Date+i[0],'%Y%m%d%H:%M:%S.%f')
        price=float(i[2])
        qty=int(i[3])
        check=KBar1M.Add(time,price,qty)
        
        # 如果價格屬於當前最高價
        if price < TmpLow:
            # 重新計算移動停損點
            TmpLow=price
            TrailingStop = TmpLow * (1+TrailingStopRatio)
        # 當價格向上觸碰到移動停損價
        elif price > TrailingStop:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            break
        # 當時間到最後出場時間強制出場
        elif time>EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            # 若要實單交易 可以將註解取消
            #OrderInfo=Order(BrokerID,Sid,'B',bid,OrderNum,'0')
            #OrderPrice=OrderInfo[0][4]
            #OrderTime=datetime.datetime.strptime(OrderInfo[0][6],'%Y/%m/%d %H:%M:%S')            
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            break