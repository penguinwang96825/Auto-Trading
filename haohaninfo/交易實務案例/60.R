#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始格式
lastBuyAmount <- 0
lastSellAmount <- 0


while(TRUE){

 #取得即時委託資訊
 Odata<-GetOrderData(DataPath,Date)
 OrderTime<- Odata[[1]][1]
 OrderBuyCount <- as.numeric(Odata[[1]][2])
 OrderSellCount <- as.numeric(Odata[[1]][4])
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 if (lastBuyAmount ==0 & lastSellAmount==0){
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }else{
  diffBuyAmount <- OrderBuyAmount - lastBuyAmount
  diffSellAmount <- OrderSellAmount - lastSellAmount
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
  if(diffBuyAmount!=0 | diffSellAmount!=0){
   print(paste(OrderTime,diffBuyAmount,diffSellAmount))
  }
 }

 
}
