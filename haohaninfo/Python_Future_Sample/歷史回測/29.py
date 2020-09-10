# -*- coding: UTF-8 -*-

#載入相關套件及函數
import datetime
import backtest_function

#取得歷史資料
Data=backtest_function.GetI020()

#透過迴圈取得每天的資料
for date in backtest_function.GetDate(Data):
    
    #取得當日的時間
    I020 = [ line for line in Data if line[0] == date ]
    
    #取得轉換時間字串至時間格式
    Time = [ datetime.datetime.strptime(date + ' ' +line[1],"%Y%m%d %H%M%S%f") for line in I020 ]

    #價格由字串轉數值
    Price = [ int(line[3]) for line in I020 ]
    
    # 設定算起始時間 、 計算週期 、 長度
    StartTime =datetime.datetime.strptime(date + ' 084500',"%Y%m%d %H%M%S")
    Cycle = datetime.timedelta( 0 , 60 )
    MA_Length = 10
    MA_Array = []
    MA_Value = []
    for i in range(len(Price)):
        time = Time[i]
        price = Price[i]
        if len(MA_Array) == 0:
            MA_Array.append(price)
        else:
            if time < StartTime+Cycle:
                MA_Array[-1] = price
            else:
                StartTime+=Cycle
                if len(MA_Array) == MA_Length:
                    MA_Array=MA_Array[1:]
                    MA_Array.append(price)
                else:
                    MA_Array.append(price)
        MA_Value.append(sum(MA_Array)/len(MA_Array))
        
    print(MA_Value)    
    

    #僅執行一天就離開 若要執行整個契約週期 可將該行移除
    break