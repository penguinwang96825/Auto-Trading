# -*- coding: UTF-8 -*-
#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#定義變數初始值
lastPrice=int(I020[0][4])
outDesk=0
inDesk=0

#開始計算內外盤
for i in I020[1:]:
 price = int(i[4])
 qty = int(i[5])
 if price > lastPrice:
  outDesk+=qty
 if price < lastPrice:
  inDesk+=qty
 print "Time:",i[0]," Price:",price," OutDesk:",outDesk," InDesk:",inDesk
 lastPrice = price