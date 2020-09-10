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
# 設定固定時間進場
StartTime = datetime.datetime.strptime(Date+'09:00:00.00','%Y%m%d%H:%M:%S.%f')

# 進場策略
Index = 0
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(i[2])
    # 現在時間 大於 進場時間
    if time > StartTime:
        # 買賣方平均每筆委託口數
        data = GO.DescribeLast(Broker, 'commission', Prod)
        time = datetime.datetime.strptime(data[0],'%Y/%m/%d %H:%M:%S.%f')
        # 買賣方平均每筆委託口數
        AvgBuy = int(data[3]) / int(data[2])
        AvgSell = int(data[5]) / int(data[4])
        # 趨勢偏多
        if AvgBuy > AvgSell:
            Index = 1
            OrderTime = time
            OrderPrice = price
            print(OrderTime,"Order Buy Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 趨勢偏空
        elif AvgBuy < AvgSell:
            Index = -1
            OrderTime = time
            OrderPrice = price
            print(OrderTime,"Order Sell Price:",OrderPrice,"Success!")
            GO.EndDescribe()
        # 趨勢尚未產生
        else:
            pass
            
