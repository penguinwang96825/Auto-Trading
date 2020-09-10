# 載入必要函數
import indicator,sys,time,datetime,haohaninfo,order

# 取得必要參數 券商代號 商品名稱
Broker = sys.argv[1]
Prod = sys.argv[2]
Qty = int(sys.argv[3])

# 部位管理物件
RC=order.Record()

# 進出場時間   
Today = time.strftime('%Y%m%d')
OrderTime = datetime.datetime.strptime(Today + ' 09:30:00','%Y%m%d %H:%M:%S')
CoverTime = datetime.datetime.strptime(Today + ' 11:25:00','%Y%m%d %H:%M:%S')

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    CTime = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 判斷時間是否到達進場時間
    if CTime > OrderTime and RC.GetOpenInterest() == 0:
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
            print(Prod,'多單買進時間',OrderInfoTime,'買進價格',OrderInfoPrice)
            continue
    # 判斷時間是否到達出場時間
    elif CTime > CoverTime and RC.GetOpenInterest() != 0:
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
            print(Prod,'多單平倉時間',OrderInfoTime,'平倉價格',OrderInfoPrice)
            GO.EndSubscribe()
    
print('績效紀錄:',RC.GetProfit())
    
