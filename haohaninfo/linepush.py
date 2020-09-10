# -*- coding: UTF-8 -*-
#載入相關套件
import lineTool

token="XXX"

def linePush(msg):
    lineTool.lineNotify(token, msg)

import time 
for i in range(10):
    linePush('測試排程-'+str(i))
    time.sleep(1)
    print(i)