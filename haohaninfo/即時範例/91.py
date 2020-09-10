# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
MAarray=[]
longMAnum=14
shortMAnum=7
lastHMTime=""
lastShortMAValue=0
lastLongMAValue=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300
coverPrice=0

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
 
 #出場判斷
 if len(MAarray)==longMAnum :
  longMAValue=float(sum(MAarray))/longMAnum
  shortMAValue=float(sum(MAarray[longMAnum-shortMAnum:]))/shortMAnum
  if lastLongMAValue==0 and lastShortMAValue==0:
   lastLongMAValue=longMAValue
   lastShortMAValue=shortMAValue
   continue
  print "ShortMA",shortMAValue,"LongMA",longMAValue 
  if index==1:
   if shortMAValue<lastLongMAValue and lastShortMAValue>=lastLongMAValue:
    index=0
    coverPrice=MatchPrice
    print MatchInfo[0],"Order Sell Success!"
    break
  elif index==-1:
   if shortMAValue>lastLongMAValue and lastShortMAValue<=lastLongMAValue:
    index=0
    coverPrice=MatchPrice
    print MatchInfo[0],"Order Buy Success!"
    break
  lastLongMAValue=longMAValue
  lastShortMAValue=shortMAValue


