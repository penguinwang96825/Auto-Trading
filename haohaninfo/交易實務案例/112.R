#取得即時報價，詳細在技巧51
source("function.R")
source("order.R")

#設定初始倉位，若為0則為無在倉部位
index <- 0

#設定三個判斷時間點
trendTime1 <- strptime('08:50:00.00','%H:%M:%OS')
trendTime2 <- strptime('09:00:00.00','%H:%M:%OS')
trendTime3 <- strptime('09:03:00.00','%H:%M:%OS')
#用變數作為趨勢初始值
trend <- 0
#用另一個變數來記錄目前的趨勢判斷進度，避免重複判斷
trendnum <- 0

#進出場價格定義
orderPrice <- 0
coverPrice <- 0

#設定MA變數初始格式
MAarray <- numeric(0)
MAnum <- 10
lastHMTime <- 0
lastPrice <- 0 
lastMAValue <- 0

while(trendnum < 3){

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
}

print(paste("Trend:",trend))

while(index ==0){
 #取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchPrice <- as.numeric(Mdata[[1]][2])
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))

 #更新MA Array
 if(length(MAarray)==0){
  MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
  lastHMTime <- HMTime
  next
 }else if (HMTime==lastHMTime){
  MAarray[1] <- MatchPrice
 }else if(HMTime>lastHMTime){ 
  MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
  lastHMTime <- HMTime
 }
 #當MA滿足10分鐘的資料時，才進行進場判斷
 if(length(na.omit(MAarray))==MAnum){
  #計算MA值
  MAValue <- round(mean(MAarray),2)
  print(paste(HMTime,MAValue))
  #若沒有前一筆資訊，則無法進行MA穿越判斷
  if (lastMAValue == 0 ){
   lastMAValue <- MAValue
   lastPrice <- MatchPrice
   next
  } 
  #進行判斷，本範例趨勢預設為1，
  if(trend>=1){
   if(lastPrice <= lastMAValue & MatchPrice > MAValue){
    orderInfo <- OrderMKT('TX00','B',1)
    orderPrice <- as.numeric(strsplit(orderInfo,",")[[1]][5])
    index <- 1
    print(paste("Order Buy Success Price:",orderPrice))
    break
   }
  }else if(trend<=(-1)){
   if(lastPrice >= lastMAValue & MatchPrice < MAValue){
    orderInfo <- OrderMKT('TX00','S',1)
    orderPrice <- as.numeric(strsplit(orderInfo,",")[[1]][5])
    index <- (-1)
    print(paste("Order Sell Success Price:",orderPrice))
    break
   }
  }
  #更新最新值
  lastPrice <- MatchPrice
  lastMAValue <- MAValue
 }
}

while(index !=0 ){

 #取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchPrice <- as.numeric(Mdata[[1]][2])
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))

 #更新MA Array
 if(length(MAarray)==0){
  MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
  lastHMTime <- HMTime
  next
 }else if (HMTime==lastHMTime){
  MAarray[1] <- MatchPrice
 }else if(HMTime>lastHMTime){    
  MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
  lastHMTime <- HMTime
 }

 #當MA滿足10分鐘的資料時，才進行進場判斷
 if(length(na.omit(MAarray))==MAnum){
  #計算MA值
  MAValue <- round(mean(MAarray),2)
  print(paste(HMTime,MAValue))
  #若沒有前一筆資訊，則無法進行MA穿越判斷
  if (lastMAValue == 0 ){
   lastMAValue <- MAValue
   lastPrice <- MatchPrice
   next
  } 
  #進行判斷，本範例預設進場買單
  if(index==1){
   if(lastPrice >= lastMAValue & MatchPrice < MAValue){
    coverInfo <- OrderMKT('TX00','S',1)
    coverPrice <- as.numeric(strsplit(coverInfo,",")[[1]][5])
    index <- 0
    print(paste("Cover Buy Success Price:",coverPrice,"Profit:",coverPrice-orderPrice))
    break
   }
  }else if(index==(-1)){
   if(lastPrice <= lastMAValue & MatchPrice > MAValue){
    coverInfo <- OrderMKT('TX00','B',1)
    coverPrice <- as.numeric(strsplit(coverInfo,",")[[1]][5])
    index <- 0
    print(paste("Cover Sell Success Price:",coverPrice,"Profit:",orderPrice-coverPrice))
    break
   }
  }
  #更新最新值
  lastPrice <- MatchPrice
  lastMAValue <- MAValue
 }

}
