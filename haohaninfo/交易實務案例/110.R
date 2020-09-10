#取得即時報價，詳細在技巧51
source("function.R")
source("order.R")

#設定初始倉位，若為0則為無在倉部位
index <- 0

#設定停損停利點
stopLoss <- 10
takeProfit <- 10

#設定進出場時機點
orderPrice <- 0
coverPrice <- 0
orderTime <- strptime('08:50:00.00','%H:%M:%OS')
coverTime <- strptime('09:00:00.00','%H:%M:%OS')

#進場條件判斷
while (index==0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])

 if(MatchTime >= orderTime){
  orderInfo <- OrderMKT('TX00','B',1)
  orderPrice <- as.numeric(strsplit(orderInfo,",")[[1]][5])
  index <- 1
  print(paste("Order Buy Success Price:",orderPrice))
  break
 }
 
}

#出場條件判斷
while (index!=0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])

 if(MatchPrice > orderPrice + takeProfit | MatchPrice + stopLoss < orderPrice | MatchTime >= coverTime ){
  coverInfo <- OrderMKT('TX00','S',1)
  coverPrice <- as.numeric(strsplit(coverInfo,",")[[1]][5])
  index <- 0
  print(paste("Cover Buy Success Price:",coverPrice,"Profit:",coverPrice-orderPrice))
  break
 }
}

