#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始值
OHLC <- matrix(, nrow = 0, ncol = 5)
tick200 <- numeric(0)
tickNum <- 1

while(TRUE){

 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- Mdata[[1]][1]
 MatchPrice <- as.numeric(Mdata[[1]][2])

 #開始累計
 if (tickNum < 200 ){
  tick200 <- c(tick200,MatchPrice)
 }else{
  #每兩百筆顯示一次結果
  OHLC <- rbind(OHLC,c(MatchTime,tick200[1],max(tick200),min(tick200),MatchPrice))
  print(OHLC)
  tick200 <- numeric(0)
  tickNum <- 0
 }

 tickNum <- tickNum+1
 
}
