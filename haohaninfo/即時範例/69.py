# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義判斷時間
trendStartTime=datetime.datetime.strptime('08:45:00.00',"%H:%M:%S.%f")
trendStartPrice=0
trendEndTime=datetime.datetime.strptime('09:00:00.00',"%H:%M:%S.%f")
trendEndPrice=0
trend=0

#取得成交資訊
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrcie=int(MatchInfo[1])
 #判斷趨勢開始結尾的成交價格
 if trendStartPrice==0 and MatchTime>trendStartTime:
  trendStartPrice=MatchPrcie
 elif trendEndPrice==0 and MatchTime>trendEndTime:
  trendEndPrice=MatchPrcie
  if trendEndPrice>trendStartPrice:
   trend+=1
  elif trendEndPrice<trendStartPrice: 
   trend-=1
  break

print "TrendStartPrice",trendStartPrice,"TrendEndPrice",trendEndPrice,"Trend:",trend

  