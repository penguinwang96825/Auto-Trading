# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
OHLC=[]

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  #定義HHMM的時間字串，方便進行分鐘轉換判斷
  HMTime=MatchInfo[0][0:2]+MatchInfo[0][3:5]
  MatchPrice=int(MatchInfo[1])
  #若OHLC為空，先填值
  if len(OHLC)==0:
   OHLC.append([HMTime,MatchPrice,MatchPrice,MatchPrice,MatchPrice])	
  else:
   #進行該分鐘是否結束	
   if HMTime==OHLC[-1][0]:
    #進行高、低價判斷
    if MatchPrice>OHLC[-1][2]:
     OHLC[-1][2]=MatchPrice
    if MatchPrice<OHLC[-1][3]:
     OHLC[-1][3]=MatchPrice
    OHLC[-1][4]=MatchPrice
   else:
   #該分鐘結束則加入新行
    OHLC.append([HMTime,MatchPrice,MatchPrice,MatchPrice,MatchPrice])
  #顯示當前開高低收
  print OHLC[-1]
