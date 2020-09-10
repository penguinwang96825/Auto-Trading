# -*- coding: UTF-8 -*-
# 載入相關套件
import talib
import numpy
import datetime
            
# K線指標class
# 參數 週期
class KBar():
    def __init__(self, date, cycle=1):
        self.Cycle=datetime.timedelta(minutes=cycle)
        self.Time=datetime.datetime.strptime( date+'090000','%Y%m%d%H%M%S' )-(self.Cycle*2)
        self.Open=numpy.array([])
        self.High=numpy.array([])
        self.Low=numpy.array([])
        self.Close=numpy.array([])
        self.Volume=numpy.array([])
    # 填入即時報價
    def Add(self,time,price,qty):
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

# 透過當前成交價 與上一筆成交價 相比計算內外盤         
class BSPower1():
    def __init__(self):
        self.BP=0
        self.SP=0
        self.LastPrice=None
    def Add(self,price,qty):
        if self.LastPrice is None:
            self.LastPrice=price
        else:
            if price>self.LastPrice:
                self.BP+=qty
            elif price<self.LastPrice:
                self.SP+=qty
            self.LastPrice=price
    def Get(self):
        return [self.BP,self.SP]
        
# 透過當前成交價 與上下一檔價 相比計算內外盤
class BSPower2():
    def __init__(self):
        self.BP=0
        self.SP=0
    def Add(self,price,qty,ask,bid):
            if price>=bid:
                self.BP+=qty
            elif price<=ask:
                self.SP+=qty
    def Get(self):
        return [self.BP,self.SP]        
        
        

