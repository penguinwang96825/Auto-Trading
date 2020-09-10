# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]

# 計算大戶指標
BO = indicator.BigOrder(0)
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    qty = int(i[3])
    bc = int(i[5])
    sc = int(i[6])
    BO.Add(qty,bc,sc)
    print(BO.Get())  
    