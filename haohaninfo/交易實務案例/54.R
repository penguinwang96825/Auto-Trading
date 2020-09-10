#取得即時報價，詳細在技巧51
source("function.R")

while(TRUE){
 
#取得成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- Mdata[[1]][1]
 MatchAmount <- as.numeric(Mdata[[1]][4])
 MatchB <- as.numeric(Mdata[[1]][5])
 MatchS <- as.numeric(Mdata[[1]][6])

 #計算平均買賣口數
 averageBuyNum <- MatchAmount/MatchB
 averageSellNum <- MatchAmount/MatchS

 print(paste(MatchTime,averageBuyNum,averageSellNum))

}
