# -*- coding: utf-8 -*-
import sys
from indicator import getFutureDailyInfo,getFutureContractInfo

# 取得最前一日的行情資料
LastDailyInfo=getFutureDailyInfo('MTX',1)
OnOpenInterest=sum([ int(i[13]) for i in LastDailyInfo ])

# 取得最前三日的法人資料
LastContractInfo=getFutureContractInfo('MXF',1)
LegalBuyOnOpenInterest=sum([ int(i[8]) for i in LastContractInfo ])
LegalSellOnOpenInterest=sum([ int(i[10]) for i in LastContractInfo ])

# 計算散戶的多空剩餘留倉部位
IndividualBuy=OnOpenInterest-LegalBuyOnOpenInterest
IndividualSell=OnOpenInterest-LegalSellOnOpenInterest

# 將散戶的多空剩餘留倉部位相除，取得散戶多空比例
IndividualRatio=IndividualBuy/IndividualSell

# 若散戶留多單則市場趨勢看跌
if IndividualRatio > 1:
    print('散戶看多，市場看跌')
# 若散戶留空單則市場趨勢看漲
elif IndividualRatio < 1:
    print('散戶看多，市場看跌')

