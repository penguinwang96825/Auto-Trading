# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'match'
# 定義商品名稱
Prod = sys.argv[1]

GO = haohaninfo.GOrder.GOQuote()
for row in GO.Describe( Broker, Table, Prod):
    print(row)

