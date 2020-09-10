# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]

# 計算內外盤
BSP = indicator.BSPower()
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    price = int(i[2])
    qty = int(i[3]) 
    BSP.Add(price,qty)
    print(BSP.Get())
