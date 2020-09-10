# 載入必要函數
import indicator,sys,time,datetime,haohaninfo,order

# 取得必要參數 券商代號 商品名稱 停損點數 停利點數
Broker = sys.argv[1]
Prod = sys.argv[2]
Qty = int(sys.argv[3])
StopLoss = float(sys.argv[4])

# 部位管理物件
RC=order.Record()

# 進場     
Today = time.strftime('%Y%m%d')
CoverTime = datetime.datetime.strptime(Today + ' 14:25:00','%Y%m%d %H:%M:%S')

# K棒物件     
Today = time.strftime('%Y%m%d')
KBar = indicator.KBar(Today,1) 

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間、價格
    CTime = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    CPrice=float(row[2])
    CQty=int(row[3])
    print(CTime,'價位',CPrice)
    # 將成交資訊填入K線物件
    KBar.AddPrice(CTime,CPrice,CQty)
    # 判斷進場
    if RC.GetOpenInterest() == 0:
        # 如果K線的長度到達30 則開始判斷進場 
        if len(KBar.GetOpen()) > 31:
            # 定義高低點
            Ceil=max(KBar.GetHigh()[-31:-2])
            Floor=min(KBar.GetLow()[-31:-2])
            Spread=(Ceil-Floor)*0.2
            # 突破高低點則進場
            if CPrice >= Ceil + Spread:
                # 透過上兩檔價委託多單(範圍市價單 委託三次 若未成交則當日不交易)
                OrderInfo=order.RangeMKTDeal(Broker,Prod,'B',Qty,'0','A',2,10)
                # 如果沒有成交則關閉程序
                if OrderInfo == False:
                    GO.EndSubscribe()
                else:
                    # 成交則寫入紀錄至部位管理物件 
                    OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                    OrderInfoPrice=float(OrderInfo[4])            
                    RC.Order('B',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                    # 紀錄固定停損停利價位
                    StopLossPoint= OrderInfoPrice -StopLoss
                    print(Prod,'多單買進時間',OrderInfoTime,'買進價格',OrderInfoPrice,'移動停損價位',StopLossPoint)
                    continue
            elif CPrice <= Floor - Spread:
                # 透過上兩檔價委託多單(範圍市價單 委託三次 若未成交則當日不交易)
                OrderInfo=order.RangeMKTDeal(Broker,Prod,'S',Qty,'0','A',2,10)
                # 如果沒有成交則關閉程序
                if OrderInfo == False:
                    GO.EndSubscribe()
                else:
                    # 成交則寫入紀錄至部位管理物件 
                    OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                    OrderInfoPrice=float(OrderInfo[4])            
                    RC.Order('S',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                    # 紀錄固定停損停利價位
                    StopLossPoint= OrderInfoPrice +StopLoss
                    print(Prod,'空單買進時間',OrderInfoTime,'買進價格',OrderInfoPrice,'移動停損價位',StopLossPoint)
                    continue
    # 判斷時間是否到達出場時間
    elif RC.GetOpenInterest() == 1:
        # 超過出場時間則出場
        if CTime > CoverTime:
            # 透過下兩檔價委託空單(範圍市價單 委託三次 若未成交則當日不交易)
            OrderInfo=order.RangeMKTDeal(Broker,Prod,'S',Qty,'0','A',2,10)
            # 如果沒有成交則關閉程序
            if OrderInfo == False:
                GO.EndSubscribe()
            else:
                # 成交則寫入紀錄至部位管理物件 
                OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                OrderInfoPrice=float(OrderInfo[4])            
                RC.Cover('S',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                print(Prod,'多單到期平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                GO.EndSubscribe()
        # 當價格向上移動 則停損點數也向上移動
        elif CPrice - StopLoss > StopLossPoint:
            StopLossPoint = CPrice - StopLoss
            continue
        # 到達移動停損價位則出場
        elif CPrice < StopLossPoint:
            # 透過下兩檔價委託空單(範圍市價單 委託三次 若未成交則當日不交易)
            OrderInfo=order.RangeMKTDeal(Broker,Prod,'S',Qty,'0','A',2,10)
            # 如果沒有成交則關閉程序
            if OrderInfo == False:
                GO.EndSubscribe()
            else:
                # 成交則寫入紀錄至部位管理物件 
                OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                OrderInfoPrice=float(OrderInfo[4])            
                RC.Cover('S',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                print(Prod,'多單停損平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                GO.EndSubscribe()
    # 判斷時間是否到達出場時間
    elif RC.GetOpenInterest() == -1:
        # 超過出場時間則出場
        if CTime > CoverTime:
            # 透過上兩檔委託多單(範圍市價單 委託三次 若未成交則當日不交易)
            OrderInfo=order.RangeMKTDeal(Broker,Prod,'B',Qty,'0','A',2,10)
            # 如果沒有成交則關閉程序
            if OrderInfo == False:
                GO.EndSubscribe()
            else:
                # 成交則寫入紀錄至部位管理物件 
                OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                OrderInfoPrice=float(OrderInfo[4])            
                RC.Cover('B',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                print(Prod,'空單到期平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                GO.EndSubscribe()
        # 當價格向下移動 則停損點數也向下移動
        elif CPrice + StopLoss < StopLossPoint:
            StopLossPoint = CPrice + StopLoss
            continue
        # 到達移動停損價位則出場
        elif CPrice < StopLossPoint:
            # 透過上兩檔委託多單(範圍市價單 委託三次 若未成交則當日不交易)
            OrderInfo=order.RangeMKTDeal(Broker,Prod,'B',Qty,'0','A',2,10)
            # 如果沒有成交則關閉程序
            if OrderInfo == False:
                GO.EndSubscribe()
            else:
                # 成交則寫入紀錄至部位管理物件 
                OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                OrderInfoPrice=float(OrderInfo[4])            
                RC.Cover('B',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                print(Prod,'空單停損平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                GO.EndSubscribe()
    

print('績效紀錄:',RC.GetProfit())

    
