# -*- coding: UTF-8 -*-
#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#起始時間至結束時間
I020a= [ line for line in I020 if int(line[0])>9000000 and int(line[0])<11000000]

#初始倉位
index=0

for i in I020a:
 if index==0:
  if 進場條件:
   OrderTime=i[0]  #下單時間紀錄
   OrderPrice=i[4] #下單價格紀錄

 elif index!=0:
  if 出場條件:
   OrderTime=i[0]  #下單時間紀錄
   OrderPrice=i[4] #下單價格紀錄



