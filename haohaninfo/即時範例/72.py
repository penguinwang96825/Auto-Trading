# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendTime=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trend=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchAmount=float(MatchInfo[3])
 MatchBcnt=int(MatchInfo[4])
 MatchScnt=int(MatchInfo[5])

 #趨勢判斷
 if MatchTime>=trendTime:
  if MatchAmount/MatchBcnt>MatchAmount/MatchScnt:
   trend+=1
  elif MatchAmount/MatchBcnt<MatchAmount/MatchScnt:
   trend-=1 
  print MatchInfo[0],"B",MatchAmount/MatchBcnt,"S",MatchAmount/MatchScnt
  break


print "Trend",trend