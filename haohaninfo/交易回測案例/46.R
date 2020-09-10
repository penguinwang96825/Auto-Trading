I020 <- read.csv('Futures_20170815_I020.csv')

# 選擇必要欄位
A01 <- I020[c(1,5,6)]
names(A01) <- c("INFO_TIME","PRICE","QTY") 

# 選擇趨勢時段
A02 <- subset(A01, INFO_TIME>=as.numeric(08450000) & INFO_TIME<=as.numeric(09000000)) 
MaxPrice <- max(A02$PRICE)
MinPrice <- min(A02$PRICE)
Spread <- MaxPrice - MinPrice 

# 起始及出場時段
A03 <- subset(A01, INFO_TIME>as.numeric(09000000) & INFO_TIME<=as.numeric(10000000)) 

Index<-0

# 開始進行回測
for(i in 1:nrow(A03)){
 #判斷進倉
 if(Index==0 & A03[i,]$PRICE>MaxPrice+Spread*as.numeric(0.2)){
  Index=1 
  OrderTime <- A03[i,]$INFO_TIME
  OrderPrice <- A03[i,]$PRICE   
  #cat(Time0,"BUY",OrderPrice,"StopPoint",StopPoint,"\n")
 }else if (Index==0 & A03[i,]$PRICE<MinPrice-Spread*as.numeric(0.2)){
  Index=-1
  OrderTime <- A03[i,]$INFO_TIME
  OrderPrice <- A03[i,]$PRICE   
  #cat(Time0,"SELL",OrderPrice,"StopPoint",StopPoint,"\n")
 }
 # 判斷平倉
 if(Index==1){
  if((A03[i,]$PRICE > OrderPrice+20 || A03[i,]$PRICE < OrderPrice-10)){
   CoveryTime <- A03[i,]$INFO_TIME
   CoveryPrice <- A03[i,]$PRICE
   cat("BUY TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",CoveryPrice-OrderPrice,'\n') 
   break
  }else if(i==nrow(A03)){
   CoveryTime <- A03[i,]$INFO_TIME
   CoveryPrice <- A03[i,]$PRICE
   cat("BUY TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",CoveryPrice-OrderPrice,'\n')  
  }
 }else if(Index==-1){
  if((A03[i,]$PRICE < OrderPrice-20 || A03[i,]$PRICE > OrderPrice+10)){
   CoveryTime <- A03[i,]$INFO_TIME
   CoveryPrice <- A03[i,]$PRICE
   cat("SELL TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",OrderPrice-CoveryPrice,'\n')
   break
  }else if(i==nrow(A03)){
   CoveryTime <- A03[i,]$INFO_TIME
   CoveryPrice <- A03[i,]$PRICE
   cat("SELL TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",OrderPrice-CoveryPrice,'\n')
  }
 }  
}

