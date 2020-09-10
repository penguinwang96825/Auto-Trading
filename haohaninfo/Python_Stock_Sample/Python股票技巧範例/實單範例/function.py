# -*- coding: UTF-8 -*-
# 載入相關套件
import tailer
from urllib.request import urlopen
import json,time,datetime

# 設定券商名稱
# BrokerID="capital" 、 "yuanta" 、 "kgi"

# 持續取得指定股票代碼的成交資訊
def getSIDMatch(Date,sid,BrokerID="capital",DataPath="C:/Data/"):
    for i in tailer.follow(open(DataPath+BrokerID+'/'+Date+'/'+sid+'_Match.txt'),0):
        j=i.strip('\n').split(',')
        yield j

# 取得指定股票代碼的最新一筆成交資訊
def getLastSIDMatch(Date,sid,BrokerID="capital",DataPath="C:/Data/"):
    tmpfiledata=open(DataPath+BrokerID+'/'+Date+'/'+sid+'_Match.txt').readlines()
    tmpfiledata.reverse()
    for i in tmpfiledata:
        j=i.strip('\n').split(',')
        return j

# 取得當月的日K
def getDayKBar(sid,date):
    # 透過API取得資料
    html=urlopen('http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date='+date+'&stockNo='+sid)
    content=html.read().decode('utf-8')
    jcontent=json.loads(content)
    data=jcontent['data']
    # 將資料整理成可用的資訊
    data=[ [i[0],float(i[3].replace(',','')),float(i[4].replace(',','')),float(i[5].replace(',','')),float(i[6].replace(',','')),float(i[8].replace(',',''))] for i in data]
    return data

# 取得往前推算n日的日K
def getDayKBarbyNum(sid,daynum):
    tmpday=datetime.datetime.now().strftime("%Y%m%d")
    # 首先取得當月資料
    dayK=getDayKBar(sid,tmpday)
    # 若資料數量不足，則更往前補足資料
    while len(dayK)<daynum:
        tmpday=(datetime.datetime.strptime((tmpday[:6]+'01'),'%Y%m%d') - datetime.timedelta(days=1)).strftime("%Y%m%d")
        tmpdata=getDayKBar(sid,tmpday)
        dayK=tmpdata+dayK
        time.sleep(3)
    # 回傳指定天數的日K
    return dayK[-daynum:]
        

