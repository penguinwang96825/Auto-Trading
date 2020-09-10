# -*- coding: UTF-8 -*-

#載入相關套件及函數
import matplotlib.pyplot as plt

#取得成交資訊
log = [ line.strip('\n').split(",") for line in open('profit.log')]

profit=0
profitList=[]
for i in log:
 if i[5]=="B":
  profit+=int(i[9])-int(i[4])
 if i[5]=="S":
  profit+=int(i[4])-int(i[9])
 profitList+=[profit]

# print profitList

#定義圖表物件
ax = plt.figure(1) 		#第一張圖片              
ax = plt.subplot(111)	#該張圖片僅一個圖案
#以上兩行，可簡寫如下一行
#fig,ax = plt.subplots()

#定義title
plt.title('Profit Line')
plt.xlabel('Time')
plt.ylabel('Profit')

#繪製圖案
#plot_date(X軸物件, Y軸物件, 線風格)
ax.plot(profitList, 'k-')

#顯示繪製圖表
plt.show()