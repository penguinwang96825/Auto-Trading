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
# K棒物件
KBar = indicator.KBar(Date,'volume',100)

# 計算成交量K棒
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    price = int(i[2])
    amount = int(i[4])
    KBar.VolumeAdd(price,amount)
    print(KBar.GetOpen(),KBar.GetHigh(),KBar.GetLow(),KBar.GetClose())
    
    
    