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
# 每日進場標記、高低點判斷
LastOrderDay=''
CeilPrice={}
FloorPrice={}
Spread={}
MoveStopLoss=50

# 回測取報價物件
KBar=GOrder.GetTAKBar(StartDate,EndDate,'TXF','Future','1','1')
# 開始回測
for n in range(0,len(KBar['time'])):
    # 將日期取出
    Date=KBar['time'][n].strftime('%Y%m%d')
    # 如果無未平倉部位 並時間為指定的進場時間 則進場
    if OrderRecord.GetOpenInterest()==0 :
        # 在9點15 判斷當日高低點
        if KBar['time'][n].strftime('%H%M') <= "0916" :
            # 新的一天則新增一組key
            if Date not in CeilPrice.keys():
                CeilPrice[Date] = KBar['high'][n]
                FloorPrice[Date] = KBar['low'][n]
                Spread[Date]=(CeilPrice[Date]-FloorPrice[Date])*0.2
            else:
                CeilPrice[Date] = max(CeilPrice[Date],KBar['high'][n])
                FloorPrice[Date] = min(FloorPrice[Date],KBar['low'][n])
                Spread[Date]=(CeilPrice[Date]-FloorPrice[Date])*0.2
        # 在9:16以後 並且當日無進場，則開始判斷當日進場
        elif KBar['time'][n].strftime('%H%M') > "0916" and KBar['time'][n].strftime('%Y%m%d') != LastOrderDay : 
            if KBar['close'][n] > CeilPrice[Date] + Spread[Date] :
                OrderRecord.Order('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice -MoveStopLoss
                LastOrderDay = KBar['time'][n].strftime('%Y%m%d')
            elif KBar['close'][n] < FloorPrice[Date] - Spread[Date] :
                OrderRecord.Order('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
                OrderPrice = KBar['open'][n+1]
                StopLossPoint = OrderPrice +MoveStopLoss
                LastOrderDay = KBar['time'][n].strftime('%Y%m%d')
            
    # 如果有多單部位，則在1330點以後立即平倉    
    elif OrderRecord.GetOpenInterest()==1 :
        # 逐筆更新移動停損價位
        if KBar['close'][n] - MoveStopLoss > StopLossPoint :
            StopLossPoint = KBar['close'][n] - MoveStopLoss
        # 判斷到期出場
        if KBar['time'][n].strftime('%H%M') >= "1330" :
            OrderRecord.Cover('Sell', KBar['product'][n],KBar['time'][n],KBar['open'][n],1)
        # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
        elif KBar['close'][n] < StopLossPoint :
            OrderRecord.Cover('Sell', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
    
    # 如果有空單部位，則在1330點以後立即平倉    
    elif OrderRecord.GetOpenInterest()==-1 :
        # 逐筆更新移動停損價位
        if KBar['close'][n] + MoveStopLoss < StopLossPoint :
            StopLossPoint = KBar['close'][n] + MoveStopLoss
        # 判斷到期出場
        if KBar['time'][n].strftime('%H%M') >= "1330" :
            OrderRecord.Cover('Buy', KBar['product'][n],KBar['time'][n],KBar['open'][n],1)
        # 如果上一根K的收盤價觸及停損價位，則在最新時間出場
        elif KBar['close'][n] > StopLossPoint :
            OrderRecord.Cover('Buy', KBar['product'][n+1],KBar['time'][n+1],KBar['open'][n+1],1)
    
# 將回測紀錄寫至MicroTest中
OrderRecord.FutureMicroTestRecord('4-5-2-F',200,50)

# 繪製走勢圖以及下單點位
from chart import ChartOrder
ChartOrder(KBar,OrderRecord.GetTradeRecord())