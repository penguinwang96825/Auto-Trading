# 載入必要模組
from haohaninfo import GOrder
from chart import ChartKBar_BBANDS
import sys

# 取得回測參數
Excgange=sys.argv[1]
Product=sys.argv[2]
StartDate=sys.argv[3]
EndDate=sys.argv[4]
Klen=sys.argv[5]
BPeriod=int(sys.argv[6])

# 登入帳號密碼(讀者須修正該帳號密碼為自己的，否則無法執行策略)
GOrder.Login('TestAccount','TestPasswd')

# K線物件
KBar=GOrder.GetTAKBar(StartDate,EndDate,Product,Excgange,'0',Klen)

# 繪製K線圖加上MA線圖
ChartKBar_BBANDS(KBar,BPeriod)

