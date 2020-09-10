# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
Qty=[]
lastAmount=0

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  #定義HHMM的時間字串，方便進行分鐘轉換判斷
  HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
  MatchAmount=int(MatchInfo[3])
  #進行每分鐘價格計算
  if len(Qty)==0:
   Qty.append([HMTime,0])
   lastAmount=MatchAmount
  else:
   if HMTime==Qty[-1][0]:
    Qty[-1][1]=MatchAmount-lastAmount
   else:
    Qty.append([HMTime,0])
    lastAmount=MatchAmount
 
  print Qty
