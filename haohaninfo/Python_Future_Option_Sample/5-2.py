# 匯入模組
from indicator import GetHistoryDataByPeriod
from order import Record
import datetime,sys  


# 指定日期
DataPath=sys.argv[1]    # 'C:/Data'
Broker=sys.argv[2]      # 'simulator'
Product=sys.argv[3]     # 'TXFI9' 
Start=sys.argv[4]       # '20190830'
End=sys.argv[5]         # '20190911'

# 定義初始倉位
OrderRecord=Record()
# 紀錄當日進場標籤(若不為None則當日不再進場)
OrderFlag=None
# 停損停利
TakeProfit=50
StopLoss=15

# 策略迴圈 (GetHistoryDataByPeriod 改為取得即時報價即可轉為實單交易)
for row in GetHistoryDataByPeriod(DataPath,Broker,Product,'Match',Start,End):
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Hour = Time.hour
    Price = float(row[2])
    # 成交買筆、成交賣筆
    bCount = int(row[5])
    sCount = int(row[6])
    
    # 省略非日盤資料
    if Hour < 8 and Hour > 13:
        continue

    # 判斷進場條件
    if OrderRecord.GetOpenInterest() == 0:
        # 當日尚未進場
        if OrderFlag == None: 
            # 本策略僅在日盤(9點至13點)進場
            if Hour >= 9 and Hour < 13 :
                # 買方筆數較低，買方平均成交口數較高，進場多單
                if bCount < sCount :
                    # 進場多單
                    OrderRecord.Order('B',Product,Time,Price,1)
                    # 紀錄進場價格
                    OrderPrice = Price
                    # 記錄當天進場(每日只進場一次)
                    OrderFlag = Time.strftime('%Y%m%d')
                    # 到下個迴圈循環
                    continue
                # 賣方筆數較低，賣方平均成交口數較高，進場空單
                if bCount > sCount :
                    # 進場多單
                    OrderRecord.Order('S',Product,Time,Price,1)
                    # 紀錄進場價格
                    OrderPrice = Price
                    # 記錄當天進場(每日只進場一次)
                    OrderFlag = Time.strftime('%Y%m%d')
                    # 到下個迴圈循環
                    continue
        # 換日則再次進場
        elif Time.strftime('%Y%m%d') != OrderFlag:
            OrderFlag = None
    # 判斷多單出場條件
    elif OrderRecord.GetOpenInterest() == 1:    
        # 判斷停利
        if Price >= OrderPrice+TakeProfit: 
            OrderRecord.Cover('S',Product,Time,Price,1)
        # 判斷停損
        elif Price <= OrderPrice-StopLoss:
            OrderRecord.Cover('S',Product,Time,Price,1)   
        # 判斷到期出場   
        elif Hour == 13:
            OrderRecord.Cover('S',Product,Time,Price,1)
    # 判斷空單出場條件
    elif OrderRecord.GetOpenInterest() == -1:    
        # 判斷停利
        if Price <= OrderPrice-TakeProfit: 
            OrderRecord.Cover('B',Product,Time,Price,1)
        # 判斷停損
        elif Price >= OrderPrice+StopLoss:
            OrderRecord.Cover('B',Product,Time,Price,1)   
        # 判斷到期出場   
        elif Hour == 13:
            OrderRecord.Cover('B',Product,Time,Price,1)
            
print('總績效',sum(OrderRecord.GetProfit()),'個別績效',OrderRecord.GetProfit())
print('全部交易紀錄',OrderRecord.GetTradeRecord())

        
                