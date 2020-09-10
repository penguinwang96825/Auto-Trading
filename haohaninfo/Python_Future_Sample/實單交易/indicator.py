# -*- coding: UTF-8 -*-
# 載入相關套件
import talib,numpy,datetime
            
# K線指標class
# 參數 型態(1:'time' , 2:'volume') 週期
class KBar():
    def __init__(self, date, type='time', cycle=1):
        if type == 'time':
            # 定義週期
            self.Cycle=datetime.timedelta(minutes=cycle)
            # 定義初始時間
            self.Time=datetime.datetime.strptime( date+'084500','%Y%m%d%H%M%S' )-(self.Cycle*2)
            # 定義開高低收量
            self.Open=numpy.array([])
            self.High=numpy.array([])
            self.Low=numpy.array([])
            self.Close=numpy.array([])
            self.Volume=numpy.array([])
        elif type == 'volume':
            # 定義周期
            self.Cycle=cycle
            # 定義初始成交量
            self.Amount=0
            # 定義開高低收
            self.Open=numpy.array([])
            self.High=numpy.array([])
            self.Low=numpy.array([])
            self.Close=numpy.array([])
    # 填入即時報價(time)
    def TimeAdd(self,time,price,qty):
        # 沒有換分鐘
        if time < self.Time+self.Cycle:
            self.Close[-1]=price
            self.Volume[-1]+=qty
            if price > self.High[-1]:
                self.High[-1] = price
            elif price < self.Low[-1]:
                self.Low[-1] = price
            return 0
        # 穿越指定時間週期 新增一根K棒
        elif time >= self.Time+self.Cycle:
            while time >= self.Time+self.Cycle:
                self.Time+=self.Cycle
            self.Open=numpy.append(self.Open,price)
            self.High=numpy.append(self.High,price)
            self.Low=numpy.append(self.Low,price)
            self.Close=numpy.append(self.Close,price)
            self.Volume=numpy.append(self.Volume,qty)
            return 1
    # 填入即時報價(volume)
    def VolumeAdd(self,price,amount):
        # 如果是第一筆資料
        if self.Amount==0:
            self.Open=numpy.append(self.Open,price)
            self.High=numpy.append(self.High,price)
            self.Low=numpy.append(self.Low,price)
            self.Close=numpy.append(self.Close,price)
            self.Amount=amount
        # 確認是否過了特定成交量
        elif amount - self.Amount < self.Cycle:
            self.Close[-1]=price
            if price > self.High[-1]:
                self.High[-1] = price
            elif price < self.Low[-1]:
                self.Low[-1] = price
            return 0
        # 達到特定成交量 新增一根K棒
        elif amount - self.Amount > self.Cycle:
            self.Open=numpy.append(self.Open,price)
            self.High=numpy.append(self.High,price)
            self.Low=numpy.append(self.Low,price)
            self.Close=numpy.append(self.Close,price)
            self.Amount=amount
            return 1
    # 取得開盤價陣列
    def GetOpen(self):
        return self.Open
    # 取得最高價陣列
    def GetHigh(self):
        return self.High
    # 取得最低價陣列
    def GetLow(self):
        return self.Low
    # 取得收盤價陣列    
    def GetClose(self):
        return self.Close
    # 取得累積成交量
    def GetVolume(self):
        return self.Volume
    # 取得移動平均線
    def GetSMA(self,tn=10):
        return talib.MA(self.Close,timeperiod=tn,matype=0)
    # 取得量能移動平均
    def GetQMA(self,tn=5):
        return talib.MA(self.Volume,timeperiod=tn,matype=0)
    # 取得MACD
    def GetMACD(self,fastp=12,slowp=24,signalp=7):    
        return talib.MACD(self.Close, fastperiod=fastp, slowperiod=slowp, signalperiod=signalp)
    # 取得布林通道指標
    def GetBBANDS(self,tp=10):
        return talib.BBANDS(self.Close,timeperiod=tp,matype=0)    
    # 取得KD
    def GetKD(self):
        return talib.STOCH(self.High, self.Low, self.Close)      
    # 取得威廉指標        
    def GetWILLR(self,tp=14):  
        return talib.WILLR(self.High, self.Low, self.Close, timeperiod=tp)
    # 取得RSI
    def GetRSI(self,tp=14):
        return talib.RSI(self.Close, timeperiod=tp)
    # 取得乖離率
    def GetBIAS(self,tn=10):
        mavalue=talib.MA(self.Close,timeperiod=tn,matype=0)
        return (self.Close-mavalue)/mavalue

# 計算內外盤類別         
class BSPower():
    def __init__(self):
        self.BP=0
        self.SP=0
        self.LastPrice=None
    def Add(self,price,qty):
        if self.LastPrice is None:
            self.LastPrice=price
        else:
            # 當價格大於上一筆價格
            if price>self.LastPrice:
                self.BP+=qty
            # 小於上一筆價格
            elif price<self.LastPrice:
                self.SP+=qty
            self.LastPrice=price
    def Get(self):
        return [self.BP,self.SP]
        
# 計算大戶指標         
class BigOrder():
    def __init__(self , num):
        # 定義幾筆以上是大單
        self.BigFlag=num
        # 買賣方累計大單
        self.B=0
        self.S=0
        # 買賣最後筆數紀錄
        self.BC=0
        self.SC=0
        # 買賣方單筆大單
        self.OnceB=0
        self.OnceS=0
    def Add(self, qty, bc, sc):
        # 判斷口數是否大於
        if qty > self.BigFlag :
            BuyCntDiff = bc-self.BC
            SellCntDiff = sc-self.SC
            # 如果買方筆數新增一筆 ，並小於賣方
            if BuyCntDiff < SellCntDiff and BuyCntDiff == 1:
                self.B+=qty
                self.OnceB=qty
                self.OnceS=0
            # 如果賣方筆數新增一筆 ，並小於買方
            elif BuyCntDiff > SellCntDiff and SellCntDiff == 1:
                self.S+=qty
                self.OnceB=0
                self.OnceS=qty
        self.BC=bc
        self.SC=sc
    def Get(self):
        return [ self.OnceB , self.OnceS , self.B ,self.S ]
        
        
# 計算委託簿固定時間變動         
class CommissionDiff():
    def __init__(self , date , cycle):
        # 買筆 買口 賣筆 賣口
        self.DataList = [[ datetime.datetime.strptime( date+'084500','%Y%m%d%H%M%S'),0,0,0,0 ]]
        self.Cycle = datetime.timedelta(minutes=cycle)
    def Add(self,time,BC,BO,SC,SO):
        # 確認是否為第一筆
        self.DataList.append([ time,BC,BO,SC,SO ])
        # 若不是超過特定時間的資料則移除
        while self.DataList[-1][0] > self.DataList[0][0]+self.Cycle:
            self.DataList=self.DataList[1:]
    # 取得下單差額
    def GetOrderDiff(self):
        BODiff=self.DataList[-1][2]-self.DataList[0][2]
        SODiff=self.DataList[-1][4]-self.DataList[0][4]
        return [ BODiff , SODiff ]
        
# 逐筆 計算累計成交量
class AccVol():
    def __init__(self , date , cycle):
        self.DataList = [[ datetime.datetime.strptime( date+'084500','%Y%m%d%H%M%S'),0 ]]
        self.Cycle = datetime.timedelta(minutes=cycle)
    # 取得累計成交量
    def Get(self):
        volume=self.DataList[-1][1] - self.DataList[0][1]
        return volume
    # 將目前總量進行計算
    def Add(self , Time , Amount ):
        self.DataList.append([Time , Amount])
        # 特定時間以前的資料進行移除
        while self.DataList[-1][0] > self.DataList[0][0]+self.Cycle:
            self.DataList=self.DataList[1:]
            
        


