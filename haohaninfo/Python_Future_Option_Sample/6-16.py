# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,indicator,datetime,time,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# 固定量K棒物件        
KBar = indicator.VolumeKBar(500) # 500口形成一根K棒 

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價、總成交量
    Price=int(row[2])
    Amount=int(row[4])
    # 將成交欄位填入
    KBar.AddPrice(Time,Price,Amount)
    print(KBar.GetTime(),KBar.GetOpen(),KBar.GetHigh(),KBar.GetLow(),KBar.GetClose())
