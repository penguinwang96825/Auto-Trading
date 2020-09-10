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
# 定義MA週期
FastPeriod=9
SlowPeriod=16

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
        FastMA=KBar1M.GetWMA(FastPeriod)
        SlowMA=KBar1M.GetWMA(SlowPeriod)
        # 判斷是否有MA值
        if len(SlowMA)>=SlowPeriod+1:
            LastFastMA=FastMA[-2]
            LastSlowMA=SlowMA[-2]
            # 快線大於慢線
            if LastFastMA > LastSlowMA:
                OrderRecord.Order('B',Product,Time,Price,1)
                print(Time,'快線',LastFastMA,'慢線',LastSlowMA,'多單進場')
                GO.EndSubscribe()
            # 快線低於慢線
            elif LastFastMA < LastSlowMA:
                OrderRecord.Order('S',Product,Time,Price,1)
                print(Time,'快線',LastFastMA,'慢線',LastSlowMA,'空單進場')
                GO.EndSubscribe()
        

for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    Qty=float(row[3])
    ChangeKFlag=KBar1M.AddPrice(Time,Price,Qty)
    # 每分鐘判斷一次
    if ChangeKFlag==1:
        FastMA=KBar1M.GetWMA(FastPeriod)
        SlowMA=KBar1M.GetWMA(SlowPeriod)
        # 判斷是否有MA值
        if len(SlowMA)>=SlowPeriod+1:
            LastFastMA=FastMA[-2]
            LastSlowMA=SlowMA[-2]
            # 多單出場判斷
            if OrderRecord.GetOpenInterest() == 1:
                # 快線小於慢線
                if LastFastMA < LastSlowMA:
                    OrderRecord.Cover('S',Product,Time,Price,1)
                    print(Time,'快線',LastFastMA,'慢線',LastSlowMA,'多單出場')
                    GO.EndSubscribe()
            # 空單出場判斷
            elif OrderRecord.GetOpenInterest() == -1:
                # 快線大於慢線
                if LastFastMA > LastSlowMA:
                    OrderRecord.Cover('B',Product,Time,Price,1)
                    print(Time,'快線',LastFastMA,'慢線',LastSlowMA,'空單出場')
                    GO.EndSubscribe()
            

        
