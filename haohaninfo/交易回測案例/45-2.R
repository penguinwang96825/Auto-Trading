# 讀取檔案
I020<- read.csv('Futures_20170815_I020.csv')
# 設置資料欄位名稱
colnames(I020)<-c("INFO_TIME","MATCH_TIME","PROD","ITEM","PRICE","QTY","AMOUNT","MATCH_BUY_CNT","MATCH_SELL_CNT")
# 設定日期
Date <- "20170508"
# 取相關欄位
A01 <- I020[c(1,4,5)]
A02 <- subset(A01, INFO_TIME>=as.numeric(09000000) & INFO_TIME<=as.numeric(11000000))
# 選取開倉及平倉時間
OrderTime <- A02[1,]$INFO_TIME
OrderPrice <- A02[1,]$PRICE
# 透過迴圈偵測停損
for( i in 1:nrow(A02)){
 #停損出場
 if(A02[i,]$PRICE <= OrderPrice-10){
  CoveryTime <- A02[i,]$INFO_TIME
  CoveryPrice <- A02[i,]$PRICE
  break
 #到期出場
 }else if(i == nrow(A02)){
  CoveryTime <- A02[nrow(A02),]$INFO_TIME
  CoveryPrice <- A02[nrow(A02),]$PRICE
 }
}
# 顯示交易回報
cat("BUY TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",CoveryPrice-OrderPrice,'\n')