# 導入資料主體
I020<- read.csv('Futures_20170815_I020.csv')
colnames(I020)<-c("INFO_TIME","MATCH_TIME","PROD","ITEM","PRICE","QTY","AMOUNT","MATCH_BUY_CNT","MATCH_SELL_CNT")
# 設置日期
Date <- "20170815"
# 取相關欄位
A01 <- I020[c(1,4,5)]
# 選取開倉及平倉時間
A02 <- subset(A01, INFO_TIME>=as.numeric(08450000) & INFO_TIME<=as.numeric(13300000))
# 設定進場時間及價格
OrderTime <- A02[1,]$INFO_TIME
OrderPrice <- A02[1,]$PRICE
# 設定出場時間及價格
CoveryTime <- A02[nrow(A02),]$INFO_TIME
CoveryPrice <- A02[nrow(A02),]$PRICE
cat("TXF",Date,OrderTime,OrderPrice,"B",Date,CoveryTime,CoveryPrice,'\n')