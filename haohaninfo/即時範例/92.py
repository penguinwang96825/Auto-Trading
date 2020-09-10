# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
lastBAmount=0
lastSAmount=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300

#取得委託資訊
for i in getOrder():		
 OrderInfo=i.split(',')
 OrderBAmount=int(OrderInfo[2])
 OrderSAmount=int(OrderInfo[4])

 if lastBAmount==0 and lastSAmount==0:
  lastBAmount=OrderBAmount
  lastSAmount=OrderSAmount

 diffBAmount=OrderBAmount-lastBAmount
 diffSAmount=OrderSAmount-lastSAmount

 #抽單出場判斷
 if index==1:
  if diffBAmount <= -100:
   index=0
   print MatchInfo[0],"Order Sell Success!"
   break
 elif index==-1:
  if diffSAmount <= -100:
   index=0
   print MatchInfo[0],"Order Buy Success!"
   break