# -*- coding: UTF-8 -*-
#載入相關套件
import time,datetime,tailer

#選定券商
Broker='masterlink_future'
#取得當天日期
Date=time.strftime("%Y%m%d")
#設定檔案位置
DataPath="C:/Data/"+Broker+'/'+Date+'/'


#持續取得成交資訊
def getMatch(prod):
    MatchFile=open(DataPath+prod+'_Match.txt')
    for line in tailer.follow(MatchFile,0):
        yield line.split(',')

#持續取得委託資訊
def getOrder(prod):
    OrderFile=open(DataPath+prod+'_Commission.txt')
    for line in tailer.follow(OrderFile,0):
        yield line.split(',')

#持續取得上下五檔價資訊
def getUpDn5(prod):
    UpDn5File=open(DataPath+prod+'_UpDn5.txt')
    for line in tailer.follow(UpDn5File,0):
        yield line.split(',')

#取得最新一筆成交資訊
def getLastMatch(prod):
    MatchFile=open(DataPath+prod+'_Match.txt')
    return tailer.tail(MatchFile,3)[-2].split(",")

#取得最新一筆委託資訊
def getLastOrder(prod):
    OrderFile=open(DataPath+prod+'_Commission.txt')
    return tailer.tail(OrderFile,3)[-2].split(",")

#取得最新一筆上下五檔價資訊
def getLastUpDn5(prod):
    UpDn5File=open(DataPath+prod+'_UpDn5.txt')
    return tailer.tail(UpDn5File,3)[-2].split(",")
