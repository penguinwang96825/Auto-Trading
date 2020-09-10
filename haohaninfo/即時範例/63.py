# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
Qty=[]
QMA=0
MAnum=5
lastHMTime=""
lastAmount=0

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  #定義HHMM的時間字串，方便進行分鐘轉換判斷
  HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
  MatchAmount=int(MatchInfo[3])
  
  #進行量MA的計算
  if len(Qty)==0:
   Qty+=[0]
   lastHMTime=HMTime
   lastAmount=MatchAmount
  else:
   if HMTime==lastHMTime:
    Qty[-1]=MatchAmount-lastAmount
   else:
    if len(Qty)==MAnum:
     QMA=sum(Qty)/len(Qty)
     print QMA
     Qty=Qty[1:]+[0]
    else: 
     Qty+=[0]
    lastHMTime=HMTime
    lastAmount=MatchAmount
  #顯示量MA
  print Qty
