# 載入必要模組
from haohaninfo import GOrder
from order import Record
import numpy as np
from talib.abstract import BBANDS
import sys

# 登入帳號密碼(讀者須修正該帳號密碼為自己的，否則無法執行策略)
GOrder.Login('TestAccount','TestPasswd')
# 建立部位管理物件
OrderRecord=Record() 
# 取得回測參數、移動停損點數
StartDate=sys.argv[1]
EndDate=sys.argv[2]
BBANDSPeriod=int(sys.argv[3])
MoveStopLoss=float(sys.argv[4])
# 回測取報價物件
KBar=GOrder.GetTAKBar(StartDate,EndDate,'3008','Stock','0','5')
KBar['Upper'],KBar['Middle'],KBar['Lower']=BBANDS(KBar,timeperiod=BBANDSPeriod)
# 開始回測
for n in range(0,len(KBar['time'])-1):
    # 先判斷long MA的上一筆值是否為空值 再接續判斷策略內容
    if not np.isnan( KBar['Middle'][n-1] ) :
        # 如果無未平倉部位
        if OrderRecord.GetOpenInterest()==0 :
            # 當價格由下向上穿越 則進場做多
            if KBar['close'][n-1] <= KBar['Lower'][n-1] and KBar['close'][n] > KBar['Lower'][n]:
                OrderRecord.Order('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice * ( 1 - MoveStopLoss )
                continue
            # 當價格由上向下穿越 則進場做空
            if KBar['close'][n-1] >= KBar['Upper'][n-1] and KBar['close'][n] < KBar['Upper'][n]:
                OrderRecord.Order('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice * ( 1 + MoveStopLoss )
                continue
        # 如果有多單部位   
        elif OrderRecord.GetOpenInterest()==1 :
            # 逐筆更新移動停損價位
            if KBar['close'][n] * ( 1 - MoveStopLoss ) > StopLossPoint :
                StopLossPoint = KBar['close'][n] * ( 1 - MoveStopLoss )
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar['close'][n] < StopLossPoint :
                OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
            # 若大於 布林通道上界 則停利出場
            if KBar['close'][n] >= KBar['Upper'][n]:
                OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
        # 如果有空單部位
        elif OrderRecord.GetOpenInterest()==-1 :
            # 逐筆更新移動停損價位
            if KBar['close'][n] * ( 1 + MoveStopLoss ) < StopLossPoint :
                StopLossPoint = KBar['close'][n] * ( 1 + MoveStopLoss )
            # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
            elif KBar['close'][n] > StopLossPoint :
                OrderRecord.Cover('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
            # 若小於 布林通道下界 則停利出場
            if KBar['close'][n] <= KBar['Lower'][n]:
                OrderRecord.Cover('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                continue
                
# 將回測紀錄寫至MicroTest中
OrderRecord.StockMicroTestRecord('5-4-4-S',0.5)

# 繪製走勢圖加上MA以及下單點位
from chart import ChartOrder_BBANDS
ChartOrder_BBANDS(KBar,OrderRecord.GetTradeRecord())

