# -*- coding: UTF-8 -*-
#時間轉數值
def TimetoNumber(time):
 time=time.zfill(8)
 sec=int(time[:2])*360000+int(time[2:4])*6000+int(time[4:6])*100+int(time[6:8])
 return sec

#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#定義相關變數
MAarray = []
MAValue = 0
STime = TimetoNumber('08450000')
Cycle = 6000
MAlen = 10
#定義上一筆值，提供給策略判斷
lastMAValue=0
lastPrice=0
#倉位為0
index=0


#開始進行MA計算
for i in I020:
 time=i[0]
 price=int(i[4])
 if len(MAarray)==0:
  MAarray+=[price]
 else:
  if TimetoNumber(time)<STime+Cycle:
   MAarray[-1]=price
  else:
   if len(MAarray)==MAlen:
    MAarray=MAarray[1:]+[price]
   else:
    MAarray+=[price]   
   STime = STime+Cycle
 #到達第10分鐘後，開始進行策略判斷
 if len(MAarray)==MAlen:
  MAValue=float(sum(MAarray))/len(MAarray)
  if lastMAValue==0 or lastPrice==0:
   lastMAValue=MAValue
   lastPrice=price
   continue
  if index==0:
   if MAValue<price and lastMAValue>=lastPrice:
    OrderTime=time		#新倉時間紀錄
    OrderPrice=price 	#新倉價格紀錄
    index=1
    print "Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice,
   elif MAValue> price and lastMAValue<=lastPrice:
    OrderTime=time		#新倉時間紀錄
    OrderPrice=price 	#新倉價格紀錄
    index=-1
    print "Sell OrderTime:",OrderTime," OrderPrice:",OrderPrice,
  elif index!=0:
   if index==1:
    if price>=OrderPrice+10 or price<=OrderPrice-10:
     CoverTime=time			#平倉時間紀錄
     CoverPrice=price 		#平倉時間紀錄
     print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice
     break
    elif i == len(I020)-1:
     CoverTime=time  		#平倉時間紀錄
     CoverPrice=price  		#平倉時間紀錄
     print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice
   if index==-1:
    if price<=OrderPrice-10 or price>=OrderPrice+10:
     CoverTime=time  			#平倉時間紀錄
     CoverPrice=price 			#平倉時間紀錄
     print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice
     break
   elif i == len(I020)-1:
     CoverTime=time  		#平倉時間紀錄
     CoverPrice=price  		#平倉時間紀錄
     print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",OrderPrice-CoverPrice


