# 取成交資訊
I020 <- read.csv('Futures_20170815_I020.csv')
# 時間轉秒數
TimeToNumber <- function(Time)
{
 T<-as.numeric(substring(Time,1,2))*360000+as.numeric(substring(Time,3,4))*6000+as.numeric(substring(Time,5,6))*100+as.numeric(substring(Time,7,8))
 return(T)
}
# 定義相關變數0
MAarray <- numeric(0)
MA <- numeric(0)
MAValue <- 0
STime <- TimeToNumber('08450000')
cycle <- 6000
len <- 10
# 進行MA 計算
for (i in 1:nrow(I020)){
 if(length(MAarray)==0){
  MAarray <- c(I020[i,]$PRICE,MAarray)
 }else{
  if(TimeToNumber(I020[i,]$INFO_TIME)<STime+cycle){
   MAarray[1] <- I020[i,]$ PRICE
  }else{
   if(length(MAarray)==len){
    MAarray <- c(I020[i,]$ PRICE,MAarray[-len])
   }else{
    MAarray <- c(I020[i,]$ PRICE,MAarray)
   }
   STime <- STime+cycle
  }
 }
 MAValue <- sum(MAarray)/length(MAarray)
 MA <- rbind(MA,c(I020[i,]$INFO_TIME,MAValue))
 #print(c(I020[i,]$INFO_TIME,MAValue))
}