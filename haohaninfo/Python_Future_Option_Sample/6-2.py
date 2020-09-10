# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# 定義報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe( Broker, 'match', Prod ):
    # 定義總量、買方筆數、賣方筆數
    Amount=int(row[4])
    BCount=int(row[5])
    SCount=int(row[6])
    # 平均買方筆數、平均賣方筆數
    AverB=Amount/BCount
    AverS=Amount/SCount
    print(row[0],AverB,AverS)