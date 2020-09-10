# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')
#取得下單函數，詳情請查看技巧103
execfile('order.py')

#設定上下界
trendEndTime=datetime.datetime.strptime("09:00:00.00","%H:%M:%S.%f")
highPoint=0
lowPoint=0
spread=0
#進出場時間限制
orderLimitTime=datetime.datetime.strptime("10:00:00.00","%H:%M:%S.%f")
coverLimitTime=datetime.datetime.strptime("12:00:00.00","%H:%M:%S.%f")

#設定初始倉位，若為0則為無在倉部位
index=0
orderTime=0
orderPrice=0
coverTime=0
coverPrice=0
#定義指標變數
stopLoss=10
takeProfit=20
maxProfit=0
fallBack=0.75

#取得高低點
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchHigh=int(MatchInfo[6])
 MatchLow=int(MatchInfo[7])
 if MatchTime>=trendEndTime:
  highPoint=MatchHigh
  lowPoint=MatchLow
  spread=highPoint-lowPoint
  break

#顯示上下界，突破則順勢入場
print "HighPoint",highPoint,"LowPoint",lowPoint,"Spread",spread

#進場判斷
for i in getMatch():    
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])
 #順勢做多
 if MatchPrice>highPoint+spread:
  index=1
  orderInfo=OrderMKT('TX00','B','1')
  orderTime=orderInfo[6]
  orderPrice=int(orderInfo[4])
  print orderTime,"Order Buy Success! Price:",orderPrice
  break
 #順勢放空
 elif MatchPrice<lowPoint-spread:
  index=-1
  orderInfo=OrderMKT('TX00','S','1')
  orderTime=orderInfo[6]
  orderPrice=int(orderInfo[4])
  print orderTime,"Order Sell Success! Price:",orderPrice
  break
 #若到10點尚未進場則當日不交易
 if MatchTime>orderLimitTime:
  print "No Order"
  sys.exit(0)

#出場判斷
for i in getMatch():    
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])
 if index==1:
  #記錄最高點，進行停利出場判斷
  currentProfit=MatchPrice-orderPrice
  if currentProfit>=max(takeProfit,maxProfit):
   maxProfit=currentProfit
  if maxProfit>0 and maxProfit*fallBack>currentProfit:
   index=0
   coverInfo=OrderMKT('TX00','S','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Sell Success! Price:",coverPrice
   break
  #停損出場
  if currentProfit<(stopLoss*-1):
   index=0
   coverInfo=OrderMKT('TX00','S','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Sell Success! Price:",coverPrice
   break  
  #到達結束時間，自動出場 
  if MatchTime>coverLimitTime:
   index=0
   coverInfo=OrderMKT('TX00','S','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Sell Success! Price:",coverPrice
   break 
 elif index==-1:
  #記錄最高點，進行停利出場判斷
  currentProfit=orderPrice-MatchPrice
  if currentProfit>=max(takeProfit,maxProfit):
   maxProfit=currentProfit
  if maxProfit>0 and maxProfit*fallBack>currentProfit:
   index=0
   coverInfo=OrderMKT('TX00','B','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Buy Success! Price:",coverPrice
   break
  #停損出場
  if currentProfit<(stopLoss*-1):
   index=0
   coverInfo=OrderMKT('TX00','B','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Buy Success! Price:",coverPrice
   break
  #到達結束時間，自動出場 
  if MatchTime>coverLimitTime:
   index=0
   coverInfo=OrderMKT('TX00','B','1')
   coverTime=coverInfo[6]
   coverPrice=int(coverInfo[4])
   print coverTime,"Order Buy Success! Price:",coverPrice
   break
 
 
  
