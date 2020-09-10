# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendTime0=datetime.datetime.strptime('08:45:00.00',"%H:%M:%S.%f")
trendTime1=datetime.datetime.strptime('08:50:00.00',"%H:%M:%S.%f")
trendTime2=datetime.datetime.strptime('08:55:00.00',"%H:%M:%S.%f")
trendTime3=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trendNum=0
trend=0

#定義指標變數
lastBAmount=0
lastSAmount=0

#取得委託資訊
for i in getOrder():		
 OrderInfo=i.split(',')
 OrderTime=datetime.datetime.strptime(OrderInfo[0],"%H:%M:%S.%f")
 OrderBAmount=int(OrderInfo[2])
 OrderSAmount=int(OrderInfo[4])

 if OrderTime>=trendTime0 and lastBAmount==0 and lastSAmount==0:
  lastBAmount=OrderBAmount
  lastSAmount=OrderSAmount

 #趨勢判斷
 if OrderTime>=trendTime1 and trendNum==0:
  diffBAmount=OrderBAmount-lastBAmount
  diffSAmount=OrderSAmount-lastSAmount
  if diffBAmount > diffSAmount:
   trend+=1
  elif diffBAmount < diffSAmount:  	
   trend-=1
  trendNum+=1
  lastBAmount=OrderBAmount
  lastSAmount=OrderSAmount
  print OrderInfo[0],"B",diffBAmount,"S",diffSAmount

 #趨勢判斷
 if OrderTime>=trendTime2 and trendNum==1:
  diffBAmount=OrderBAmount-lastBAmount
  diffSAmount=OrderSAmount-lastSAmount
  if diffBAmount > diffSAmount:
   trend+=1
  elif diffBAmount < diffSAmount:   
   trend-=1
  trendNum+=1
  lastBAmount=OrderBAmount
  lastSAmount=OrderSAmount
  print OrderInfo[0],"B",diffBAmount,"S",diffSAmount

 #趨勢判斷
 if OrderTime>=trendTime2 and trendNum==2:
  diffBAmount=OrderBAmount-lastBAmount
  diffSAmount=OrderSAmount-lastSAmount
  if diffBAmount > diffSAmount:
   trend+=1
  elif diffBAmount < diffSAmount:   
   trend-=1
  print OrderInfo[0],"B",diffBAmount,"S",diffSAmount
  break 

print "Trend",trend