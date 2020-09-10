# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import backtest_function
# 取I020(成交資料)
I020 = backtest_function.GetI020()
# 定義停損點數
StopLoss = 10

# 開始回測
for date in backtest_function.GetDate(I020):
    # 取當日資料
    Data = [i for i in I020 if i[0] == date]
    # 取當日9:00~11:00資料
    Data1 = [i for i in Data if int(i[1]) >= 90000000000 and int(i[1]) <= 110000000000]
    # 進場時間、進場價格
    OrderTime = Data1[0][1]
    OrderPrice = int(Data1[0][3]) 
    # 出場判斷
    for i in range(1,len(Data1)):
        time = Data1[i][1]
        price = int(Data1[i][3])
        # 停損出場
        if price <= OrderPrice - StopLoss:
            # 出場時間、出場價格
            CoverTime = time
            CoverPrice = price
            break
        # 11:00出場
        elif i == len(Data1) - 1:
            # 出場時間、出場價格
            CoverTime = time
            CoverPrice = price         
    # 計算損益
    Profit = CoverPrice - OrderPrice
    # 印出交易紀錄
    print('Date:',date,'OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
    
    
    
