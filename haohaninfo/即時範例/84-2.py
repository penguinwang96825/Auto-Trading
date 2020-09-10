# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#設定指標變數
trendEndTime=datetime.datetime.strptime("09:00:00.00","%H:%M:%S.%f")
highPoint=0
lowPoint=999999999

#設定初始倉位，若為0則為無在倉部位
index=0
orderPrice=0

#取得高低點
for i in getMatch():		
 MatchInfo=i.split(',')
 MatchTime=datetime.datetime.strptime(MatchInfo[0],"%H:%M:%S.%f")
 MatchPrice=int(MatchInfo[1])

 if MatchPrice>highPoint:
  highPoint=MatchPrice
 if MatchPrice<lowPoint:
  lowPoint=MatcMatchPricehLow
  
 if MatchTime>=trendEndTime:
  break	

print "HighPoint",highPoint,"LowPoint",lowPoint

#進場判斷
for i in getMatch():    
 MatchInfo=i.split(',')
 MatchPrice=int(MatchInfo[1])

 if MatchPrice>highPoint:
  index=1
  orderPrice=MatchPrice
  print MatchInfo[0],"Order Buy Success!"
  break
 elif MatchPrice<lowPoint:
  index=-1
  orderPrice=MatchPrice
  print MatchInfo[0],"Order Sell Success!"
  break

#接著以下為出場條件判斷，本章不做介紹

   