# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,indicator,datetime,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# 委託簿固定時間變動的物件        
CDiff = indicator.CommissionDiff(5) # 計算五分鐘的變動量

# 計算委託簿固定時間變動
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'commission', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義買方口數、買方筆數、賣方口數、賣方筆數
    BAmount=int(row[2])
    BCount=int(row[3])
    SAmount=int(row[4])
    SCount=int(row[5])
    # 將委託欄位填入
    CDiff.Add(Time,BAmount,BCount,SAmount,SCount)
    print(CDiff.GetOrderDiff())
