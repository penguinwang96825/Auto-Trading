# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#定義指標變數
OutDesk=0
InDesk=0

#假設目前倉位為買方，進場部分請參考第七章
index=1
orderPrice=10300
coverPrice=0

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
 
 #出場判斷
 if index==1:
  if InDesk>OutDesk:
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Sell Success!"
   break
 elif index==-1:
  if InDesk<OutDesk: 
   index=0
   coverPrice=MatchPrice
   print MatchInfo[0],"Order Buy Success!"
   break
 
 print MatchInfo[0],"OutDesk",OutDesk,"InDesk",InDesk


