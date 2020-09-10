# 載入必要模組
from haohaninfo import GOrder
from order import Record
import sys

# 登入帳號密碼(讀者須修正該帳號密碼為自己的，否則無法執行策略)
GOrder.Login('TestAccount','TestPasswd')

# 建立部位管理物件
OrderRecord=Record() 

# 取得回測參數
StartDate=sys.argv[1]
EndDate=sys.argv[2]
# 停損停利點數設置
StopLoss=float(sys.argv[3])
TakeProfit=float(sys.argv[4])
LastOrderDay=''

# 回測取報價物件
KBar=GOrder.GetTAKBar(StartDate,EndDate,'TXF','Future','1','1')
# 開始回測
for n in range(0,len(KBar['time'])):
    # 如果無未平倉部位 並時間為指定的進場時間 則進場
    if OrderRecord.GetOpenInterest()==0 :
        # 如果最新的K線時間在 10點至11點內
        if KBar['time'][n].strftime('%H%M') >= "1000" and KBar['time'][n].strftime('%H%M') <= "1100" :
            OrderRecord.Order('Buy', KBar['product'][n],KBar['time'][n],KBar['open'][n],1)
            OrderPrice = KBar['open'][n+1]
            StopLossPoint = OrderPrice - StopLoss
            TakeProfitPoint = OrderPrice + TakeProfit
            LastOrderDay = KBar['time'][n].strftime('%Y%m%d')
    # 如果有未平倉部位，則在11點以後立即平倉    
    elif OrderRecord.GetOpenInterest()==1 :
        # 如果最新的K線時間超過 11點
        if KBar['time'][n].strftime('%H%M') >= "1100" :
            OrderRecord.Cover('Sell', KBar['product'][n],KBar['time'][n],KBar['open'][n],1)
        # 如果上一根K的收盤價觸及停利價位，則在最新時間出場
        elif KBar['close'][n] > TakeProfitPoint :
            OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
        # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
        elif KBar['close'][n] < StopLossPoint :
            OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
    
# 將回測紀錄寫至MicroTest中
OrderRecord.FutureMicroTestRecord('4-4-2-F',200,50)