# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
stopLoss=10
takeProfit=10

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300
coverPrice=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchPrice=int(MatchInfo[1])
 
 #出場判斷 
 if index==1:
  if MatchPrice>=orderPrice+takeProfit or MatchPrice<=orderPrice-stopLoss:
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Sell Success!"
   break
 elif index==-1:
  if MatchPrice<=orderPrice-takeProfit or MatchPrice>=orderPrice+stopLoss:
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Sell Success!"
   break
 


