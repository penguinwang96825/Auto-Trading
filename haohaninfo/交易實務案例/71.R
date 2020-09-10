#取得即時報價，詳細在技巧51
source("function.R")

#三個判斷區段，設定四個判斷時間點
trendTime0 <- strptime('08:45:00.00','%H:%M:%OS')
trendTime1 <- strptime('08:50:00.00','%H:%M:%OS')
trendTime2 <- strptime('08:55:00.00','%H:%M:%OS')
trendTime3 <- strptime('09:00:00.00','%H:%M:%OS')
#紀錄每上個時間點的總量
lastBuyAmount <- 0
lastSellAmount <- 0
#用變數作為趨勢初始值
trend <- 0
#用另一個變數來記錄目前的趨勢判斷進度，避免重複判斷
trendnum <- 0

while(TRUE){

 Odata<-GetOrderData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 OrderTime <- strptime(Odata[[1]][1],'%H:%M:%OS')
 OrderBuyAmount <- as.numeric(Odata[[1]][3])
 OrderSellAmount <- as.numeric(Odata[[1]][5])

 #進行第一次的總量紀錄
 if ( OrderTime > trendTime0 & lastBuyAmount == 0){
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }

 #第一次判斷委託變動量
 if( OrderTime > trendTime1 & trendnum == 0 ){
  #計算8:45至8:50委託總量差異
  diffBuyAmount <- OrderBuyAmount - lastBuyAmount
  diffSellAmount <- OrderSellAmount - lastSellAmount

  if( diffBuyAmount > diffSellAmount ){
   trend <- trend + 1
  }else if( diffBuyAmount < diffSellAmount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }

 #第二次判斷委託變動量
 if( OrderTime > trendTime2 & trendnum == 1 ){
  #計算8:50至8:55委託總量差異 
  diffBuyAmount <- OrderBuyAmount - lastBuyAmount
  diffSellAmount <- OrderSellAmount - lastSellAmount

  if( diffBuyAmount > diffSellAmount ){
   trend <- trend + 1
  }else if( diffBuyAmount < diffSellAmount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }

 #第三次判斷委託變動量
 if( OrderTime > trendTime3 & trendnum == 2 ){
  #計算8:55至9:00委託總量差異
  diffBuyAmount <- OrderBuyAmount - lastBuyAmount
  diffSellAmount <- OrderSellAmount - lastSellAmount

  if( diffBuyAmount > diffSellAmount ){
   trend <- trend + 1
  }else if( diffBuyAmount < diffSellAmount ){
   trend <- trend - 1
  }
  trendnum <- trendnum +1
  lastBuyAmount <- OrderBuyAmount
  lastSellAmount <- OrderSellAmount
 }


 #判斷完成後，顯示預測趨勢
 #若trend大於0，則看多；小於0，則看空
 if( trendnum == 3 ){
  print(trend)
 }

}
