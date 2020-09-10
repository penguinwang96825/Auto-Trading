#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1
orderPrice <- 10000

#紀錄每上個時間點的資訊
lastOrderTime <- NA
lastBuyAmount <- 0
lastSellAmount <- 0

while(index !=0){

 Odata<-GetOrderData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 OrderTime <- strptime(Odata[[1]][1],'%H:%M:%OS')
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 #進行第一次的總量紀錄
 if ( is.na(lastOrderTime) ){
  lastOrderTime <- OrderTime
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
  next
 }

 if( OrderTime > lastOrderTime ){
  diffBuyAmount <- OrderBuyAmount - lastBuyAmount
  diffSellAmount <- OrderSellAmount - lastSellAmount

  if (index ==1){
   if(diffBuyAmount < -100){
    index <- 0
    print("Cover Buy Success!")
    break
   }
  }else if(index==(-1)){
   if(diffSellAmount < -100){
    index <- 0
    print("Cover Sell Success!")
    break
   }

  }

  lastOrderTime <- OrderTime
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }

}
