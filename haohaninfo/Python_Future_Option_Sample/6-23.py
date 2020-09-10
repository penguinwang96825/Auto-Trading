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

# 計算 Pivot Point
PP=(DailyHigh+DailyLow+DailyClose)/3
R3=DailyHigh+(2*(PP-DailyLow))
R2=PP+DailyHigh-DailyLow
R1=(PP*2)-DailyLow
S1=(PP*2)-DailyHigh
S2=PP-DailyHigh+DailyLow
S3=DailyLow+(2*(DailyHigh-PP))

print(DailyTime,'R3',R3,'R2',R2,'R1',R1,'PP',PP,'S1',S1,'S2',S2,'S1',S1,sep='\n')
