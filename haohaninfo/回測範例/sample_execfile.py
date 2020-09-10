import os
import sys
import math
os.chdir('D:\\data')


def TimetoNumber(time):
 time=time.zfill(8)
 sec=int(time[:2])*360000+int(time[2:4])*6000+int(time[4:6])*100+int(time[6:8])
 return sec

def NumbertoTime(sec):
 TOS=str(sec%100).zfill(2)
 TTime=sec/100
 TS=str(TTime%60).zfill(2)
 TTime=TTime/60
 TM=str(TTime%60).zfill(2)
 TTime=TTime/60
 TH=str(TTime%60).zfill(2)
 return TH+TM+TS+TOS

