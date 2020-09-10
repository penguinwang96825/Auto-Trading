# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendTime=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trend=0

#定義指標變數
OutDesk=0
InDesk=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrcie=int(MatchInfo[1])
 MatchQty=int(MatchInfo[2])
 UpDn5Info=getLastUpDn5()
 Dn1Price=int(UpDn5Info[1])
 Up1Price=int(UpDn5Info[11])

 if MatchPrcie>=Up1Price:
  OutDesk+=MatchQty
 if MatchPrcie<=Dn1Price:
  InDesk+=MatchQty

 #趨勢判斷
 if MatchTime >= trendTime:
  if OutDesk>InDesk:
   trend+=1
  elif OutDesk<InDesk:
   trend-=1 
  break
 
 print MatchInfo[0],"OutDesk",OutDesk,"InDesk",InDesk

print "Trend",trend