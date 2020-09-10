# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
MAarray=[]
MAnum=10
lastHMTime=""

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 #定義HHMM的時間字串，方便進行分鐘轉換判斷
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])

 #進行MA的計算
 if len(MAarray)==0:
  MAarray+=[MatchPrice]
  lastHMTime=HMTime
 else:
  if HMTime==lastHMTime:
   MAarray[-1]=MatchPrice
  elif HMTime!=lastHMTime:
   if len(MAarray)<MAnum:
    MAarray+=[MatchPrice]
   elif len(MAarray)==MAnum:
   	MAarray=MAarray[1:]+[MatchPrice]
   lastHMTime=HMTime

 print HMTime,"MAvalue",float(sum(MAarray))/len(MAarray)
