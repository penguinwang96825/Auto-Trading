# -*- coding: utf-8 -*-
import sys,haohaninfo
from indicator import getFutureContractInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProduct=sys.argv[1]

# 取得最前三日的法人資料
LastDailyInfo=getFutureContractInfo(WebProduct,3)
# 取得未平倉數量欄位 自營商、投信、外資
LastDailyInfo1=[ float(i[12]) for i in LastDailyInfo if i[1]=='外資' ]

# 判斷法人連三買
if LastDailyInfo1[0] > LastDailyInfo1[1] > LastDailyInfo1[2]:
    print('法人連三日買進部位')
# 判斷法人連三賣
elif LastDailyInfo1[0] < LastDailyInfo1[1] < LastDailyInfo1[2] :
    print('法人連三日賣出部位')
# 除此之外，動作不一致
else:
    print('法人三天動作不一致')
    

