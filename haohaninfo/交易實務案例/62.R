#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始格式
MAarray <- numeric(0)
MAnum <- 10
lastHMTime <- 0 

while(TRUE){

 #取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchPrice <- as.numeric(Mdata[[1]][2])
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))


 #計算MA
 if(length(MAarray)==0){
     MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
     lastHMTime <- HMTime
     next
 }else if (HMTime==lastHMTime){
   MAarray[1] <- MatchPrice
 }else if(HMTime>lastHMTime){    
     MAarray <- c(MatchPrice,MAarray[1:(MAnum-1)])
 }

 print(MAarray)

 cat(HMTime," MA",round(mean(MAarray,na.rm=TRUE),2),"\n")
  
 lastHMTime <- HMTime

}
