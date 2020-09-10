# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300

#取得委託資訊
for i in getOrder():		
 OrderInfo=i.split(',')
 OrderBCnt=int(OrderInfo[1])
 OrderBAmount=float(OrderInfo[2])
 OrderSCnt=int(OrderInfo[3])
 OrderSAmount=float(OrderInfo[4])
 
 #出場判斷
 if index==1:
  if OrderBAmount/OrderBCnt<OrderSAmount/OrderSCnt:
   index=0
   print MatchInfo[0],"Order Sell Success!"
   break
 elif index==-1:
  if OrderBAmount/OrderBCnt>OrderSAmount/OrderSCnt:
   index=0
   print MatchInfo[0],"Order Buy Success!"
   break