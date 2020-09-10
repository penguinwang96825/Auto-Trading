# -*- coding: UTF-8 -*-
#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#起始時間至結束時間
I020a= [ int(line[4]) for line in I020 if int(line[0])<=9000000 ]
I020b= [ line for line in I020 if int(line[0])>9000000 and int(line[0])<11000000 ]

#定義上下界
ceil=max(I020a)
floor=min(I020a)
#倉位為0
index=0

for i in range(len(I020b)):
 price=int(I020b[i][4])
 #進場判斷
 if index==0:
  if price>ceil:
   OrderTime=I020b[i][0]			#新倉時間紀錄
   OrderPrice=price 				#新倉價格紀錄
   index=1
   print "Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice,
  elif price<floor:
   OrderTime=I020b[i][0]			#新倉時間紀錄
   OrderPrice=price 				#新倉價格紀錄
   index=-1
   print "Sell OrderTime:",OrderTime," OrderPrice:",OrderPrice,
  elif i == len(I020b)-1:
   print "No Trade"	
   break
 #出場判斷
 elif index!=0:
  if index==1:
   if OrderPrice+20<=price or OrderPrice-10>=price:
    CoverTime=I020b[i][0]  			#平倉時間紀錄
    CoverPrice=int(I020b[i][4]) 	#平倉時間紀錄
    print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice
    break
   elif i == len(I020b)-1:
    CoverTime=I020b[i][0]  			#平倉時間紀錄
    CoverPrice=int(I020b[i][4])  	#平倉時間紀錄
    print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice
  elif index==-1:
   if price<=OrderPrice-20 or price>=OrderPrice+10:
    CoverTime=I020b[i][0]  			#平倉時間紀錄
    CoverPrice=int(I020b[i][4])  	#平倉時間紀錄
    print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice
    break
   elif i == len(I020b)-1:
    CoverTime=I020b[i][0]  			#平倉時間紀錄
    CoverPrice=int(I020b[i][4])  	#平倉時間紀錄
    print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice

