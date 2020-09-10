import sys
from backtest_function import GetHistoryData,DayList

sid=sys.argv[1]

# 定義區間、停損停利點
box_ratio = 0.02
stoploss_ratio = 0.015
takeprofit_ratio = 0.07


# 定義績效
TotalProfit=[]

for date in DayList():
    # 取得回測資料
    Data=GetHistoryData(date,sid)

    # 取得開盤價
    StartPrice = float(Data[0][2])
    
    # 進場判斷
    Index=0
    for i in range(1,len(Data)):
        price = float(Data[i][2])
        # 當價格突破上界
        if price >= StartPrice * (1+box_ratio):
            Index=1
            OrderTime=Data[i][0]
            OrderPrice=price
            # 制定停損停利點
            StopLossPoint=StartPrice * (1-stoploss_ratio)
            TakeProfitPoint=StartPrice * (1+takeprofit_ratio)
            break
        # 當價格突破下界
        elif price <= StartPrice * (1-box_ratio):
            Index=-1
            OrderTime=Data[i][0]
            OrderPrice=price
            # 制定停損停利點
            StopLossPoint=StartPrice * (1+stoploss_ratio)
            TakeProfitPoint=StartPrice * (1-takeprofit_ratio)
            break
        # 當天尚未進行交易
        elif i==len(Data)-1:
            print(date+' NO Trade')
    
    # 若沒有進行交易，則不進行接下來的判斷        
    if Index==0:
        continue
    
    # 定義出場判斷的資料，取得進場以後的資料
    Data1 = [ i for i in Data if int(i[0])>int(OrderTime) ]

    # 出場判斷
    if Index==1:
        for i in range(0,len(Data1)):
            price = float(Data1[i][2])
            # 停損判斷
            if price <= StopLossPoint:
                CoverTime=Data1[i][0]
                CoverPrice=price
                break
            # 停利判斷
            elif price >= TakeProfitPoint:
                CoverTime=Data1[i][0]
                CoverPrice=price
                break
            # 收盤強制出場
            elif i==len(Data1)-1:
                CoverTime=Data1[i][0]
                CoverPrice=price
        Profit=CoverPrice-OrderPrice
        TotalProfit+=[Profit]
        print(date,sid,'Buy OrderTime',OrderTime,'OrderPrice',OrderPrice,'CoverTime',CoverTime,'CoverPrice',CoverPrice,'Profit',Profit)
    elif Index==-1:
        for i in range(0,len(Data1)):
            price = float(Data1[i][2])
            # 停損判斷
            if price >= StopLossPoint:
                CoverTime=Data1[i][0]
                CoverPrice=price
                break
            # 停利判斷
            elif price <= TakeProfitPoint:
                CoverTime=Data1[i][0]
                CoverPrice=price
                break
            # 收盤強制出場
            elif i==len(Data1)-1:
                CoverTime=Data1[i][0]
                CoverPrice=price
        Profit=OrderPrice-CoverPrice
        TotalProfit+=[Profit]
        print(date,sid,'Sell OrderTime',OrderTime,'OrderPrice',OrderPrice,'CoverTime',CoverTime,'CoverPrice',CoverPrice,'Profit',Profit)


#顯示總績效
print('Total Profit',sum(TotalProfit))





