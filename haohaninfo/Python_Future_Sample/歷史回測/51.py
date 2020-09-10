# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import backtest_function 
from talib.abstract import *
# 取I020(成交資料)
I020 = backtest_function.GetI020()

# 定義停利停損點數
TakeProfit = 20
StopLoss = 10

# 開始回測
for date in backtest_function.GetDate(I020):
    # 取當日資料
    Data = [i for i in I020 if i[0] == date]
    # 取Ta-lib適用的分K資料
    TAKBar = backtest_function.ConvertTAKBar(date,Data)
    # 計算RSI指標(資料,期數)
    TAKBar['RSI6'] = RSI(TAKBar,6)
    # 計算MA指標(資料,期數)
    TAKBar['MA10'] = SMA(TAKBar,10)
    # 倉位為0
    index = 0
    
    # 資料長度足夠計算指標才開始判斷
    for i in range(10,len(TAKBar['time'])):
        # 當前時間、當前收盤價、當前RSI值、當前MA值、上一分鐘收盤價、上一分鐘MA值
        thisTime = TAKBar['time'][i]
        thisClose = TAKBar['close'][i]
        lastClose = TAKBar['close'][i-1]
        thisRSI = TAKBar['RSI6'][i]
        thisMA = TAKBar['MA10'][i]
        lastMA = TAKBar['MA10'][i-1]
                
        # 進場判斷
        if index == 0:
            # 多單進場
            if thisRSI > 50 and lastClose <= lastMA and thisClose > thisMA:
                index = 1
                OrderTime = thisTime
                OrderPrice = thisClose
            # 空單進場
            elif thisRSI < 50 and lastClose >= lastMA and thisClose < thisMA:
                index = -1
                OrderTime = thisTime
                OrderPrice = thisClose
            # 當日沒有交易
            elif i == len(TAKBar['time'])-1:
                print(date,'No Trade')
                break
        # 出場判斷
        elif index != 0:
            # 多單出場
            if index == 1:
                # 停利停損
                if thisClose >= OrderPrice + TakeProfit or thisClose <= OrderPrice - StopLoss:
                    CoverTime = thisTime			
                    CoverPrice = thisClose
                    Profit = CoverPrice - OrderPrice
                    print('B','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
                    break
                # 11:00出場
                elif i == len(TAKBar['time'])-1:
                    CoverTime = thisTime  			
                    CoverPrice = thisClose 	
                    Profit = CoverPrice - OrderPrice
                    print('B','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
            # 空單出場
            elif index == -1:
                # 停利停損
                if thisClose <= OrderPrice - TakeProfit or thisClose >= OrderPrice + StopLoss:
                    CoverTime = thisTime
                    CoverPrice = thisClose  	
                    Profit = OrderPrice - CoverPrice
                    print('S','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
                    break
                # 11:00出場
                elif i == len(TAKBar['time'])-1:
                    CoverTime = thisTime 			
                    CoverPrice = thisClose
                    Profit = OrderPrice - CoverPrice
                    print('S','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
    
