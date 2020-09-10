# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]
# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# 設定大戶指標 差距進場點數、順差停利點數、逆差停損點數
BigDifferent = 500
BigPositive = 1000
BigNegative = 500
# 固定式停損點數、爆量出場口數、進場後過M分鐘出場
FixStopLoss = 15
BigVolume = 1000
OverOrdertime = datetime.timedelta(minutes=40)
# 計算大戶指標物件
BigOrder = indicator.BigOrder(20)
# 設定停止進場時間、出場時間
StopTime = datetime.datetime.strptime(Date+'12:20:00.00','%Y%m%d%H:%M:%S.%f')
EndTime = datetime.datetime.strptime(Date+'13:00:00.00','%Y%m%d%H:%M:%S.%f')

# 進場策略
Index = 0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    BigOrder.Add(int(i[3]),int(i[5]),int(i[6]))
    OnceBuy,OnceSell,AccBigBuy,AccBigSell = BigOrder.Get()
    # 超過可進場時間 當日不做交易
    if time >= StopTime:
        print("Today No Order")
        GO.EndDescribe()
    # 多單進場
    elif AccBigBuy-AccBigSell > BigDifferent:
        Index = 1
        OrderTime = time
        OrderPrice = price
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        GO.EndDescribe()
    # 空單進場
    elif AccBigSell-AccBigBuy > BigDifferent:
        Index = -1
        OrderTime = time
        OrderPrice = price
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        GO.EndDescribe()
    
# 重新計算大戶指標
BigOrder = indicator.BigOrder(20)
# 計算K棒成交量物件
Volume = indicator.AccVol(Date,1)
       
# 出場策略
# 持有多單
if Index == 1:
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price = float(i[2])
        qty = int(i[3])
        BigOrder.Add(int(i[3]),int(i[5]),int(i[6]))
        OnceBuy,OnceSell,AccBigBuy,AccBigSell = BigOrder.Get()
        Volume.Add(time,qty)

        # 大戶指標順差停利
        if AccBigBuy-AccBigSell > BigPositive:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 大戶指標逆差停損
        elif AccBigSell-AccBigBuy > BigNegative:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 固定式停損
        elif price <= OrderPrice-FixStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 爆量且獲利情況下出場
        elif Volume.Get() >= BigVolume and price > OrderPrice:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 進場後過M分鐘出場   
        elif time >= OrderTime + OverOrdertime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 13:00強制出場
        elif time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Buy Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        
# 持有空單
elif Index == -1:
    for i in GO.Describe(Broker, Table, Prod):
        time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
        price = float(i[2])
        qty = int(i[3])
        BigOrder.Add(int(i[3]),int(i[5]),int(i[6]))
        OnceBuy,OnceSell,AccBigBuy,AccBigSell = BigOrder.Get()
        Volume.Add(time,qty)
        # 大戶指標順差停利
        if AccBigSell-AccBigBuy > BigPositive:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 大戶指標逆差停損
        elif AccBigBuy-AccBigSell > BigNegative:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 固定式停損
        elif price >= OrderPrice+FixStopLoss:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 爆量且獲利情況下出場
        elif Volume.Get() >= BigVolume and price < OrderPrice:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 進場後過M分鐘出場   
        elif time >= OrderTime + OverOrdertime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
        # 13:00強制出場
        elif time >= EndTime:
            Index=0
            CoverTime=time
            CoverPrice=price
            print(CoverTime,"Cover Sell Price:",CoverPrice,"Success!")
            GO.EndDescribe()
    
    
    
    






       
