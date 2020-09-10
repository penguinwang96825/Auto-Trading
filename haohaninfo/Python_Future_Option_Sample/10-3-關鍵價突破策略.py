# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime 
from order import Record
from indicator import getFutureDailyInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProduct=sys.argv[1]
# 定義交易商品
Product=sys.argv[2]
# 定義券商
Broker='Simulator'

# 定義初始倉位
OrderRecord=Record()
# 取得期貨行情資料
DailyInfo=getFutureDailyInfo(WebProduct,1)[0]
DailyTime,DailyHigh,DailyLow,DailyClose=DailyInfo[0],float(DailyInfo[4]),float(DailyInfo[5]),float(DailyInfo[6])

# 計算 Pivot Point
PP=(DailyHigh+DailyLow+DailyClose)/3
R3=DailyHigh+(2*(PP-DailyLow))
R2=PP+DailyHigh-DailyLow
R1=(PP*2)-DailyLow
S1=(PP*2)-DailyHigh
S2=PP-DailyHigh+DailyLow
S3=DailyLow+(2*(DailyHigh-PP))
print('R1',R1,'S1',S1,'R2',R2,'S2',S2)

# 定義持倉最久時間(180分鐘)
HoldTime=datetime.timedelta(minutes=180)

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
for row in GO.Subscribe( Broker, 'match', Product ):
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 如果部位為空
    if OrderRecord.GetOpenInterest() == 0:
        # 突破壓力支撐價位
        if Price > R1 and Price < R2:
            print('當前價',Price,'突破Pivot Point R1壓力價位',R1,'，多單進場')
            # 紀錄進場價格
            OrderPrice=Price
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 進場紀錄
            OrderRecord.Order('S',Product,Time,Price,1)
            GO.EndSubscribe()
        elif Price < S1 and Price > S2:
            print('當前價',Price,'突破Pivot Point S1支撐價位',S1,'，空單進場')
            # 紀錄進場價格
            OrderPrice=Price
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 進場紀錄
            OrderRecord.Order('S',Product,Time,Price,1)
            GO.EndSubscribe()
        elif Price > R2 or Price < S2:
            print('當前價',Price,'已突破R2、S2故不進場')
            GO.EndSubscribe()
# 多單出場
if OrderRecord.GetOpenInterest() == 1:
    for row in GO.Subscribe( Broker, 'match', Product ):
        # 取得時間、價格欄位
        Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
        Price=float(row[2])
        # 到出場時間後出場
        if Time >= LastOverTime:
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()       
        # 判斷回檔至PP停損
        elif Price <= PP :
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,Price,'停損出場')
            GO.EndSubscribe()   
        # 判斷至R2停利
        elif Price >= R2 :
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,Price,'停利出場')
            GO.EndSubscribe()    
            
# 空單出場
elif OrderRecord.GetOpenInterest() == -1:
    for row in GO.Subscribe( Broker, 'match', Product ):
        # 取得時間、價格欄位
        Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
        Price=float(row[2])
        # 到出場時間後出場
        if Time >= LastOverTime:
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()       
        # 判斷回檔至PP停損
        elif Price >= PP :
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,Price,'停損出場')
            GO.EndSubscribe()     
        # 判斷至S2停利
        elif Price >= S2 :
            # 多單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,Price,'停利出場')
            GO.EndSubscribe()      

print('全部交易紀錄',OrderRecord.GetTradeRecord())
