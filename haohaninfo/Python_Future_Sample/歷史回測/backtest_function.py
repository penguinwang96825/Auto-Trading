# 載入相關套件及函數
import datetime
import numpy

def GetI020(filename='TXFL8-I020.csv'):
    Data=open(filename).readlines()
    Data0= [ line.strip('\n').split(',') for line in Data ]
    return Data0
    
def GetI030(filename='TXFL8-I030.csv'):
    Data=open(filename).readlines()
    Data0= [ line.strip('\n').split(',') for line in Data ]
    return Data0
    
def GetDate(data):
    Date = [ line[0] for line in data ]
    return sorted(set(Date))
    
# Tick資料轉分K棒
def ConvertKBar(date,data,n=60):
    # 定義初始時間及K棒頻率
    StartTime = datetime.datetime.strptime(date + ' 08450000','%Y%m%d %H%M%S%f') 
    Cycle = datetime.timedelta(0,n)
    # 定義空的 List 並將每分鐘資料存入
    KBar = []
    for i in data:
        # 時間、價格、成交量
        time = datetime.datetime.strptime(i[0] + ' ' + i[1],'%Y%m%d %H%M%S%f') 
        price = int(i[3])
        qty = int(i[4])
        # 第一筆資料
        if len(KBar) == 0:
            # 新增第一筆
            KBar.append([StartTime,price,price,price,price,qty])
        # 第二筆資料以後
        else:
            # 沒有換分鐘
            if time < StartTime + Cycle:
                # 最高價判斷
                KBar[-1][2]=max(price,KBar[-1][2])
                # 最低價判斷
                KBar[-1][3]=min(price,KBar[-1][3])
                # 收盤價更換
                KBar[-1][4]=price
                # 累計量
                KBar[-1][5]+=qty
            # 穿越指定時間週期 新增一根K棒
            elif time >= StartTime + Cycle:
                while time >= StartTime + Cycle:
                    # 起始時間 + 週期
                    StartTime += Cycle
                # 新增一根新的K棒
                KBar.append([StartTime,price,price,price,price,qty])
    return KBar
    
# 轉換成Ta-lib適用的格式
def ConvertTAKBar(date,data,n=60):
    # 取K棒資料
    KBar = ConvertKBar(date,data,n)
    # 定義新的 TAKBar dictionary
    TAKBar={}
    # 分別取出時間、開、高、低、收、量，並轉換資料型態
    TAKBar['time'] = numpy.array([ i[0] for i in KBar ])
    TAKBar['open'] = numpy.array([ float(i[1]) for i in KBar ])
    TAKBar['high'] = numpy.array([ float(i[2]) for i in KBar ])
    TAKBar['low'] = numpy.array([ float(i[3]) for i in KBar ])
    TAKBar['close'] = numpy.array([ float(i[4]) for i in KBar ])
    TAKBar['volume'] = numpy.array([ float(i[5]) for i in KBar ])
    return TAKBar           
                
                
