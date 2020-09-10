# -*- coding: utf-8 -*-
import sys,datetime
from indicator import getPutCallRatio

# 取得前30日的Put Call Ratio 
PCRData=getPutCallRatio()
PCR = [ float(i[-1]) for i in PCRData ]
# 取得Put Call Ratio的平均、最後一筆
PCRAver=sum(PCR)/len(PCR)
PCRLast=PCR[-1]

# 如果最後一筆小於平均Put Call Ratio
if PCRLast < PCRAver: 
    print('當前Put Call Ratio偏多方')
# 如果最後一筆大於平均Put Call Ratio
elif PCRLast > PCRAver: 
    print('當前Put Call Ratio偏空方')
