# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendTime1=datetime.datetime.strptime('08:50:00.00',"%H:%M:%S.%f")
trendTime2=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trendTime3=datetime.datetime.strptime('09:03:00.00',"%H:%M:%S.%f")
trendNum=0
trend=0

#取得委託資訊
for i in getOrder():		
 OrderInfo=i.split(',')
 OrderTime=datetime.datetime.strptime(OrderInfo[0],"%H:%M:%S.%f")
 OrderBCnt=int(OrderInfo[1])
 OrderBAmount=float(OrderInfo[2])
 OrderSCnt=int(OrderInfo[3])
 OrderSAmount=float(OrderInfo[4])

 #趨勢判斷
 if OrderTime>=trendTime1 and trendNum==0:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:  	
   trend-=1 
  trendNum+=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt

 #趨勢判斷
 if OrderTime>=trendTime2 and trendNum==1:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:  	
   trend-=1
  trendNum+=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt

 #趨勢判斷
 if OrderTime>=trendTime3 and trendNum==2:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:  	
   trend-=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt
  break 

print "Trend",trend