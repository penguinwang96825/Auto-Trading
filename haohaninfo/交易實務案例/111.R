#取得即時報價，詳細在技巧51
source("function.R")
source("order.R")

#設定初始倉位，若為0則為無在倉部位
index <- 0

#設定停損停利點
stopLoss <- 10
takeProfit <- 20
maxProfit <- NA
fallBack <- 0.75

#進出場價格定義
orderPrice <- 0
coverPrice <- 0

#設定進場出場時機點
trendEndTime <- strptime('08:50:00.00','%H:%M:%OS')
endTime <- strptime('09:00:00.00','%H:%M:%OS')

#高低點設定
highPrice <- NA
lowPrice <- NA
spread <- NA

#進場條件判斷
while (index==0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])

 #在9:00之前，判斷價格高低點
 if (MatchTime >= trendEndTime){
  if (is.na(highPrice)){
   #取得最高最低價、價差 
   highPrice <- as.numeric(Mdata[[1]][7])
   lowPrice <- as.numeric(Mdata[[1]][8])
   spread <- highPrice - lowPrice
   print(paste("highPrice:",highPrice,"lowPrice:",lowPrice,"spread:",spread))
  }else{
   if (MatchPrice > highPrice + spread){
    orderInfo <- OrderMKT('TX00','B',1)
    orderPrice <- as.numeric(strsplit(orderInfo,",")[[1]][5])
    index <- 1
    print(paste("Order Buy Success Price:",orderPrice))
    print(paste("highPrice:",highPrice,"lowPrice:",lowPrice,"spread:",spread))
    break
   }else if (MatchPrice < lowPrice - spread){
    orderInfo <- OrderMKT('TX00','S',1)
    orderPrice <- as.numeric(strsplit(orderInfo,",")[[1]][5])
    index <- (-1)
    print(paste("Order Sell Success Price:",orderPrice))
    print(paste("highPrice:",highPrice,"lowPrice:",lowPrice,"spread:",spread))
    break
   }
  } 
 }
}


while (index!=0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])

 if(index == 1){
  #計算目前價差
  diff <- MatchPrice - orderPrice
  if( diff >= takeProfit ){
   maxProfit <- diff
  #價格回跌出場 
  }else if( (!is.na(maxProfit) & maxProfit * fallBack > diff) | MatchPrice + stopLoss < orderPrice | MatchTime >= endTime ){
   coverInfo <- OrderMKT('TX00','S',1)
   coverPrice <- as.numeric(strsplit(coverInfo,",")[[1]][5])
   index <- 0
   print(paste("Cover Buy Success Price:",coverPrice,"Profit:",coverPrice-orderPrice))
   break
  }
 }else if(index == (-1)){
  #計算目前價差
  diff <- orderPrice - MatchPrice
  if( diff >= takeProfit ){
   maxProfit <- diff
  #價格回跌出場
  }else if( (!is.na(maxProfit) & maxProfit * fallBack > diff) | MatchPrice < orderPrice + stopLoss | MatchTime >= endTime ){
   coverInfo <- OrderMKT('TX00','B',1)
   coverPrice <- as.numeric(strsplit(coverInfo,",")[[1]][5])
   index <- 0
   print(paste("Cover Sell Success Price:",coverPrice,"Profit:",orderPrice-coverPrice))
   break
  }
 }
}
