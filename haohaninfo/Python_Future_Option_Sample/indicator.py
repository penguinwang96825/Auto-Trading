# 載入必要套件
import requests,datetime,os
from bs4 import BeautifulSoup 
import numpy as np
import matplotlib.dates as mdates
from talib.abstract import *  # 載入技術指標函數


# 取得歷史資料         
def GetHistoryData(DataPath,Broker,Date,Product,Table):
    filename=DataPath+'/'+Broker+'/'+Date+'/'+Product+'_'+Table+'.txt'
    Data=[ i.strip('\n').split(',') for i in open(filename) ]
    return Data

# 取得一段期間的歷史資料
def GetHistoryDataByPeriod(DataPath,Broker,Product,Table,Start,End):
    FilePath=DataPath+'/'+Broker+'/'
    # 找出在資料夾中的日期
    Dates=[ day for day in os.listdir(FilePath) if day.isdigit()==True and day>=Start and day<=End ]
    Dates.sort()
    # 定義要回傳的List
    Data=[]
    # 透過迴圈將每天的檔案都放進該迴圈中
    for Date in Dates:
        filename=DataPath+'/'+Broker+'/'+Date+'/'+Product+'_'+Table+'.txt'
        Data.extend([ i.strip('\n').split(',') for i in open(filename)])
    return Data

# 取得N日期貨行情表
def getFutureDailyInfo(product,n):
    
    # 定義要去資料的日期
    cdate=datetime.datetime.now()
    data_num=0
    
    # 獨立的將每天的近月商品日夜盤資料取出
    tmpdaydata=[]
    tmpnightdata=[]
    
    # 當資料尚未足夠則繼續執行迴圈
    while data_num<n:
        
        # 取得當天字串
        date=cdate.strftime('%Y/%m/%d')
        
        # 首先取得夜盤資料 再取得日盤資料
        for daynight in ['1','0']:
        
            # 取得網頁資料
            html=requests.post('https://www.taifex.com.tw/cht/3/futDailyMarketReport',data={ 
                    'queryType': '2' ,
                    'marketCode': daynight , 
                    'commodity_id': product ,
                    'queryDate': date ,
                    'MarketCode': daynight ,
                    'commodity_idt': product
                    })
            
            # 將網頁資料解析
            soup=BeautifulSoup(html.text,'html.parser')
            # 取得該網頁的行情表格
            table=soup.find('table', class_='table_f')
            # 判斷是否有資料才進行資料讀取
            if table != None:
                tmplist=[]
                # 將每行獨立取出
                for tr in table.find_all('tr'):
                    tmplist1 = []
                    # 將每個欄位取出
                    for td in tr.findChildren(recursive=False):
                        tmpobj=td.get_text()
                        tmpobj=''.join(tmpobj.split())
                        tmplist1.append(tmpobj)
                    # 判斷是否為資料
                    if tmplist1[3].isdigit() :
                        tmplist.append([date]+tmplist1)
                # 若有資料則填入
                if len(tmplist) > 0:
                    # 夜盤資料
                    if daynight == '1':
                        tmpnightdata.append(tmplist[0])
                        data_num+=1
                    # 日盤資料
                    elif daynight == '0' and tmplist[0][10].isdigit():
                        tmpdaydata.append(tmplist[0])
            else:
                print(date,'當天尚無資料')
            
        # 將日期減去一天
        cdate -= datetime.timedelta(1)
    
    # 將日夜盤的K棒整合
    tmpdata=[]
    # 以夜盤資料為主
    for row in tmpnightdata:
        # 取得夜盤開高低收
        nightopen,nighthigh,nightlow,nightclose=float(row[3]),float(row[4]),float(row[5]),float(row[6])
        # 取得日盤資料
        tmpdaydata1=[ i for i in tmpdaydata if i[0] == row[0] ]
        # 如果日盤有資料 就將兩邊資料整合
        if tmpdaydata1 != []:
            tmpdaydata1=tmpdaydata1[0]
            # 取得日盤的
            dayopen,dayhigh,daylow,dayclose=float(tmpdaydata1[3]),float(tmpdaydata1[4]),float(tmpdaydata1[5]),float(tmpdaydata1[6])
            # 判斷日夜盤高低點位
            if dayhigh > nighthigh: 
                nighthigh = dayhigh
            if daylow > nightlow:
                nightlow = daylow
            tmpdata.append([row[0],row[1],row[2],nightopen,nighthigh,nightlow,dayclose])
        # 如果日盤無資料
        else:
            tmpdata.append([row[0],row[1],row[2],nightopen,nighthigh,nightlow,nightclose])
    # 回傳資料
    return tmpdata

# 取得N日期貨三大法人未平倉
def getFutureContractInfo(product,n):
    
    # 定義要去資料的日期
    cdate=datetime.datetime.now()
    data_num=0
    
    # 獨立的將每天的近月商品資料取出
    tmpdata=[]
    
    # 當資料尚未足夠則繼續執行迴圈
    while data_num<n:
        
        # 取得當天字串
        date=cdate.strftime('%Y/%m/%d')
        
        # 取得網頁資料
        html=requests.post('https://www.taifex.com.tw/cht/3/futContractsDate',data={ 
                'queryType': '1',
                'doQuery': '1',
                'queryDate': date,
                'commodityId': product,
                'goDay': '',
                'dateaddcnt':'' 
                })
                
        # 將網頁資料解析
        soup=BeautifulSoup(html.text,'html.parser')
        
        # 取得該網頁的行情表格
        table=soup.find('table', class_='table_f')
        
        # 判斷是否有資料才進行資料讀取
        if table != None:
            tmplist=[]
            # 將每行獨立取出
            for tr in table.find_all('tr'):
                # 將每行每個欄位取出
                tmpobj=tr.get_text()
                tmpobj=tmpobj.replace(',','').split()
                tmplist.append(tmpobj)
            # 篩選特定行數、欄位資料
            tmplist=[ [date] + i[-13:]  for i in tmplist ][3:-4]
            # 新增資料
            tmpdata.extend(tmplist)
            # 成功日數+1
            data_num+=1
        else:
            print('當天尚無三大法人資料')
        
        # 將日期減去一天
        cdate -= datetime.timedelta(1)
        
    return tmpdata

# 取得N日選擇權行情資料
def getOptionDailyInfo(product,n,data=[],cdate='',daynight='1'):
    
    # 取資料起始日期
    if cdate=='':
        # 定義要去資料的日期
        cdate=datetime.datetime.now()
        
    # 取得當天字串
    date=cdate.strftime('%Y/%m/%d')
        
    # 取得網頁資料
    html=requests.post('https://www.taifex.com.tw/cht/3/optDailyMarketReport',data={ 
            'queryType': '1',
            'marketCode': daynight,	
            'commodity_id': product,
            'queryDate': date ,	
            'MarketCode': daynight,		
            'commodity_idt': product
            })
    
    # 將網頁資料解析
    soup=BeautifulSoup(html.text,'html.parser')
    
    # 判斷是否有資料才進行資料讀取
    tmplist=[]
    if '查無資料' not in str(soup):
        # 將每行獨立取出
        for tr in soup.find_all('tr'):
            tmpobj=tr.get_text().replace('-','0').split()
            # 判斷是否有未平倉資料 以及相同商品
            if len(tmpobj)>0 and tmpobj[0]==product:
                tmplist.append([date]+tmpobj)  
        if len(tmplist) > 0:
            # 填入夜盤
            if daynight == '1':
                # print(tmplist,1)
                data.extend([ i[:9]+['0','0'] for i in tmplist])
            # 填入日盤
            if daynight == '0':
                for row in tmplist:
                    for index, item in enumerate(data):
                        if data[index][:5] == row[:5]:
                            # 開高低收
                            if float(row[5]) > float(data[index][5]) and float(row[5]) !=0 :
                                data[index][5]=row[5]
                            if float(row[6]) > float(data[index][6]) :
                                data[index][6] = row[6]
                            if float(row[7]) < float(data[index][7]) and float(row[7]) !=0 or float(data[index][7])==0 :
                                data[index][7] = row[7]
                            if float(row[8]) !=0 :
                                data[index][8] = row[8]
                            # 填入成交價、未平倉
                            data[index][9]=row[-2]
                            data[index][10]=row[-1]
                            break    
    else:
        print(date,'當天尚無資料')
        
    # 取完夜盤之後 取得日盤資料
    if daynight == '1':
        return getOptionDailyInfo(product,n,data,cdate,'0')
    # 取得日盤後判斷資料是否足夠 足夠則回傳
    elif daynight == '0':
        datalen=len(set([ i[0] for i in data ]))
        if datalen >= n:
            cdata=data
            return cdata
        else:
            # 將日期減去一天
            cdate -= datetime.timedelta(1)
            return getOptionDailyInfo(product,n,data,cdate,'1')
    
# 取得選擇權Put Call Ratio
def getPutCallRatio(start_day='',end_day=''):
    # 取得網頁資料
    html=requests.post('https://www.taifex.com.tw/cht/3/pcRatio',data={ 
                'queryStartDate': start_day,		
                'queryEndDate': end_day,
            })

    # 將網頁資料解析
    soup=BeautifulSoup(html.text,'html.parser')

    # 取得該網頁的行情表格
    table=soup.find('table', class_='table_a')

    # 判斷是否有資料才進行資料讀取
    if table != None:
        tmplist=[]
        # 將每行獨立取出
        for tr in table.find_all('tr'):
            tmplist1 = []
            # 將每個欄位取出
            for td in tr.findChildren(recursive=False):
                tmpobj=td.get_text().replace(',','')
                tmpobj=''.join(tmpobj.split())
                tmplist1.append(tmpobj)
            tmplist.append(tmplist1)  
        # 顯示資訊
        return tmplist[1:]
    else:
        print('尚無資料')
        return False
    
# 算K棒
class KBar():
    # 設定初始化變數
    def __init__(self,date,cycle = 1):
        # K棒的頻率(分鐘)
        self.TAKBar = {}
        self.TAKBar['time'] = np.array([])
        self.TAKBar['open'] = np.array([])
        self.TAKBar['high'] = np.array([])
        self.TAKBar['low'] = np.array([])
        self.TAKBar['close'] = np.array([])
        self.TAKBar['volume'] = np.array([])
        self.current = datetime.datetime.strptime(date + ' 00:00:00','%Y%m%d %H:%M:%S')
        self.cycle = datetime.timedelta(minutes = cycle)
    # 更新最新報價
    def AddPrice(self,time,price,volume):
        # 同一根K棒
        if time < self.current:
            # 更新收盤價
            self.TAKBar['close'][-1] = price
            # 更新成交量
            self.TAKBar['volume'][-1] += volume  
            # 更新最高價
            self.TAKBar['high'][-1] = max(self.TAKBar['high'][-1],price)
            # 更新最低價
            self.TAKBar['low'][-1] = min(self.TAKBar['low'][-1],price)  
            # 若沒有更新K棒，則回傳0
            return 0
        # 不同根K棒
        else:
            while time >= self.current:
                self.current += self.cycle
            self.TAKBar['time'] = np.append(self.TAKBar['time'],self.current)
            self.TAKBar['open'] = np.append(self.TAKBar['open'],price)
            self.TAKBar['high'] = np.append(self.TAKBar['high'],price)
            self.TAKBar['low'] = np.append(self.TAKBar['low'],price)
            self.TAKBar['close'] = np.append(self.TAKBar['close'],price)
            self.TAKBar['volume'] = np.append(self.TAKBar['volume'],volume)
            # 若有更新K棒，則回傳1
            return 1
    # 取時間
    def GetTime(self):
        return self.TAKBar['time']      
    # 取開盤價
    def GetOpen(self):
        return self.TAKBar['open']
    # 取最高價
    def GetHigh(self):
        return self.TAKBar['high']
    # 取最低價
    def GetLow(self):
        return self.TAKBar['low']
    # 取收盤價
    def GetClose(self):
        return self.TAKBar['close']
    # 取成交量
    def GetVolume(self):
        return self.TAKBar['volume']
    # 取MA值(MA期數)
    def GetMA(self,n,matype):
        return MA(self.TAKBar,n,matype)    
    # 取SMA值(SMA期數)
    def GetSMA(self,n):
        return SMA(self.TAKBar,n)
    # 取WMA值(WMA期數)
    def GetWMA(self,n):
        return WMA(self.TAKBar,n)
    # 取EMA值(EMA期數)
    def GetEMA(self,n):
        return EMA(self.TAKBar,n)    
    # 取MACD值
    def GetMACD(self,fast_P,slow_P,macd_P):
        return MACD(self.TAKBar,fast_P,slow_P,macd_P)
    # 取布林通道值(中線期數)
    def GetBBands(self,n):
        return BBANDS(self.TAKBar,n)
    # 取KD值(RSV期數,K值期數,D值期數)
    def GetKD(self,rsv,k,d):
        return STOCH(self.TAKBar,fastk_period = rsv,slowk_period = k,slowd_period = d)
    # RSI(RSI期數)
    def GetRSI(self,n):
        return RSI(self.TAKBar,n)
    # 取得乖離率
    def GetBIAS(self,tn=10):
        mavalue=MA(self.TAKBar,timeperiod=tn,matype=0)
        return (self.TAKBar['close']-mavalue)/mavalue
    # 取得繪圖的格式(時間開高低收)(應用在回測章節)
    def GetChartTypeData(self):
        return [ [mdates.date2num(self.TAKBar['time'][i]),self.TAKBar['open'][i],self.TAKBar['high'][i],self.TAKBar['low'][i],self.TAKBar['close'][i]] for i in range(len(self.TAKBar['time'])) ]

# 固定量K棒
class VolumeKBar():
    # 設定初始化變數
    def __init__(self,cycle = 500):
        # K棒的頻率(分鐘)
        self.TAKBar = {}
        self.TAKBar['time'] = np.array([])
        self.TAKBar['open'] = np.array([])
        self.TAKBar['high'] = np.array([])
        self.TAKBar['low'] = np.array([])
        self.TAKBar['close'] = np.array([])
        self.Cycle = cycle
        self.Amount = 0
    # 填入即時報價(volume)
    def AddPrice(self,time,price,amount):
        # 如果是第一筆資料
        if self.Amount==0:
            self.TAKBar['time']=np.append(self.TAKBar['time'],time)
            self.TAKBar['open']=np.append(self.TAKBar['open'],price)
            self.TAKBar['high']=np.append(self.TAKBar['high'],price)
            self.TAKBar['low']=np.append(self.TAKBar['low'],price)
            self.TAKBar['close']=np.append(self.TAKBar['close'],price)
            self.Amount=amount
            return 0
        # 換日的情況，成交量變少，一樣換K棒
        elif amount < self.Amount:
            self.TAKBar['time']=np.append(self.TAKBar['time'],time)
            self.TAKBar['open']=np.append(self.TAKBar['open'],price)
            self.TAKBar['high']=np.append(self.TAKBar['high'],price)
            self.TAKBar['low']=np.append(self.TAKBar['low'],price)
            self.TAKBar['close']=np.append(self.TAKBar['close'],price)
            self.Amount=amount
            return 1
        # 確認是否過了特定成交量
        elif amount - self.Amount < self.Cycle:
            self.TAKBar['close'][-1]=price
            if price > self.TAKBar['high'][-1]:
                self.TAKBar['high'][-1] = price
            elif price < self.TAKBar['low'][-1]:
                self.TAKBar['low'][-1] = price
            return 0
        # 達到特定成交量 新增一根K棒
        elif amount - self.Amount > self.Cycle:
            self.TAKBar['time']=np.append(self.TAKBar['time'],time)
            self.TAKBar['open']=np.append(self.TAKBar['open'],price)
            self.TAKBar['high']=np.append(self.TAKBar['high'],price)
            self.TAKBar['low']=np.append(self.TAKBar['low'],price)
            self.TAKBar['close']=np.append(self.TAKBar['close'],price)
            self.Amount=amount
            return 1
        
        
        
    # 取時間
    def GetTime(self):
        return self.TAKBar['time']      
    # 取開盤價
    def GetOpen(self):
        return self.TAKBar['open']
    # 取最高價
    def GetHigh(self):
        return self.TAKBar['high']
    # 取最低價
    def GetLow(self):
        return self.TAKBar['low']
    # 取收盤價
    def GetClose(self):
        return self.TAKBar['close']
        
# 計算委託簿固定時間變動         
class CommissionDiff():
    def __init__(self , cycle):
        # 買筆 買口 賣筆 賣口
        self.DataList = [[ datetime.datetime.strptime( '000000','%H%M%S'),0,0,0,0 ]]
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
    def __init__(self , cycle):
        self.DataList = [[ datetime.datetime.strptime( '000000','%H%M%S'),0 ]]
        self.Cycle = datetime.timedelta(minutes=cycle)
    # 取得累計成交量
    def Get(self):
        volume=self.DataList[-1][1] - self.DataList[0][1]
        priceDiff=self.DataList[-1][2] - self.DataList[0][2]
        return [ volume , priceDiff ]
    # 將目前總量進行計算
    def Add(self , Time , Amount , Price ):
        self.DataList.append([Time , Amount , Price])
        # 特定時間以前的資料進行移除
        while self.DataList[-1][0] > self.DataList[0][0]+self.Cycle:
            self.DataList=self.DataList[1:]
            
