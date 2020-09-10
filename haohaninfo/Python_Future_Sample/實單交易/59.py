# -*- coding: UTF-8 -*-
# 載入相關套件
import function,datetime,sys

# 取得當天日期
Date = datetime.datetime.now().strftime("%Y%m%d")
# 交易商品名稱
Prod = sys.argv[1]

# 取逐筆成交資訊
for i in function.getMatch(Prod):
    print(i)
    
# 取得逐筆委託資訊
# for i in function.getOrder(Prod):
    # print(i)
    
# 取得上下五檔價量資訊
# for i in function.getUpDn5(Prod):
    # print(i)
    
    