# -*- coding: UTF-8 -*-
# 載入相關套件
import haohaninfo,indicator,datetime,time,sys

# 選擇報價平台
Broker = sys.argv[1]
# 定義商品名稱
Prod = sys.argv[2]

# K棒物件     
Today=time.strftime('%Y%m%d')
KBar = indicator.KBar(Today,1) 

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價、成交量
    Price=int(row[2])
    Qty=int(row[3])
    # 將成交欄位填入
    KBar.AddPrice(Time,Price,Qty)
    # 取得RSI
    print(KBar.GetTime(),KBar.GetClose(),KBar.GetRSI(5))
