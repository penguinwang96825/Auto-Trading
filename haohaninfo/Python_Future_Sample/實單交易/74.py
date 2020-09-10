# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'commission'
# 定義商品名稱
Prod = sys.argv[1]

# 計算委託簿買賣平均口數
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    AvgBuy = int(i[3])/int(i[2])
    AvgSell = int(i[5])/int(i[4])
    print(AvgBuy,AvgSell)  
    
    
    