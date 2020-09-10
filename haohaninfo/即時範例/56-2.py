# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
OutDesk=0
InDesk=0

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  MatchTime=MatchInfo[0]
  MatchPrcie=int(MatchInfo[1])
  #取得上下五檔價資訊
  UpDn5Info=getLastUpDn5()
  Dn1Price=int(UpDn5Info[1])
  Up1Price=int(UpDn5Info[11])
  
  #進行內外盤判斷
  if MatchPrcie>=Up1Price:
   OutDesk+=1
  if MatchPrcie<=Dn1Price:
   InDesk+=1

  print MatchTime,"OutDesk",OutDesk,"InDesk",InDesk
