# -*- coding: UTF-8 -*-
#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#定義變數初始值
high=int(I020[0][4])
low=int(I020[0][4])

#開始計算高低點
for i in I020[1:]:
 price = int(i[4])
 if price > high:
  high=price
 if price < low:
  low=price
 print "Time:",i[0]," Price:",price," High:",high," Low:",low