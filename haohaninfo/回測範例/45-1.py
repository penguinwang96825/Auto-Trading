# -*- coding: UTF-8 -*-
#取I020，依照逗點分隔，並將分隔符號去除
I020 = [ line.strip('\n').split(",") for line in open('Futures_20170815_I020.csv')][1:]

#起始時間至結束時間
I020a= [ line for line in I020 if int(line[0])>9000000 and int(line[0])<11000000]


OrderTime=I020a[0][0]  #下單時間紀錄
OrderPrice=int(I020a[0][4]) #下單價格紀錄

CoverTime=I020a[-1][0]  #平倉時間紀錄
CoverPrice=int(I020a[-1][4])  #平倉時間紀錄

print "Buy OrderTime:",OrderTime," OrderPrice:",OrderPrice,
print " CoverTime:",CoverTime," CoverPrice:",CoverPrice," Profit:",CoverPrice-OrderPrice