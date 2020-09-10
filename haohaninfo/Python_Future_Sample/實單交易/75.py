# -*- coding: UTF-8 -*-
# 載入相關套件
import sys,indicator,datetime,haohaninfo

# 券商
Broker = 'Masterlink_Future'
# 定義資料類別
Table = 'commission'
# 定義商品名稱
Prod = sys.argv[1]
# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# 委託簿固定時間變動的物件        
CDIF = indicator.CommissionDiff(Date,5)

# 計算委託簿固定時間變動
GO = haohaninfo.GOrder.GOQuote()
for i in GO.Describe(Broker, Table, Prod):
    time = datetime.datetime.strptime(i[0],'%Y/%m/%d %H:%M:%S.%f')
    bc = int(i[2])
    bo = int(i[3])
    sc = int(i[4])
    so = int(i[5])
    CDIF.Add(time,bc,bo,sc,so)
    print(CDIF.GetOrderDiff())
    