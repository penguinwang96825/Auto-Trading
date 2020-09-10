# -*- coding: utf-8 -*-

import sys
from indicator import getOptionDailyInfo

# 定義契約、取得日期
product=sys.argv[1]
target=sys.argv[2]

data=getOptionDailyInfo(product,1)
call=[ i for i in data if i[2]==target and i[4]=='Call']
put=[ i for i in data if i[2]==target and i[4]=='Put']
call.sort(key = lambda x: int(x[-1]))
put.sort(key = lambda x: int(x[-1]))
print('壓力：',call[-1][3],'支撐：',put[-1][3])