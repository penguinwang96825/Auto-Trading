# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,indicator,datetime,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# 委託簿固定時間變動的物件        
Vol = indicator.AccVol(5) # 計算五分鐘的變動量

# 計算委託簿固定時間變動
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義總成交量
    Amount=int(row[4])
    # 將成交欄位填入
    Vol.Add(Time,Amount)
    print(Vol.Get())
