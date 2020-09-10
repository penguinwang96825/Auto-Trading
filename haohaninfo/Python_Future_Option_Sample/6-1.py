# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義資料表格
Table = sys.argv[2]
# 定義商品名稱
Prod = sys.argv[3]

# 定義報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe( Broker, Table, Prod ):
    print(row)
