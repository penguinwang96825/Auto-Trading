# -*- coding: utf-8 -*-

import sys
from indicator import getOptionDailyInfo

# 定義契約、取得日期
product=sys.argv[1]
target=sys.argv[2]

# 取得最近兩天的選擇權日資料
data=getOptionDailyInfo(product,2)

# 依照指定契約篩選資料
target_data=[ i for i in data if i[2]==target ]

# 將買權賣權分別計算
tmplist=[]
for tp in ['Call','Put']:
    type_data=[ i for i in target_data if i[4]==tp]
    # 依照履約價分別計算
    exercise_prices=sorted(set([ i[3] for i in type_data ]))
    for exercise_price in exercise_prices:
        ep_data=[ i for i in type_data if i[3] == exercise_price] 
        if len(ep_data) != 2:
            continue
        tmplist.append([ep_data[0][0],
                        ep_data[0][1],
                        ep_data[0][2],
                        ep_data[0][3],
                        ep_data[0][4],
                        float(ep_data[0][8])-float(ep_data[1][8]),
                        ep_data[0][-2],
                        ep_data[1][-2],
                        int(ep_data[0][-2])-int(ep_data[1][-2]),
                        ep_data[0][-1],
                        ep_data[1][-1],
                        int(ep_data[0][-1])-int(ep_data[1][-1])           
                        ])

tmplist.sort(key = lambda x: int(x[3]))
print(*tmplist, sep = "\n")