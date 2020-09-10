#取得即時報價，詳細在技巧51
source("function.R")

#設定三個判斷時間點
trendTime1 <- strptime('08:50:00.00','%H:%M:%OS')
trendTime2 <- strptime('09:00:00.00','%H:%M:%OS')
trendTime3 <- strptime('09:03:00.00','%H:%M:%OS')
#用變數作為趨勢初始值
trend <- 0
#用另一個變數來記錄目前的趨勢判斷進度，避免重複判斷
trendnum <- 0

while(TRUE){

 Odata<-GetOrderData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 OrderTime <- strptime(Odata[[1]][1],'%H:%M:%OS')
 OrderBuyCount <- as.numeric(Odata[[1]][2])
 OrderSellCount <- as.numeric(Odata[[1]][4])
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 #第一次判斷委託比重
 if( OrderTime > trendTime1 & trendnum == 0 ){
  if( OrderBuyAmount/OrderBuyCount > OrderSellAmount/OrderSellCount ){
   trend <- trend + 1
  }else if( OrderBuyAmount/OrderBuyCount < OrderSellAmount/OrderSellCount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
 }

 #第二次判斷委託比重
 if( OrderTime > trendTime2 & trendnum == 1 ){
  if( OrderBuyAmount/OrderBuyCount > OrderSellAmount/OrderSellCount ){
   trend <- trend + 1
  }else if( OrderBuyAmount/OrderBuyCount < OrderSellAmount/OrderSellCount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
 }

 #第三次判斷委託比重
 if( OrderTime > trendTime3 & trendnum == 2 ){
  if( OrderBuyAmount/OrderBuyCount > OrderSellAmount/OrderSellCount ){
   trend <- trend + 1
  }else if( OrderBuyAmount/OrderBuyCount < OrderSellAmount/OrderSellCount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
 }

 #判斷完成後，顯示預測趨勢
 if( trendnum ==3 ){
  print(trend)
 }

}
