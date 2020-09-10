# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
TickMA200=[]
TickOHLC=[]

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=MatchInfo[0]
 MatchPrice=int(MatchInfo[1])
 
 #將Tick相加
 TickMA200+=[MatchPrice]
 
 #當tick200筆時，進行開高低收統計
 if len(TickMA200)==200:
  TickOHLC+=[[MatchTime,TickMA200[0],max(TickMA200),min(TickMA200),TickMA200[-1]]]
  TickMA200=[]
  print TickOHLC[-1]