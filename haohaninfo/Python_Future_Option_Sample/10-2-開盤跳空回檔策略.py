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
# 取得最前一日的行情資料、近月商品
LastDailyInfo=getFutureDailyInfo(WebProduct,1)[0]
# 取得前日收盤價
LastDailyClosePrice=int(LastDailyInfo[6])
# 定義持倉最久時間(300分鐘)
HoldTime=datetime.timedelta(minutes=180)
# 大於多少跳空點數進場
Gap=20
# 移動停損點數
StopLoss=10

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):
    # print(row)
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    
    # print('昨日收盤價:',LastDailyClosePrice,'價格',Price)
    # 如果部位為空
    if OrderRecord.GetOpenInterest() == 0:
        # 判斷向上跳空，放空
        if Price > LastDailyClosePrice+Gap :
            print('向上跳空',Price - LastDailyClosePrice,'點')
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 紀錄進場價格
            OrderPrice=Price
            # 進場紀錄
            OrderRecord.Order('S',Product,Time,Price,1)
            # 取得第一筆報價即跳出該迴圈
            GO.EndSubscribe()
        # 判斷向下跳空，做多
        elif Price < LastDailyClosePrice-Gap:
            print('向上跳空',LastDailyClosePrice - Price,'點')
            # 定義最後出場時間
            LastOverTime=Time+HoldTime
            # 紀錄進場價格
            OrderPrice=Price
            # 進場紀錄
            OrderRecord.Order('B',Product,Time,Price,1)
            # 取得第一筆報價即跳出該迴圈
            GO.EndSubscribe()
        else:
            print('無足夠跳空缺口')
            # 取得第一筆報價即跳出該迴圈
            GO.EndSubscribe()
            
# 多單出場
if OrderRecord.GetOpenInterest() == 1:
    print('啟動多單出場程序')
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
        # 判斷固定停損
        elif Price <= OrderPrice - StopLoss :
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,Price,'停損出場')
            GO.EndSubscribe()    
        # 跳空回檔出場
        elif Price >= LastDailyClosePrice :
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,Price,'跳空回檔出場')
            GO.EndSubscribe()   
            
# 空單出場
elif OrderRecord.GetOpenInterest() == -1:
    print('啟動空單出場程序')
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
        # 判斷固定停損
        elif Price >= OrderPrice + StopLoss :
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,Price,'停損出場')
            GO.EndSubscribe()     
        # 跳空回檔出場
        elif Price <= LastDailyClosePrice :
            # 多單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,Price,'跳空回檔出場')
            GO.EndSubscribe()   

print('全部交易紀錄',OrderRecord.GetTradeRecord())