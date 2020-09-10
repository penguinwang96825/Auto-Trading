# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#設定指標變數
MAarray=[]
longMAnum=14
shortMAnum=7
lastHMTime=""
lastShortMAValue=0
lastLongMAValue=0
crossTime=0
interval=300

#設定趨勢
trend=1

#設定初始倉位，若為0則為無在倉部位
index=0
orderPrice=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])

 if len(MAarray)==0:
  MAarray+=[MatchPrice]
  lastHMTime=HMTime
 else:
  if HMTime==lastHMTime:
   MAarray[-1]=MatchPrice
  elif HMTime!=lastHMTime:
   if len(MAarray)<longMAnum:
    MAarray+=[MatchPrice]
   elif len(MAarray)==longMAnum:
   	MAarray=MAarray[1:]+[MatchPrice]
   lastHMTime=HMTime
 
 if len(MAarray)==longMAnum :
  longMAValue=float(sum(MAarray))/longMAnum
  shortMAValue=float(sum(MAarray[longMAnum-shortMAnum:]))/shortMAnum
  if lastLongMAValue==0 and lastShortMAValue==0:
   lastLongMAValue=longMAValue
   lastShortMAValue=shortMAValue
   continue
  print "ShortMA",shortMAValue,"LongMA",longMAValue 
  if trend==1:
   if shortMAValue>lastLongMAValue and lastShortMAValue<=lastLongMAValue:
    if crossTime==0:
     crossTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
     print "Cross",MatchInfo[0]
    elif datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f") > crossTime+datetime.timedelta(0,interval):
     index=1
     orderPrice=MatchPrice
     print MatchInfo[0],"Order Buy Success!"
     break
  elif trend==-1:
   if shortMAValue<lastLongMAValue and lastShortMAValue>=lastLongMAValue:
    if crossTime==0:
     crossTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
     print "Cross",MatchInfo[0]    
    elif datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f") > crossTime+datetime.timedelta(0,interval):
     index=-1
     orderPrice=MatchPrice
     print MatchInfo[0],"Order Sell Success!"
     break
  lastLongMAValue=longMAValue
  lastShortMAValue=shortMAValue
  
#接著以下為出場條件判斷，本章不做介紹

   