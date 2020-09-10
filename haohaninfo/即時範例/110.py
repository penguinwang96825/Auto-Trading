# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')
#取得下單函數，詳情請查看技巧103
execfile('order.py')

#設定開始時間及結束時間
startTime=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
endTime=datetime.datetime.strptime('10:00:00.00',"%H:%M:%S.%f")

#設定初始倉位，若為0則為無在倉部位
index=0
orderTime=0
orderPrice=0
coverTime=0
coverPrice=0
#定義指標變數
stopLoss=10
takeProfit=10


#進場判斷
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])
 #時間到則進場
 if MatchTime>=startTime:
  index=1
  orderInfo=OrderMKT('TX00','B','1')
  orderTime=orderInfo[6]
  orderPrice=int(orderInfo[4])
  print orderTime,"Order Buy Success! Price:",orderPrice
  break

#出場判斷 
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])
 
 if index==1:
  #停損停利判斷
  if MatchPrice>=orderPrice+takeProfit or MatchPrice<=orderPrice-stopLoss:
   index=0
   coverInfo=OrderMKT('TX00','S','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Sell Success! Price:",coverPrice
   break
  #時間到則出場
  if MatchTime>=endTime:
   index=0
   coverInfo=OrderMKT('TX00','S','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Sell Success! Price:",coverPrice
   break 

