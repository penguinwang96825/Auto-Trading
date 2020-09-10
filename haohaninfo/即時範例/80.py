# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#設定指標變數
MAarray=[]
MAnum=10
lastHMTime=""
lastMAValue=0
lastPrice=0

#設定趨勢
trend=1

#設定初始倉位，若為0則為無在倉部位
index=0
orderPrice=0


#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
 MatchPrice=int(MatchInfo[1])

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
 
 if len(MAarray)==MAnum :
  MAValue=float(sum(MAarray))/len(MAarray)
  if lastMAValue==0 and lastPrice==0:
   lastMAValue=MAValue
   lastPrice=MatchPrice
   continue
  print "Price",MatchPrice,"MA",MAValue 
  if trend==1:
   if MatchPrice>MAValue and lastPrice<=lastMAValue:
    index=1
    orderPrice=MatchPrice
    print MatchInfo[0],"Order Buy Success!"
    break
  elif trend==-1:
   if MatchPrice<MAValue and lastPrice>=lastMAValue:
    index=-1
    orderPrice=MatchPrice
    print MatchInfo[0],"Order Sell Success!"
    break
  lastMAValue=MAValue
  lastPrice=MatchPrice 

#接著以下為出場條件判斷，本章不做介紹

   