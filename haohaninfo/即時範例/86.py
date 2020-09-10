# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#設定指標變數
lastBcnt=0
lastScnt=0
accB=0
accS=0

#設定初始倉位，若為0則為無在倉部位
index=0
orderPrice=0

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
    if MatchQty>=30 and accB>accS:
     index=1 
     orderPrice=MatchPrice
     print MatchInfo[0],"Order Buy Success!"
     break
   elif diffScnt==1 and diffBcnt>1:
    accS+=MatchQty
    print MatchInfo[0],MatchPrice,0,MatchQty,accB,accS
    if MatchQty>=30 and accS>accS:
     index=-1 
     orderPrice=MatchPrice
     print MatchInfo[0],"Order Sell Success!"
     break
 
 lastBcnt=MatchBcnt
 lastScnt=MatchScnt
   
#接著以下為出場條件判斷，本章不做介紹