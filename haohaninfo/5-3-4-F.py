# 載入必要模組
from haohaninfo import GOrder
from order import Record
import numpy as np
from talib.abstract import RSI
import sys

# 登入帳號密碼(讀者須修正該帳號密碼為自己的，否則無法執行策略)
GOrder.Login('TestAccount','TestPasswd')
# 建立部位管理物件
OrderRecord=Record() 
# 取得回測參數、移動停損點數
StartDate=sys.argv[1]
EndDate=sys.argv[2]
LongRSIPeriod=int(sys.argv[3])
ShortRSIPeriod=int(sys.argv[4])
MoveStopLoss=float(sys.argv[5])
# 回測取報價物件
KBar=GOrder.GetTAKBar(StartDate,EndDate,'TXF','Future','0','10')
# 計算 RSI指標 以及定義中線
KBar['RSI_long']=RSI(KBar,timeperiod=LongRSIPeriod)
KBar['RSI_short']=RSI(KBar,timeperiod=ShortRSIPeriod)
KBar['Middle']=np.array([50]*len(KBar['time']))
# 開始回測
for n in range(0,len(KBar['time'])-1):
    # 先判斷long MA的上一筆值是否為空值 再接續判斷策略內容
    if not np.isnan( KBar['RSI_long'][n-1] ) :
        # 如果無未平倉部位
        if OrderRecord.GetOpenInterest()==0 :
            # short RSI 大於 long RSI 並且 long RSI 大於 50
            if KBar['RSI_short'][n-1] <= KBar['RSI_long'][n-1] and KBar['RSI_short'][n] > KBar['RSI_long'][n] and KBar['RSI_long'][n] > KBar['Middle'][n] :
                OrderRecord.Order('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice - MoveStopLoss
                print(KBar['time'][n] ,'Buy',KBar['RSI_short'][n-1] ,KBar['RSI_long'][n-1] , KBar['RSI_short'][n], KBar['RSI_long'][n])
                continue
            # short RSI 小於 long RSI 並且 long RSI 小於 50
            if KBar['RSI_short'][n-1] >= KBar['RSI_long'][n-1] and KBar['RSI_short'][n] < KBar['RSI_long'][n] and KBar['RSI_long'][n] < KBar['Middle'][n] :
                OrderRecord.Order('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice + MoveStopLoss
                continue
        # 如果有多單部位   
        elif OrderRecord.GetOpenInterest()==1 :
            # 結算平倉
            if KBar['product'][n+1] != KBar['product'][n] :
                OrderRecord.Cover('Sell', KBar['product'][n],KBar['time'][n],KBar['close'][n],1)
                continue
            # 逐筆更新移動停損價位
            if KBar['close'][n] - MoveStopLoss > StopLossPoint :
                StopLossPoint = KBar['close'][n] - MoveStopLoss
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar['close'][n] < StopLossPoint :
                OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
        # 如果有空單部位
        elif OrderRecord.GetOpenInterest()==-1 :
            # 結算平倉
            if KBar['product'][n+1] != KBar['product'][n] :
                OrderRecord.Cover('Buy', KBar['product'][n],KBar['time'][n],KBar['close'][n],1)
                continue
            # 逐筆更新移動停損價位
            if KBar['close'][n] + MoveStopLoss < StopLossPoint :
                StopLossPoint = KBar['close'][n] + MoveStopLoss
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar['close'][n] > StopLossPoint :
                OrderRecord.Cover('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
                
# 將回測紀錄寫至MicroTest中
OrderRecord.FutureMicroTestRecord('5-3-4-F',200,50)

# 繪製走勢圖加上MA以及下單點位
from chart import ChartOrder_RSI_1
ChartOrder_RSI_1(KBar,OrderRecord.GetTradeRecord())

