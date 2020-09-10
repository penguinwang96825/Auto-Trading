#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1
orderPrice <- 10000

#設定停利基準點
takeProfit <- 20
maxProfit <- NA
fallBack <- 0.75

#出場條件判斷
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
  }else if( !is.na(maxProfit) & maxProfit * fallBack > diff ){
   index <- 0
   print("Cover Buy Success!")
   break
  }
 }else if(index == (-1)){
  #計算目前價差
  diff <- orderPrice - MatchPrice
  if( diff >= takeProfit ){
   maxProfit <- diff
  #價格回跌出場
  }else if( !is.na(maxProfit) & maxProfit * fallBack > diff ){
   index <- 0
   print("Cover Sell Success!")
   break
  }
 }
}

