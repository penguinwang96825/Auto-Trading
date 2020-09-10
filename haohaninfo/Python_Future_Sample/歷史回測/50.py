# -*- coding: UTF-8 -*-

# 載入相關套件及函數
import backtest_function
# 取I020(成交資料)
I020 = backtest_function.GetI020()

# 定義停利停損點數
TakeProfit = 30
StopLoss = 10

# 開始回測
for date in backtest_function.GetDate(I020):
    # 取當日資料
    Data = [i for i in I020 if i[0] == date]
    # 取當日9:00前的價格資料
    Data1 = [int(i[3]) for i in Data if int(i[1]) < 90000000000]
    # 取當日9:00~11:00資料
    Data2 = [i for i in Data if int(i[1]) >= 90000000000 and int(i[1]) <= 110000000000]
    # 定義上下界
    ceil = max(i for i in Data1)
    floor = min(i for i in Data1)
    # 倉位為0
    index = 0
    # 開始判斷
    for i in range(len(Data2)):
        # 當前時間、價格
        time = Data2[i][1]
        price = int(Data2[i][3]) 
        # 進場判斷
        if index == 0:
            # 多單進場
            if price > ceil:
                index = 1
                OrderTime = time
                OrderPrice = price				  
            # 空單進場
            elif price < floor:
                index = -1
                OrderTime = time
                OrderPrice = price	
            # 當日沒有交易
            elif i == len(Data2)-1:
                print(date,'No Trade')
                break
        # 出場判斷
        elif index != 0:
            # 多單出場
            if index == 1:
                # 停利停損
                if price >= OrderPrice + TakeProfit or price <= OrderPrice - StopLoss:
                    CoverTime = time			
                    CoverPrice = price
                    Profit = CoverPrice - OrderPrice
                    print('Date:',date,'B','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
                    break
                # 11:00出場
                elif i == len(Data2)-1:
                    CoverTime = time  			
                    CoverPrice = price 	
                    Profit = CoverPrice - OrderPrice
                    print('Date:',date,'B','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
            # 空單出場
            elif index == -1:
                # 停利停損
                if price <= OrderPrice - TakeProfit or price >= OrderPrice + StopLoss:
                    CoverTime = time
                    CoverPrice = price  	
                    Profit = OrderPrice - CoverPrice
                    print('Date:',date,'S','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
                    break
                # 11:00出場
                elif i == len(Data2)-1:
                    CoverTime = time 			
                    CoverPrice = price
                    Profit = OrderPrice - CoverPrice
                    print('Date:',date,'S','OrderTime:',OrderTime,'OrderPrice:',OrderPrice,'CoverTime:',CoverTime,'CoverPrice:',CoverPrice,'Profit:',Profit)
    
    
