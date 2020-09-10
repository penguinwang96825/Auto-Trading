# 讀取檔案
I020<- read.csv('Futures_20170815_I020.csv')
# 設置資料欄位名稱
colnames(I020)<-c("INFO_TIME","MATCH_TIME","PROD","ITEM","PRICE","QTY","AMOUNT","MATCH_BUY_CNT","MATCH_SELL_CNT")
# 設定日期
Date <- "20170508"
# 取相關欄位
A01 <- I020[c(1,4,5)]
# 選取開倉及平倉時間
A02 <- subset(A01, INFO_TIME>=as.numeric(09000000) & INFO_TIME<=as.numeric(11000000))
# 設定進場時間及價格
OrderTime <- A02[1,]$INFO_TIME
OrderPrice <- A02[1,]$PRICE
# 設定出場時間及價格
CoveryTime <- A02[nrow(A02),]$INFO_TIME
CoveryPrice <- A02[nrow(A02),]$PRICE
# 顯示交易回報
cat("BUY TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",CoveryPrice-OrderPrice,'\n')