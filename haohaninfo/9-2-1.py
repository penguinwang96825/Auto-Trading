# 載入必要函數
import indicator,sys,time,datetime,haohaninfo,order
import numpy as np

# 取得必要參數 券商代號 商品名稱
Broker = sys.argv[1]
Prod = sys.argv[2]
KMinute= int(sys.argv[3])
ShortMAPeriod= int(sys.argv[4])
LongMAPeriod= int(sys.argv[5])
StopLoss= int(sys.argv[6])

# 部位管理物件
RC=order.Record()

# K棒物件     
Today = time.strftime('%Y%m%d')
KBar = indicator.KBar(Today,KMinute) 

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價、成交量
    Price=float(row[2])
    Qty=int(row[3])
    # 更新K棒 若新增K棒則判斷開始判斷 策略
    if KBar.AddPrice(Time,Price,Qty) == 1:
        CloseList=KBar.GetClose()
        # 如果 長MA 計算出值 則開始判斷進出場
        if len(CloseList) >= LongMAPeriod+2:
            LongMAList = KBar.GetEMA(LongMAPeriod)
            ShortMAList=KBar.GetEMA(ShortMAPeriod)
            ClosePrice=CloseList[-2]
            LongMA=LongMAList[-2]
            ShortMA=ShortMAList[-2]
            LastClosePrice=CloseList[-3]
            LastLongMA=LongMAList[-3]
            LastShortMA=ShortMAList[-3]
            print(RC.GetOpenInterest(),Time,'最新收盤價',ClosePrice,'上一筆收盤價',LastClosePrice,'最新短MA',ShortMA,'上一筆最新短MA',LastShortMA,'最新長MA',LongMA,'上一筆最新長MA',LastLongMA)
            # 判斷進場的部分
            if RC.GetOpenInterest() == 0:
                # 黃金交叉 買進多單
                if LastShortMA <= LastLongMA and ShortMA > LongMA:
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
                        # 紀錄移動停損停利價位
                        StopLossPoint= OrderInfoPrice-StopLoss
                        print(Prod,'多單進場買進時間',OrderInfoTime,'買進價格',OrderInfoPrice,'停損價位',StopLossPoint)
                        GO.EndSubscribe()
                # 死亡交叉 買進空單
                elif LastShortMA >= LastLongMA and ShortMA < LongMA:
                    # 透過下兩檔價委託空單(範圍市價單 委託三次 若未成交則當日不交易)
                    OrderInfo=order.RangeMKTDeal(Broker,Prod,'S',Qty,'0','A',2,10)
                    # 如果沒有成交則關閉程序
                    if OrderInfo == False:
                        GO.EndSubscribe()
                    else:
                        # 成交則寫入紀錄至部位管理物件 
                        OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                        OrderInfoPrice=float(OrderInfo[4])            
                        RC.Order('S',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                        # 紀錄移動停損停利價位
                        StopLossPoint= OrderInfoPrice+StopLoss
                        print(Prod,'空單買進時間',OrderInfoTime,'買進價格',OrderInfoPrice,'停損價位',StopLossPoint)
                        GO.EndSubscribe()
            # 判斷多單出場的部分
            elif RC.GetOpenInterest() == 1:
                # 移動停損判斷
                if ClosePrice-StopLoss > StopLossPoint:
                    StopLossPoint=ClosePrice-StopLoss 
                elif ClosePrice <= StopLossPoint:
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
                        # 紀錄移動停損停利價位
                        StopLossPoint= OrderInfoPrice-StopLoss
                        print(Prod,'多單平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                        GO.EndSubscribe()
            # 判斷空單出場的部分
            elif RC.GetOpenInterest() == -1:
                # 移動停損判斷
                if ClosePrice+StopLoss < StopLossPoint:
                    StopLossPoint=ClosePrice+StopLoss 
                elif ClosePrice >= StopLossPoint:
                    # 透過下兩檔價委託空單(範圍市價單 委託三次 若未成交則當日不交易)
                    OrderInfo=order.RangeMKTDeal(Broker,Prod,'B',Qty,'0','A',2,10)
                    # 如果沒有成交則關閉程序
                    if OrderInfo == False:
                        GO.EndSubscribe()
                    else:
                        # 成交則寫入紀錄至部位管理物件 
                        OrderInfoTime=datetime.datetime.strptime(OrderInfo[7],'%Y/%m/%d %H:%M:%S')
                        OrderInfoPrice=float(OrderInfo[4])            
                        RC.Cover('B',Prod,OrderInfoTime,OrderInfoPrice,Qty)
                        # 紀錄移動停損停利價位
                        StopLossPoint= OrderInfoPrice-StopLoss
                        print(Prod,'多單平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
                        GO.EndSubscribe()
                
                
print('績效紀錄:',RC.GetProfit())