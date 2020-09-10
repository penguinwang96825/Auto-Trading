# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime,numpy
from order import Record
from indicator import KBar

# 定義交易商品
Product=sys.argv[1]
# 定義券商
Broker='Simulator'

# 定義初始倉位
OrderRecord=Record()
# 定義K棒物件
Today=datetime.datetime.now().strftime('%Y%m%d')
KBar1M=KBar(Today,1)
# 定義RSI週期
Period=10

# 訂閱報價
GO = haohaninfo.GOrder.GOQuote()
# 進場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    # 每分鐘判斷一次
    if ChangeKFlag==1:
        # 取得RSI
        RSI=KBar1M.GetRSI(Period)
        # 判斷是否有RSI值
        if len(RSI) >= Period+1:
            LastRSI=RSI[-2]
            # RSI小於10
            if LastRSI < 10:
                OrderRecord.Order('B',Product,Time,Price,1)
                print(Time,'價格',Price,'RSI',LastRSI,'多單進場')
                GO.EndSubscribe()
            # RSI大於90
            elif LastRSI > 90:
                OrderRecord.Order('S',Product,Time,Price,1)
                print(Time,'價格',Price,'RSI',LastRSI,'空單進場')
                GO.EndSubscribe()
        

# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    # 每分鐘判斷一次
    if ChangeKFlag==1:
        # 取得RSI
        RSI=KBar1M.GetRSI(Period)
        # 判斷是否有RSI值
        if len(RSI) >= Period+1:
            LastRSI=RSI[-2]
            # 多單出場
            if OrderRecord.GetOpenInterest() == 1:
                # RSI回歸50
                if LastRSI > 50:
                    OrderRecord.Cover('S',Product,Time,Price,1)
                    print(Time,'價格',Price,'RSI',LastRSI,'多單出場')
                    GO.EndSubscribe()
            # 空單出場
            if OrderRecord.GetOpenInterest() == -1:
                # RSI回歸50
                if LastRSI < 50:
                    OrderRecord.Cover('B',Product,Time,Price,1)
                    print(Time,'價格',Price,'RSI',LastRSI,'空單出場')
                    GO.EndSubscribe()
    
