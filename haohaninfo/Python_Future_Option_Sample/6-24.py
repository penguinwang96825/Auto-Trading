# -*- coding: utf-8 -*-
import sys
from indicator import getFutureDailyInfo

# 定義契約、取得日期
product=sys.argv[1]
info_num=1

# 取得期貨行情資料
DailyInfo=getFutureDailyInfo(product,1)[0]
DailyTime=DailyInfo[0]
DailyHigh=float(DailyInfo[4])
DailyLow=float(DailyInfo[5])
DailyClose=float(DailyInfo[6])

# 計算 CDP
CDP=(DailyHigh+DailyLow+DailyClose)/3
AH=CDP+DailyHigh-DailyLow
NH=2*CDP-DailyLow
NL=2*CDP-DailyHigh
AL=CDP-DailyHigh+DailyLow

print(DailyTime,'AH',AH,'NH',NH,'CDP',CDP,'NL',NL,'AL',AL,sep='\n')
