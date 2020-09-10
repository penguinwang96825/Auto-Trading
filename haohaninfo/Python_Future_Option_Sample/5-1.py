# 匯入模組
from indicator import GetHistoryDataByPeriod,KBar
import datetime,sys  

# 指定日期
DataPath=sys.argv[1]    # 'C:/Data'
Broker=sys.argv[2]      # 'simulator'
Product=sys.argv[3]     # 'TXFI9' 
Start=sys.argv[4]       # '20190830'
End=sys.argv[5]         # '20190911'

# 定義1分K棒的物件
MinuteKBar=KBar(Start,1)

for row in GetHistoryDataByPeriod(DataPath,Broker,Product,'Match',Start,End):
    Time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    Price = float(row[2])
    Volume = int(row[4])
    # 餵資料進K棒物件
    ChangeFlag = MinuteKBar.AddPrice(time,price,volume)
    # 接下來策略會寫在下方
    # ...
    # 如果 ChangeFlag 變數為1，則代表換新K棒
    # if ChangeFlag == 1:
    # 取用加權移動平均線方式
    # MinuteKBar.GetWMA(15)

