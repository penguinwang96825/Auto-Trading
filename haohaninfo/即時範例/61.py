# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

#取得上下五檔價量資訊
for i in getUpDn5():		
 UpDn5Info=i.split(',')
 UpDn5Time=UpDn5Info[0]
 totalUpPrice=0
 totalUpQty=0
 totalDnPrice=0
 totalDnQty=0
 
 #開始進行上下五檔加權平均值
 for j in range(0,5):
  totalDnPrice+=int(UpDn5Info[1+2*j])*int(UpDn5Info[2+2*j])
  totalDnQty+=int(UpDn5Info[2+2*j])
  totalUpPrice+=int(UpDn5Info[11+2*j])*int(UpDn5Info[12+2*j])
  totalUpQty+=int(UpDn5Info[12+2*j])
 
 print UpDn5Time,"avgUpPrice",float(totalUpPrice)/totalUpQty,"avgDnPrice",float(totalDnPrice)/totalDnQty  



