# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
Qty=[]
lastHMTime=""
lastAmount=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
  MatchAmount=int(MatchInfo[3])
  
  if lastAmount==0:
   lastAmount=MatchAmount
   lastHMTime=HMTime
  if HMTime==lastHMTime:
   Qty=MatchAmount-lastAmount
  else:
   Qty=0
   lastAmount=MatchAmount
   lastHMTime=HMTime 
  
  #出場判斷
  if Qty>=1000:
   if index==1:
    index=0
    print MatchInfo[0],"Order Sell Success!"
    break 
   if index==-1:
    index=0
    print MatchInfo[0],"Order Buy Success!"
    break

  print Qty