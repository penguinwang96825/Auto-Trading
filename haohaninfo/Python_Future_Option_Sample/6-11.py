# -*- coding: utf-8 -*-

import sys
from indicator import getOptionDailyInfo

# 定義契約、取得日期
product=sys.argv[1]
info_num=int(sys.argv[2])

print(getOptionDailyInfo(product,info_num))
