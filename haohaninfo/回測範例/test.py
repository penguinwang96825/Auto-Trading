# -*- coding: UTF-8 -*-

#取得報價資訊，詳情請查看技巧51
execfile('function.py')

for i in getMatch():		

  UpDn5Info=getLastUpDn5()
  print getLastOrder()