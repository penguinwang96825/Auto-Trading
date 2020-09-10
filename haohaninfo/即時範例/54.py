# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#取得成交資訊
for i in getMatch():		
  MatchInfo=i.split(',')
  MatchTime=MatchInfo[0]
  MatchAmount=int(MatchInfo[3])
  MatchBCnt=int(MatchInfo[4])
  MatchSCnt=int(MatchInfo[5])

  #進行平均買賣口計算
  avgB=float(MatchAmount)/MatchBCnt
  avgS=float(MatchAmount)/MatchSCnt
  
  print MatchTime,"avgB",avgB,"avgS",avgS
