#取得即時報價，詳細在技巧51
source("function.R")

#設定初始的資料格式
Qty <- 0
lastMinute <- 0
lastQty <- 0

while(index!=0){
 #取得成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchAmount <- as.numeric(Mdata[[1]][4])
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))
 
 #若為初始值，即更新最新一筆資訊
 if(lastQty==0){
  lastQty <- MatchAmount
  lastMinute <- HMTime
 }else{
  #若非初始值，即更新最新一筆資訊
  #換分鐘則新增一筆資料
  if(HMTime > lastMinute){
   lastQty <- MatchAmount
   lastMinute <- HMTime
   Qty <- 0
  }else{
   Qty <- MatchAmount - lastQty

  }
 }

 #當每分鐘累計量超過1000時出場
 if(Qty >= 1000){
  if (index ==1){
   index <- 0
   print("Cover Buy Success!")
   break
  }else if(index==(-1)){
   index <- 0
   print("Cover Sell Success!")
   break
  }

 }

}
