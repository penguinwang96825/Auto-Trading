#取得即時報價，詳細在技巧51
source("function.R")

#設定初始的資料格式
averageBuyNum<-0
averageSellNum<-0
endTime <- strptime('09:00:00.00','%H:%M:%OS')
trend <- NA

while(TRUE){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchAmount <- as.numeric(Mdata[[1]][4])
 MatchB <- as.numeric(Mdata[[1]][5])
 MatchS <- as.numeric(Mdata[[1]][6])

 if( MatchTime > endTime & is.na(trend) ){
  #計算平均買賣口數
  averageBuyNum <- MatchAmount/MatchB
  averageSellNum <- MatchAmount/MatchS
  if ( averageBuyNum > averageSellNum ){
   trend <- 1
  }else if(averageBuyNum < averageSellNum){
   trend <- (-1)
  }else{
   trend <- 0
  }
 }
 
 if(!is.na(trend)){
  print(trend)
 }
}
