# 匯入套件
from haohaninfo.MicroTest import microtest_db

# 設定下單人員(MicroTest帳號)
Account = 'Test'
# 設定策略名稱
Strategy = 'Sample1_FixTime'
# 設定商品
Product = 'TXFA9'
# 設定策略單次買賣口數
Qty = '1'
# 設定手續費
Commission = '100'

# 設定交易稅
def getFutureTax(Oprice,Cprice):
   return str(round(Oprice * 200 * 0.00002) + round(Cprice * 200 * 0.00002))

# 轉換資料庫時間格式
def DBdate(date):
   return date[:4]+'-'+date[4:6]+'-'+date[6:8]

# 取資料
I020 = open('TXFA9.I020').readlines()
# 刪除換行符號並切割字串
I020 = [ i.strip('\n').split(',') for i in I020]
# 取日期唯一值
DateList = sorted(set([ i[0] for i in I020 ]))

for date in DateList:
    # 取當日資料
    data = [ i for i in I020 if i[0] == date ]
    # 取9:00~12:00資料
    data = [ i for i in data if i[1] >= '090000000000' and i[1] < '120000000000']
    # 進場時間及價格
    OrderTime = data[0][1]
    OrderTime = OrderTime[:2] + ':' + OrderTime[2:4] + ':' + OrderTime[4:6]
    OrderPrice = int(data[0][3])
    # 出場時間及價格
    CoverTime = data[-1][1]
    CoverTime = CoverTime[:2] + ':' + CoverTime[2:4] + ':' + CoverTime[4:6]
    CoverPrice = int(data[-1][3])
    # 計算稅金
    Tax = getFutureTax(OrderPrice,CoverPrice)
    # 印出交易紀錄
    print(Product,DBdate(date),OrderTime,OrderPrice,'B',Qty,DBdate(date),CoverTime,CoverPrice,Tax,Commission,Strategy,Account)
    # 寫入資料庫
    microtest_db.insert_to_server_db(Product,DBdate(date),OrderTime,str(OrderPrice),'B',Qty,DBdate(date),CoverTime,str(CoverPrice),Tax,Commission,Strategy,Account)
