# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
lastBcnt=0
lastScnt=0
accB=0
accS=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300
coverPrice=0

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
 
 #出場判斷
 if index==1:
  if accB<accS:
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Sell Success!"
   break 
 elif index==-1: 
  if accB>accS:
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Buy Success!"
   break 

 lastBcnt=MatchBcnt
 lastScnt=MatchScnt
