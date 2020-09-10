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
for row in GO.Subscribe( Broker, 'commission', Prod ):
    # 定義買方口數、買方筆數、賣方口數、賣方筆數
    BAmount=int(row[2])
    BCount=int(row[3])
    SAmount=int(row[4])
    SCount=int(row[5])
    # 平均委託買方筆數、平均委託賣方筆數
    AverB=BAmount/BCount
    AverS=SAmount/SCount
    print(row[0],AverB,AverS)