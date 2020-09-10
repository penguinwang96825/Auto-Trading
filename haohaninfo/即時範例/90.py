# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
MAarray=[]
MAnum=10
lastHMTime=""
lastMAValue=0
lastPrice=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300
coverPrice=0

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
 
 #出場判斷
 if len(MAarray)==MAnum :
  MAValue=float(sum(MAarray))/len(MAarray)
  if lastMAValue==0 and lastPrice==0:
   lastMAValue=MAValue
   lastPrice=MatchPrice
   continue
  print "Price",MatchPrice,"MA",MAValue 
  if index==1:
   if MatchPrice<MAValue and lastPrice>=lastMAValue:
    index=0
    coverPrice=MatchPrice
    print MatchInfo[0],"Order Sell Success!"
    break
  elif index==-1:
   if MatchPrice>MAValue and lastPrice<=lastMAValue:
    index=0
    coverPrice=MatchPrice
    print MatchInfo[0],"Order Buy Success!"
    break
  lastMAValue=MAValue
  lastPrice=MatchPrice 



   