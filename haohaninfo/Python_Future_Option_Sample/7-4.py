# -*- coding: utf-8 -*-
import sys,haohaninfo 
from indicator import getFutureDailyInfo,getOptionDailyInfo

# 定義契約(需要輸入期交所查詢行情的商品名稱)
WebProductFuture=sys.argv[1]
WebProductOption=sys.argv[2]

# 取得最前一日的行情資料、近月商品
LastFutureDailyInfo=getFutureDailyInfo(WebProductFuture,1)[0]
LastFuturePrice=float(LastFutureDailyInfo[6])

# 台指選擇權100點一跳
ExcutePriceGap=100
# 取得選擇權價內一檔履約價
CallExcutePrice=LastFuturePrice-(LastFuturePrice%100)
PutExcutePrice=CallExcutePrice+ExcutePriceGap
# 取得選擇權行情資料
LastOptionDailyInfo=getOptionDailyInfo(WebProductOption,2)
# 取得價內一檔的選擇權
LastCall=[ i for i in LastOptionDailyInfo if float(i[3])==CallExcutePrice and i[4]=='Call' ]
LastCall=sorted(LastCall,key=lambda x: x[2])[:2]
LastPut=[ i for i in LastOptionDailyInfo if float(i[3])==PutExcutePrice and i[4]=='Put' ]
LastPut=sorted(LastPut,key=lambda x: x[2])[:2]

# 判斷買權成交量上升、未平倉量上升
if float(LastCall[0][-2]) > float(LastCall[1][-2]) and float(LastCall[0][-1]) > float(LastCall[1][-1]):
    print('買權成交量上升、未平倉量上升，看漲')

# 判斷賣權成交量上升、未平倉量上升
if float(LastPut[0][-2]) > float(LastPut[1][-2]) and float(LastPut[0][-1]) > float(LastPut[1][-1]):
    print('買權成交量上升、未平倉量上升，看跌')






