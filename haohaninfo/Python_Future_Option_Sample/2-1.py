# -*- coding: utf-8 -*-

# 載入檔案，並做欄位的轉值
Data = open('put-call-parity.txt').readlines()
Data = [ i.strip('\n').split(',') for i in Data ]
Data = [ [i[0],i[1],float(i[2])] for i in Data ]

# 定義商品名稱及價格
TXFname = 'TXFK9'
TXFprice= None
Callname = 'TXO11200K9'
Callprice= None
Putname = 'TXO11200W9'
Putprice= None
# 選擇權合成期貨的價格
Realprice = None

# 開始進行點差計算
for row in Data:
    # 當報價為期貨時
    if row[1] == TXFname:
        TXFprice = row[2]
        # 當買權及賣權都有報價，就開始計算點差
        if Callprice != None and Putprice != None :
            # 合成期貨的計算
            Realprice=Callprice-Putprice+11200
            # 當點差大於 5 並顯示 代表產生可以套利的機會
            if abs(TXFprice-Realprice) > 5 :
                print(row[0],TXFprice,Realprice,TXFprice-Realprice)
    # 當報價為買權時
    elif row[1] == Callname:
        Callprice = row[2]
    # 當報價為賣權時
    elif row[1] == Putname:
        Putprice = row[2]
    
        
