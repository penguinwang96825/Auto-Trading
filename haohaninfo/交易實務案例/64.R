#取得即時報價，詳細在技巧51
source("function.R")

#設定初始的資料格式
closePrice <- matrix(, nrow = 0, ncol = 2)


while(TRUE){

 #取得成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchPrice <- as.numeric(Mdata[[1]][2])
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))

 #計算每分鐘價格變動
 if( nrow(closePrice) == 0 ){
  closePrice <- rbind(closePrice,c(HMTime,MatchPrice))
 }else{
  if(HMTime > closePrice[nrow(closePrice),1]){
   closePrice <- rbind(closePrice ,c(HMTime,MatchPrice))
  }else{
   closePrice[nrow(closePrice),2] <- MatchPrice
  }

 }
 print(closePrice)

}
