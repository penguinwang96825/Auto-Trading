# 匯入模組
from indicator import GetHistoryDataByPeriod,KBar
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
# 定義K棒物件(判斷區間)
MinuteKbar=KBar(Start,1) 
# 定義MA、RSI週期
MAPeriod=10
RSIPeriod=30

# 策略迴圈 (GetHistoryDataByPeriod 改為取得即時報價即可轉為實單交易)
for row in GetHistoryDataByPeriod(DataPath,Broker,Product,'Match',Start,End):
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price = float(row[2])
    Qty = int(row[3])
    
    # 餵資料進K線物件
    ChangeFlag = MinuteKbar.AddPrice(Time,Price,Qty)
    # 如果有換K棒才會取得MA以及RSI
    if ChangeFlag == 1 :
        # 最少要滿足技術指標週期，才開始判斷
        if len(MinuteKbar.GetClose()) < max(MAPeriod,RSIPeriod) :
            continue
        # 取得最新的、上一筆收盤價
        Close=MinuteKbar.GetClose()[-2]
        # 取得最新的、上一筆MA
        MA=MinuteKbar.GetWMA(10)[-2]
        # 取得最新的RSI
        RSI=MinuteKbar.GetRSI(30)[-2]
        
        # 判斷進場條件
        if OrderRecord.GetOpenInterest() == 0:
            # RSI 大於 50 且 價格 > MA 
            if RSI > 50 and Close > MA :
                # 進場多單
                OrderRecord.Order('B',Product,Time,Price,1)
                # 到下個迴圈循環
                continue
            # RSI 小於 50 且 價格 < MA 
            elif RSI < 50 and Close < MA :
                # 進場多單
                OrderRecord.Order('S',Product,Time,Price,1)
                # 到下個迴圈循環
                continue
        # 判斷多單出場條件
        elif OrderRecord.GetOpenInterest() == 1:    
            # RSI 小於 50 且 價格 > MA 
            if RSI < 50 and Close > MA :
                OrderRecord.Cover('S',Product,Time,Price,1)
        # 判斷空單出場條件
        elif OrderRecord.GetOpenInterest() == -1:    
            # RSI 大於 50 且 價格 > MA 
            if RSI > 50 and Close < MA :
                OrderRecord.Cover('B',Product,Time,Price,1)
            
print('總績效',sum(OrderRecord.GetProfit()),'個別績效',OrderRecord.GetProfit())
print('全部交易紀錄',OrderRecord.GetTradeRecord())
OrderRecord.GeneratorProfitChart()