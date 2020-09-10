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
# 停損停利
TakeProfit=20
TakeProfitPrice=0
# 定義K棒物件(判斷區間)
MinuteKbar=KBar(Start,1) 
# 定義區間
Ceil=99999999999
Floor=0
Spread=0
GapRatio=0.1

# 策略迴圈 (GetHistoryDataByPeriod 改為取得即時報價即可轉為實單交易)
for row in GetHistoryDataByPeriod(DataPath,Broker,Product,'Match',Start,End):
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price = float(row[2])
    Qty = int(row[3])
    
    # 餵資料進K線物件
    ChangeFlag = MinuteKbar.AddPrice(Time,Price,Qty)
    # 如果有換K棒才會更新最高最低值
    if ChangeFlag == 1 and len(MinuteKbar.GetHigh())>=30 :
        Ceil = max(MinuteKbar.GetHigh()[-30:])
        Floor = min(MinuteKbar.GetLow()[-30:])
        Spread = Ceil - Floor
        
    # 判斷進場條件
    if OrderRecord.GetOpenInterest() == 0:
        # 當價格突破區間上方，
        if Price >= Ceil + Spread * GapRatio :
            # 進場多單
            OrderRecord.Order('B',Product,Time,Price,1)
            # 紀錄進場價格
            TakeProfitPrice = Price
            # 到下個迴圈循環
            continue
        # 賣方筆數較低，賣方平均成交口數較高，進場空單
        if Price <= Floor -  Spread * GapRatio :
            # 進場多單
            OrderRecord.Order('S',Product,Time,Price,1)
            # 紀錄進場價格
            TakeProfitPrice = Price
            # 到下個迴圈循環
            continue
    # 判斷多單出場條件
    elif OrderRecord.GetOpenInterest() == 1:    
        # 移動停損，更新下單後最高價
        if Price > TakeProfitPrice:
            TakeProfitPrice = Price
        # 回跌至最高價 扣除停利點數出場
        elif Price <= TakeProfitPrice - TakeProfit:  
            TakeProfit
            OrderRecord.Cover('S',Product,Time,Price,1)
    # 判斷空單出場條件
    elif OrderRecord.GetOpenInterest() == -1:    
        # 移動停損，更新下單後最低價
        if Price < TakeProfitPrice:
            TakeProfitPrice = Price
        # 回跌至最高價 扣除停利點數出場
        elif Price >= TakeProfitPrice + TakeProfit:  
            TakeProfit
            OrderRecord.Cover('B',Product,Time,Price,1)
            
print('總績效',sum(OrderRecord.GetProfit()),'個別績效',OrderRecord.GetProfit())
print('全部交易紀錄',OrderRecord.GetTradeRecord())

        
                