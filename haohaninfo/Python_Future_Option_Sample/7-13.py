# -*- coding: utf-8 -*-
import sys,haohaninfo,datetime,numpy
from order import Record
from indicator import KBar,getPutCallRatio

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
# MA穿越次數
CrossFlag=0

# 取得前30日的Put Call Ratio 來判斷當天趨勢 
PCRData=getPutCallRatio()
PCR = [ float(i[-1]) for i in PCRData ]
# 取得Put Call Ratio的平均、最後一筆
PCRAver=sum(PCR)/len(PCR)
PCRLast=PCR[-1]

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
        if len(SlowMA)>=SlowPeriod+2:
            Last1FastMA,Last2FastMA=FastMA[-2],FastMA[-3]
            Last1SlowMA,Last2SlowMA=SlowMA[-2],SlowMA[-3]            
            # 如果最後一筆小於平均Put Call Ratio，趨勢偏多
            if PCRLast < PCRAver: 
                # 快線穿越慢線
                if Last1FastMA > Last1SlowMA and Last2FastMA < Last2SlowMA :
                    CrossFlag+=1
                    # 穿越第二次
                    if CrossFlag == 2:
                        OrderRecord.Order('B',Product,Time,Price,1)
                        print(Time,'快線',Last1FastMA,'慢線',Last1SlowMA,'多單進場')
                        GO.EndSubscribe()
            # 如果最後一筆大於平均Put Call Ratio，趨勢偏空
            if PCRLast > PCRAver:     
                # 快線穿越慢線
                if Last1FastMA < Last1SlowMA and Last2FastMA > Last2SlowMA :
                    CrossFlag+=1
                    # 穿越第二次
                    if CrossFlag == 2:
                        OrderRecord.Order('S',Product,Time,Price,1)
                        print(Time,'快線',Last1FastMA,'慢線',Last1SlowMA,'空單進場')
                        GO.EndSubscribe()

# 定義要進出場的時間(13:30出場)
OutTime=datetime.datetime.now().replace( hour=13 , minute=30 , second=00 , microsecond=00 )        

# 出場判斷
for row in GO.Subscribe( Broker, 'match', Product ):    
    # 取得時間、價格欄位
    Time=datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price=float(row[2])
    # 到出場時間後出場
    if Time >= OutTime:
        if OrderRecord.GetOpenInterest() == 1:
            # 多單出場
            OrderRecord.Cover('S',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()       
        if OrderRecord.GetOpenInterest() == -1:
            # 空單出場
            OrderRecord.Cover('B',Product,Time,Price,1)
            print(Time,'時間到出場')
            GO.EndSubscribe()      
        
