# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
lastBcnt=0
lastScnt=0
accB=0
accS=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=MatchInfo[0]
 MatchPrice=int(MatchInfo[1])
 MatchQty=int(MatchInfo[2])
 MatchBcnt=int(MatchInfo[4])
 MatchScnt=int(MatchInfo[5])
 
 #儲存上一筆最新總筆數 
 if lastBcnt==0 and lastScnt==0:
  lastBcnt=MatchBcnt
  lastScnt=MatchScnt
 else:
  #計算相差筆數	
  diffBcnt=MatchBcnt-lastBcnt
  diffScnt=MatchScnt-lastScnt
  #進行數量判斷
  if MatchQty>=10:
   #進行買賣方判斷
   if diffBcnt==1 and diffScnt>1:
    accB+=MatchQty
    print MatchTime,MatchPrice,MatchQty,0,accB,accS
   elif diffScnt==1 and diffBcnt>1:
    accS+=MatchQty
    print MatchTime,MatchPrice,0,MatchQty,accB,accS

 lastBcnt=MatchBcnt
 lastScnt=MatchScnt