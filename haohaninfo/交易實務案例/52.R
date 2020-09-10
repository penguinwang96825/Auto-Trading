#取得即時報價，詳細在技巧51
source("function.R")

#設定初始的資料格式
OHLC <- matrix(, nrow = 0, ncol = 5)

while(TRUE){
 #取得報價資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchPrice <- as.numeric(Mdata[[1]][2])
 #設置方便進行判斷的時間格式 
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))

 #若為初始值，即更新最新一筆資訊
 if( nrow(OHLC) == 0 ){
  OHLC <- rbind(OHLC,c(HMTime,MatchPrice,MatchPrice,MatchPrice,MatchPrice))
 }else{
  #若非初始值，即更新最新一筆資訊
  if(HMTime > OHLC[nrow(OHLC),1]){
   OHLC <- rbind(OHLC ,c(HMTime,MatchPrice,MatchPrice,MatchPrice,MatchPrice))
  }else{
   #計算開高低收
   if(MatchPrice>OHLC[nrow(OHLC),3]){
    OHLC[nrow(OHLC),3] <- MatchPrice
   }else if(MatchPrice<OHLC[nrow(OHLC),4]){
    OHLC[nrow(OHLC),4] <- MatchPrice
   }
   OHLC[nrow(OHLC),5] <- MatchPrice
  }

 }
 print(OHLC)

}


