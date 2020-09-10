# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendTime=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trend=0

#定義指標變數
lastBcnt=0
lastScnt=0
accB=0
accS=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])
 MatchQty=int(MatchInfo[2])
 MatchBcnt=int(MatchInfo[4])
 MatchScnt=int(MatchInfo[5])
  
 if lastBcnt==0 and lastScnt==0:
  lastBcnt=MatchBcnt
  lastScnt=MatchScnt
 else:
  diffBcnt=MatchBcnt-lastBcnt
  diffScnt=MatchScnt-lastScnt
  if MatchQty>=10:
   if diffBcnt==1 and diffScnt>1:
    accB+=MatchQty
    print MatchInfo[0],MatchPrice,MatchQty,0,accB,accS
   elif diffScnt==1 and diffBcnt>1:
    accS+=MatchQty
    print MatchInfo[0],MatchPrice,0,MatchQty,accB,accS
 
 #趨勢判斷
 if MatchTime>=trendTime:
  if accB>accS:
   trend+=1 
  elif accB<accS:
   trend-=1 
  break

 lastBcnt=MatchBcnt
 lastScnt=MatchScnt

print "Trend",trend

