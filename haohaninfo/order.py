# 載入必要套件
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from haohaninfo.MicroTest import microtest_db
import numpy as np
import haohaninfo,time
GOC = haohaninfo.GOrder.GOCommand()
GOQ = haohaninfo.GOrder.GOQuote()

# 下單部位管理物件
class Record():
    def __init__(self ):
        # 儲存績效
        self.Profit=[]
        # 未平倉
        self.OpenInterestQty=0
        self.OpenInterest=[]
        # 交易紀錄總計
        self.TradeRecord=[]
    # 進場紀錄
    def Order(self, BS,Product,OrderTime,OrderPrice,OrderQty):
        if BS=='B' or BS=='Buy':
            for i in range(OrderQty):
                self.OpenInterest.append([1,Product,OrderTime,OrderPrice])
                self.OpenInterestQty +=1
        elif BS=='S' or BS=='Sell':
            for i in range(OrderQty):
                self.OpenInterest.append([-1,Product,OrderTime,OrderPrice])
                self.OpenInterestQty -=1
    # 出場紀錄(買賣別需與進場相反，多單進場則空單出場)
    def Cover(self, BS,Product,CoverTime,CoverPrice,CoverQty):
        if BS=='S' or BS=='Sell':
            for i in range(CoverQty):
                # 取得多單未平倉部位
                TmpInterest=[ i for i in self.OpenInterest if i[0]==1 ][0]
                if TmpInterest != []:
                    # 清除未平倉紀錄
                    self.OpenInterest.remove(TmpInterest)
                    self.OpenInterestQty -=1
                    # 新增交易紀錄
                    self.TradeRecord.append(['B',TmpInterest[1],TmpInterest[2],TmpInterest[3],CoverTime,CoverPrice])
                    self.Profit.append(CoverPrice-TmpInterest[3])
                else:
                    print('尚無進場')
        elif BS=='B' or BS=='Buy':
            for i in range(CoverQty):
                # 取得空單未平倉部位
                TmpInterest=[ i for i in self.OpenInterest if i[0]==-1 ][0]
                if TmpInterest != []:
                    # 清除未平倉紀錄
                    self.OpenInterest.remove(TmpInterest)
                    self.OpenInterestQty +=1
                    # 新增交易紀錄
                    self.TradeRecord.append(['S',TmpInterest[1],TmpInterest[2],TmpInterest[3],CoverTime,CoverPrice])
                    self.Profit.append(TmpInterest[3]-CoverPrice)
                else:
                    print('尚無進場')
    # 取得當前未平倉量
    def GetOpenInterest(self):               
        # 取得未平倉量
        return self.OpenInterestQty
    # 取得交易紀錄
    def GetTradeRecord(self):               
        # 取得未平倉量
        return self.TradeRecord   
    # 取得交易績效
    def GetProfit(self):       
        return self.Profit  
    # 將股票的回測紀錄寫入MicroTest當中
    def StockMicroTestRecord(self,StrategyName,Discount):
        microtest_db.login('jack','1234','ftserver.haohaninfo.com')
        for row in self.TradeRecord:
            Fee=row[3]*1000*0.001425*Discount + row[5]*1000*0.001425*Discount 
            Tax=row[5]*1000*0.003
            microtest_db.insert_to_server_db(   \
            row[1],                             \
            row[2].strftime('%Y-%m-%d'),        \
            row[2].strftime('%H:%M:%S'),        \
            row[3],                             \
            row[0],                             \
            '1',                                \
            row[4].strftime('%Y-%m-%d'),        \
            row[4].strftime('%H:%M:%S'),        \
            row[5],                             \
            Tax,                                \
            Fee,                                \
            StrategyName)    
        microtest_db.commit()
    # 將期貨的回測紀錄寫入MicroTest當中
    def FutureMicroTestRecord(self,StrategyName,ProductValue,Fee):
        microtest_db.login('jack','1234','ftserver.haohaninfo.com')
        for row in self.TradeRecord:
            Tax=row[5]*ProductValue*0.00002*2
            microtest_db.insert_to_server_db(   \
            row[1],                             \
            row[2].strftime('%Y-%m-%d'),        \
            row[2].strftime('%H:%M:%S'),        \
            str(int(row[3])),                             \
            str(row[0]),                             \
            '1',                                \
            row[4].strftime('%Y-%m-%d'),        \
            row[4].strftime('%H:%M:%S'),        \
            str(row[5]),                             \
            str(int(Tax)),                                \
            str(int(Fee)),                                \
            StrategyName) 
        microtest_db.commit()
    # 取得交易績效
    def GetTotalProfit(self):  
        return sum(self.Profit)
    # 取得平均交易績效
    def GetAverageProfit(self): 
        return sum(self.Profit)/len(self.Profit)
    # 取得勝率
    def GetWinRate(self):
        WinProfit = [ i for i in self.Profit if i > 0 ]
        return len(WinProfit)/len(self.Profit)
    # 最大連續虧損
    def GetAccLoss(self):
        AccLoss = 0
        MaxAccLoss = 0
        for p in self.Profit:
            if p <= 0:
                AccLoss+=p
                if AccLoss < MaxAccLoss:
                    MaxAccLoss=AccLoss
            else:
                AccLoss=0
        return MaxAccLoss
    # 最大資金回落(MDD)
    def GetMDD(self):
        MDD,Capital,MaxCapital = 0,0,0
        for p in self.Profit:
            Capital += p
            MaxCapital = max(MaxCapital,Capital)
            DD = MaxCapital - Capital
            MDD = max(MDD,DD)
        return MDD
    # 平均獲利 
    def GetAverEarn(self):
        WinProfit = [ i for i in self.Profit if i > 0 ]
        return sum(WinProfit)/len(WinProfit)
    # 平均虧損
    def GetAverLoss(self):
        FailProfit = [ i for i in self.Profit if i < 0 ]
        return sum(FailProfit)/len(FailProfit)
    # 產出交易績效圖
    def GeneratorProfitChart(self,StrategyName='Strategy'):
        # 定義圖表
        ax1 = plt.subplot(111)
        # 計算累計績效
        TotalProfit=[0]
        for i in self.Profit:
            TotalProfit.append(TotalProfit[-1]+i)
        # 繪製圖形
        ax1.plot( TotalProfit  , '-', linewidth=1 )
        #定義標頭
        ax1.set_title('Profit')
        plt.show()    # 顯示繪製圖表
        # plt.savefig(StrategyName+'.png') #儲存繪製圖表
    

    

# 市價委託單(預設非當沖、倉別自動)
def OrderMKT(Broker,Product,BS,Qty,DayTrade='0',OrderType='A'):
    # 送出交易委託
    # print([Broker, Product, BS, '',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType])
    OrderNo=GOC.Order(Broker, Product, BS, '0',str(Qty), "IOC", "MKT" ,str(DayTrade),OrderType)
    print(OrderNo)
    # 判斷是否委託成功(這邊以元富為例)
    if OrderNo != '委託失敗':
        while True:
            # 取得成交帳務
            MatchInfo=GOC.MatchAccount(Broker,OrderNo)
            # 判斷是否成交
            if MatchInfo != []:
                # 成交則回傳
                return MatchInfo[0].split(',')
    else:
        return False
            
     
            
# 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
def OrderRangeMKT(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10): 
    # 新增訂閱要下單的商品，預防沒有取到該商品報價
    # GOC.AddQuote(Broker,Product,True)
    # 取得委託商品的上下五檔來進行限價委託(這邊預設下單與報價使用同一個券商，若不同則需另外調整)
    UpdnInfo=GOQ.SubscribeLast(Broker,'updn5',Product)
    # 如果是買單，則掛上五檔委託
    if BS == 'B':
        OrderPoint=UpdnInfo[OrderPriceLevel*2]
    elif BS == 'S':
        OrderPoint=UpdnInfo[10+OrderPriceLevel*2]
    # 送出交易委託
    print([Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType])
    OrderNo=GOC.Order(Broker, Product, BS, str(OrderPoint), str(Qty), "ROD", "LMT" ,str(DayTrade),OrderType )
    # 設定刪單時間
    EndTime=time.time()+Wait
    # 判斷是否委託成功(這邊以元富為例)
    if OrderNo != '委託失敗':
        # 若大於刪單時間則跳出迴圈
        while time.time() < EndTime:
            # 取得成交帳務
            MatchInfo=GOC.MatchAccount(Broker,OrderNo)
            # 判斷是否成交
            if MatchInfo != []:
                # 成交則回傳
                return MatchInfo[0].split(',')
            # 稍等0.5秒
            time.sleep(0.5)
            print('尚未成交')
        # 刪單並確認委託成功刪除
        GOC.Delete(Broker,OrderNo)
        GOC.GetAccount(Broker,OrderNo)
        print('到期刪單')
        return False
    else:
        return False 

# 範圍市價單(預設非當沖、倉別自動、掛上下N檔價1-5[預設3]、N秒尚未成交刪單[預設10])
def RangeMKTDeal(Broker,Product,BS, Qty,DayTrade='0',OrderType='A',OrderPriceLevel=3,Wait=10):
    # 防止例外狀況，最多下三次單
    for i in range(3):
        OrderInfo=OrderRangeMKT(Broker,Product,BS,Qty,DayTrade,OrderType,OrderPriceLevel,Wait)
        if OrderInfo != False:
            return OrderInfo
    # 三次委託皆失敗，建議當日不做交易
    return False
