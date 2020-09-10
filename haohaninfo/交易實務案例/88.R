#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1
orderPrice <- 10000

#停損停利點數
stopLoss <- 10
takeProfit <- 10

#出場條件判斷
while (index!=0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])

 if(index == 1 & (MatchPrice > orderPrice + takeProfit | MatchPrice + stopLoss < orderPrice ) ){
  index <- 0
  print("Cover Buy Success!")
  break
 }else if (index == (-1) & ( MatchPrice + takeProfit < orderPrice | MatchPrice > orderPrice + stopLoss )){
  index <- 0
  print("Cover Sell Success!")
  break
  
 }
 
}

