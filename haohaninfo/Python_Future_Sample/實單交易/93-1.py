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
# 計算大戶指標物件
BigOrder = indicator.BigOrder(20)
# 設定固定時間進場
StartTime = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')

# 進場策略
Index = 0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    BigOrder.Add(int(i[3]),int(i[5]),int(i[6]))
    OnceBuy,OnceSell,AccBigBuy,AccBigSell = BigOrder.Get()
    # 趨勢偏多
    if OnceBuy > 30 and AccBigBuy > 500:
        Index = 1
        OrderTime = time
        OrderPrice = price
        print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
        GO.EndDescribe()
    # 趨勢偏空
    elif OnceSell > 30 and AccBigSell > 500:
        Index = -1
        OrderTime = time
        OrderPrice = price
        print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
        GO.EndDescribe()

            
