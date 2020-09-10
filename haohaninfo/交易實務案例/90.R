#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1

#設定變數初始格式
MAarray <- numeric(0)
MAnum <- 10
lastHMTime <- 0
lastPrice <- 0 
lastMAValue <- 0

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
  #若沒有前一筆資訊，則無法進行MA穿越判斷
  if (lastMAValue == 0 ){
   lastMAValue <- MAValue
   lastPrice <- MatchPrice
   next
  } 
  #進行判斷，本範例預設進場買單
  if(index==1){
   if(lastPrice >= lastMAValue & MatchPrice < MAValue){
    index <- 0
    print("Cover Buy Success!")
    break
   }
  }else if(index==(-1)){
   if(lastPrice <= lastMAValue & MatchPrice > MAValue){
    index <- 0
    print("Cover Sell Success!")
    break
   }
  }
  #更新最新值
  lastPrice <- MatchPrice
  lastMAValue <- MAValue
 }

}

