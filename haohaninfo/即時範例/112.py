# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')
#取得下單函數，詳情請查看技巧103
execfile('order.py')

#定義趨勢判斷時間
trendTime1=datetime.datetime.strptime('08:50:00.00',"%H:%M:%S.%f")
trendTime2=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trendTime3=datetime.datetime.strptime('09:03:00.00',"%H:%M:%S.%f")
trendNum=0
trend=0

#設定指標變數
MAarray=[]
MAnum=10
lastHMTime=""
lastMAValue=0
lastPrice=0

#設定初始倉位，若為0則為無在倉部位
index=0
orderTime=0
orderPrice=0
coverTime=0
coverPrice=0

#判斷趨勢
for i in getOrder():    
 OrderInfo=i.split(',')
 OrderTime=datetime.datetime.strptime(OrderInfo[0],"%H:%M:%S.%f")
 OrderBCnt=int(OrderInfo[1])
 OrderBAmount=float(OrderInfo[2])
 OrderSCnt=int(OrderInfo[3])
 OrderSAmount=float(OrderInfo[4])

 #趨勢判斷1
 if OrderTime>=trendTime1 and trendNum==0:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:   
   trend-=1 
  trendNum+=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt

 #趨勢判斷2
 if OrderTime>=trendTime2 and trendNum==1:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:   
   trend-=1
  trendNum+=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt

 #趨勢判斷3
 if OrderTime>=trendTime3 and trendNum==2:
  if OrderBAmount/OrderBCnt > OrderSAmount/OrderSCnt:
   trend+=1
  elif OrderBAmount/OrderBCnt < OrderSAmount/OrderSCnt:   
   trend-=1
  print OrderInfo[0],"B",OrderBAmount/OrderBCnt,"S",OrderSAmount/OrderSCnt
  break 


#進場判斷
for i in getMatch():		
 MatchInfo=i.split(',')
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])

 #計算MA
 if len(MAarray)==0:
  MAarray+=[MatchPrice]
  lastHMTime=HMTime
 else:
  if HMTime==lastHMTime:
   MAarray[-1]=MatchPrice
  elif HMTime!=lastHMTime:
   if len(MAarray)<MAnum:
    MAarray+=[MatchPrice]
   elif len(MAarray)==MAnum:
   	MAarray=MAarray[1:]+[MatchPrice]
   lastHMTime=HMTime
 
 #當MA計算完成後，開始判斷進場
 if len(MAarray)==MAnum :
  MAValue=float(sum(MAarray))/len(MAarray)
  if lastMAValue==0 and lastPrice==0:
   lastMAValue=MAValue
   lastPrice=MatchPrice
   continue
  print "Price",MatchPrice,"MA",MAValue 
  #多方進場判斷
  if trend>=1:
   #當價格向上突破MA
   if MatchPrice>MAValue and lastPrice<=lastMAValue:
    index=1
    orderInfo=OrderMKT('TX00','B','1')
    orderTime=orderInfo[6]
    orderPrice=int(orderInfo[4])
    print orderTime,"Order Buy Success! Price:",orderPrice
    break
  #空方進場判斷  
  elif trend<=-1:
   #當價格向下突破MA
   if MatchPrice<MAValue and lastPrice>=lastMAValue:
    index=1
    orderInfo=OrderMKT('TX00','S','1')
    orderTime=orderInfo[6]
    orderPrice=int(orderInfo[4])
    print orderTime,"Order Sell Success! Price:",orderPrice
    break
  lastMAValue=MAValue
  lastPrice=MatchPrice 

#出場判斷
for i in getMatch():    
 MatchInfo=i.split(',')
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])

 #計算MA
 if len(MAarray)==0:
  MAarray+=[MatchPrice]
  lastHMTime=HMTime
 else:
  if HMTime==lastHMTime:
   MAarray[-1]=MatchPrice
  elif HMTime!=lastHMTime:
   if len(MAarray)<MAnum:
    MAarray+=[MatchPrice]
   elif len(MAarray)==MAnum:
    MAarray=MAarray[1:]+[MatchPrice]
   lastHMTime=HMTime
 
 #MA計算後出場判斷
 if len(MAarray)==MAnum :
  MAValue=float(sum(MAarray))/len(MAarray)
  if lastMAValue==0 and lastPrice==0:
   lastMAValue=MAValue
   lastPrice=MatchPrice
   continue
  print "Price",MatchPrice,"MA",MAValue 
  #當價格向下穿越MA則出場
  if index==1:
   if MatchPrice<MAValue and lastPrice>=lastMAValue:
    index=0
    coverInfo=OrderMKT('TX00','S','1')
    coverTime=coverInfo[6]
    coverPrice=int(coverInfo[4])
    print coverTime,"Order Sell Success! Price:",coverPrice
    break
  #當價格向上穿越MA則出場
  elif index==-1:
   if MatchPrice>MAValue and lastPrice<=lastMAValue:
    index=0
    coverInfo=OrderMKT('TX00','B','1')
    coverTime=coverInfo[6]
    coverPrice=int(coverInfo[4])
    print coverTime,"Order Buy Success! Price:",coverPrice
    break
  lastMAValue=MAValue
  lastPrice=MatchPrice 

   