# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
closePrice=[]
lastHMTime=""

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 #定義HHMM的時間字串，方便進行分鐘轉換判斷
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])
 
 #進行每分鐘收盤價計算
 if len(closePrice)==0:
  closePrice+=[MatchPrice]
  lastHMTime=HMTime
 else:
  if HMTime==lastHMTime:
   closePrice[-1]= MatchPrice
  elif HMTime!=lastHMTime:
   closePrice+=[MatchPrice]
   lastHMTime=HMTime
 
 #顯示當前價
 print "current Price:",closePrice[-1]