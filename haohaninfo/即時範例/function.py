# -*- coding: UTF-8 -*-
#載入相關套件
import time
import datetime
import tailer

#取得當天日期
Date=time.strftime("%Y%m%d")
#設定檔案位置
DataPath="D:/data/"

#開啟這三個檔案
MatchFile=open(DataPath+Date+'_Match.txt')
OrderFile=open(DataPath+Date+'_Commission.txt')
UpDn5File=open(DataPath+Date+'_UpDn5.txt')

#持續取得成交資訊
def getMatch():
 return tailer.follow(MatchFile,0)

#持續取得委託資訊
def getOrder():
 return tailer.follow(OrderFile,0)

#持續取得上下五檔價資訊
def getUpDn5():
 return tailer.follow(UpDn5File,0)

#取得最新一筆成交資訊
def getLastMatch():
 return tailer.tail(MatchFile,3)[-2].split(",")

#取得最新一筆委託資訊
def getLastOrder():
 return tailer.tail(OrderFile,3)[-2].split(",")

#取得最新一筆上下五檔價資訊
def getLastUpDn5():
 return tailer.tail(UpDn5File,3)[-2].split(",")

