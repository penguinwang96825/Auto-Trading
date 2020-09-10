#取得即時報價，詳細在技巧51
source("function.R")

while(TRUE){

 #取得即時委託資訊
 Odata<-GetOrderData(DataPath,Date)
 OrderTime<- Odata[[1]][1]
 OrderBuyCount <- as.numeric(Odata[[1]][2])
 OrderSellCount <- as.numeric(Odata[[1]][4])
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 print(paste(OrderTime,OrderBuyAmount/OrderBuyCount,OrderSellAmount/OrderSellCount))

}
