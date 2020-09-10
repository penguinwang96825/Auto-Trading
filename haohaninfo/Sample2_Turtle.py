# 匯入套件
from haohaninfo.MicroTest import microtest_db

# 設定下單人員(MicroTest帳號)
Account = 'Test'
# 設定策略名稱
Strategy = 'Sample2_Turtle'
# 設定商品
Product = 'TXFA9'
# 設定策略單次買賣口數
Qty = '1'
# 設定手續費
Commission = '100'

#設定交易稅
def getFutureTax(Oprice,Cprice):
   return str(round(Oprice * 200 * 0.00002) + round(Cprice * 200 * 0.00002))

#轉換資料庫時間格式
def DBdate(date):
   return date[:4]+'-'+date[4:6]+'-'+date[6:8]

# 取資料
I020 = open(Product+'.I020').readlines()
# 刪除換行符號並切割字串
I020 = [ i.strip('\n').split(',') for i in I020]
# 取日期唯一值
DateList = sorted(set([ i[0] for i in I020 ]))

for date in DateList:
    # 取當日資料
    data = [ i for i in I020 if i[0] == date ]
    # 取8:45~9:00的成交價
    data1 = [ int(i[3]) for i in data if i[1] >= '084500000000' and i[1] < '090000000000']
    # 區間高低點
    MaxPrice = max(data1)
    MinPrice = min(data1)
    # 需突破的額外點數
    Gap = (MaxPrice - MinPrice) * 0.5

    # 取9:00過後的資料
    data2 = [ i for i in data if i[1] >= '090000000000']
    # 進出場判斷
    BS = None
    for i in range(0,len(data2)):
        time = data2[i][1]
        time = time[:2] + ':' + time[2:4] + ':' + time[4:6]
        price = int(data2[i][3])

        # 多單進場(突破區間最高價外加額外點數)
        if BS == None and price > MaxPrice + Gap:
            BS = 'B'
            OrderTime = time
            OrderPrice = price
        # 空單進場(跌破區間最低價外加額外點數)
        elif BS == None and price < MinPrice - Gap:
            BS = 'S'
            OrderTime = time
            OrderPrice = price
    
        # 多單出場
        if BS == 'B' and i == len(data2)-1:
            CoverTime = time
            CoverPrice = price
            # 計算稅金
            Tax = getFutureTax(OrderPrice,CoverPrice)
            #印出交易資料
            print(Product,DBdate(date),OrderTime,OrderPrice,BS,Qty,DBdate(date),CoverTime,CoverPrice,Tax,Commission,Strategy,Account)
            #寫入資料庫
            microtest_db.insert_to_server_db(Product,DBdate(date),OrderTime,str(OrderPrice),BS,Qty,DBdate(date),CoverTime,str(CoverPrice),Tax,Commission,Strategy,Account)
            break
        # 空單出場
        elif BS == 'S' and i == len(data2)-1:
            CoverTime = time
            CoverPrice = price
            # 計算稅金
            Tax = getFutureTax(OrderPrice,CoverPrice)
            #印出交易資料
            print(Product,DBdate(date),OrderTime,OrderPrice,BS,Qty,DBdate(date),CoverTime,CoverPrice,Tax,Commission,Strategy,Account)
            #寫入資料庫
            microtest_db.insert_to_server_db(Product,DBdate(date),OrderTime,str(OrderPrice),BS,Qty,DBdate(date),CoverTime,str(CoverPrice),Tax,Commission,Strategy,Account)
            break
