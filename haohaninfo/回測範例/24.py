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
MA = []
MAValue = 0
STime = TimetoNumber('08450000')
Cycle = 6000
MAlen = 10

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
 MAValue=float(sum(MAarray))/len(MAarray)
 MA.extend([[time,MAValue]])
 print time,MAValue

