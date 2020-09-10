# 載入必要函數
import indicator,sys,time,datetime,haohaninfo

# 取得必要參數 券商代號 商品名稱
Broker = sys.argv[1]
Prod = sys.argv[2]

# K棒物件     
Today = time.strftime('%Y%m%d')
KBar = indicator.KBar(Today,1) 

# 訂閱報價物件
GO = haohaninfo.GOrder.GOQuote()
# 訂閱報價
for row in GO.Subscribe(Broker, 'match', Prod):
    # 定義時間
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    # 定義成交價、成交量
    Price=float(row[2])
    Qty=int(row[3])
    # 將成交欄位填入
    KBar.AddPrice(Time,Price,Qty)
    print(KBar.GetTime(),KBar.GetBBands(10))
