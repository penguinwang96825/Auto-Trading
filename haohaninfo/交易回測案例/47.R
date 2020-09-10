
# 取得分鐘數的函數
getMin <- function(time){
 min <- round(as.numeric(substr(time,nchar(time)-5,nchar(time)))/10000,0)
 return(min)
}

# 載入成交資訊
I020 <- read.csv('Futures_20170815_I020.csv')

A01 <- I020[c(1,5,6)]
names(A01) <- c("INFO_TIME","PRICE","QTY") 
 
# 起始及出場時段
A03 <- subset(A01, INFO_TIME<=as.numeric(13300000)) 

# 初始狀態
Index<-0
MAarray <- numeric(0)
MA <- 0 
lastMA <-0

# 開始進行策略回測
for(i in 2:nrow(A03)){
 
 if(Index==0){
  #動態計算MA
  if(length(MAarray)==0){
   MAarray <- c(A03[i,]$PRICE,MAarray)
  }else if(getMin(A03[i,]$INFO_TIME)==getMin(A03[i-1,]$INFO_TIME)){
   MAarray[1] <- A03[i,]$PRICE
  }else{
   MAarray <- c(A03[i,]$PRICE,MAarray)
   if(length(MAarray)>10){
    MAarray <- MAarray[-11]
   }
  }

  #若尚未滿10 分鐘，則不進行進場判斷
  if(length(MAarray)<10){
   next
  }else if (lastMA==0){
   lastMA = round(sum(MAarray)/10,3)
   next
  }else { 
   MA <- round(sum(MAarray)/10,3)
  }
  #進場判斷
  if(A03[i,]$PRICE>MA && A03[i-1,]$PRICE<lastMA){
    Index=1 
    OrderTime <- A03[i,]$INFO_TIME
        OrderPrice <- A03[i,]$PRICE   
   #cat(Time0,"BUY",OrderPrice,"StopPoint",StopPoint,"\n")
   }else if (A03[i,]$PRICE<MA && A03[i-1,]$PRICE>lastMA){
    Index=-1
    OrderTime <- A03[i,]$INFO_TIME
        OrderPrice <- A03[i,]$PRICE   
       #cat(Time0,"SELL",OrderPrice,"StopPoint",StopPoint,"\n")
   }
   lastMA=MA
  }
  #出場判斷
  if(Index==1){
   if((A03[i,]$PRICE > OrderPrice+5 || A03[i,]$PRICE < OrderPrice-3)){
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
   if((A03[i,]$PRICE < OrderPrice-5 || A03[i,]$PRICE > OrderPrice+3)){
                Time1 <- A03[i,]$INFO_TIME
                CoveryPrice <- A03[i,]$PRICE
    cat("SELL TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",OrderPrice-CoveryPrice,'\n')
    break
         }else if(i==nrow(A03)){
                Time1 <- A03[i,]$INFO_TIME
                CoveryPrice <- A03[i,]$PRICE
    cat("SELL TIME:",OrderTime,"PRICE:",OrderPrice,"COVERY TIME:",CoveryTime,"C_PRICE:",CoveryPrice,"PROFIT",OrderPrice-CoveryPrice,'\n')
   }
  }  
 }

