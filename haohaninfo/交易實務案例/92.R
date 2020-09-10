#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1
orderPrice <- 10000

while(index !=0){

 Odata<-GetOrderData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 OrderTime <- strptime(Odata[[1]][1],'%H:%M:%OS')
 OrderBuyCount <- as.numeric(Odata[[1]][2])
 OrderSellCount <- as.numeric(Odata[[1]][4])
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 #判斷委託比重
 if( index == 1 ){
  #反向穿越出場
  if( OrderBuyAmount/OrderBuyCount < OrderSellAmount/OrderSellCount ){
   index <- 0
   print("Cover Buy Success!")
   break
  }
 }else if ( index == (-1) ){
  #反向穿越出場
  if( OrderBuyAmount/OrderBuyCount > OrderSellAmount/OrderSellCount ){
   index <- 0
   print("Cover Sell Success!")
   break
  }
 }
}
