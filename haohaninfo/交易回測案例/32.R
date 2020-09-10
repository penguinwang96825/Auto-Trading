# 讀取成交資訊
I020 <- read.csv('Futures_20170815_I020.csv')
# 時間轉秒數
TimeToNumber <- function(Time)
{
 T<-as.numeric(substring(Time,1,2))*360000+as.numeric(substring(Time,3,4))*6000+as.numeric(substring(Time,5,6))*100+as.numeric(substring(Time,7,8))
 return(T)
}
# 定義變數
STime <- TimeToNumber('08450000') # 起始時間
cycle <- 6000 # 週期為分鐘
Qty <- numeric(0)
# 計算每個周期的總量
for (i in 1:nrow(I020)){
 if(TimeToNumber(sprintf('%08d',I020[i,]$INFO_TIME))>STime+cycle){
  if(length(Qty)==0){
   Qty <- rbind(Qty,c(I020[i,]$INFO_TIME,I020[i,]$AMOUNT,I020[i,]$AMOUNT))
  }else{
   amount <- I020[i,]$AMOUNT-Qty[nrow(Qty),2]
   Qty <- rbind(Qty,c(I020[i,]$INFO_TIME,I020[i,]$AMOUNT,amount))
  }
  STime <- STime+cycle
 }
}
# 定義該圖表在整體繪圖的位置
par(fig=c(0,10,3.5,10)/10)
# 定義X 軸時間格式
Time <- strptime(sprintf('%08d',I020$INFO_TIME),'%H%M%S')
# 繪製圖表
plot(Time,I020$PRICE,type='l',xaxt = "n",xlab="")
# 定義該圖表在整體繪圖的位置
par(fig=c(0,10,0,4.5)/10)
par(new=T)
# 由於兩張圖X 時間軸不相等，所以要另外定義時間
QTime <- strptime(sprintf('%08d',Qty[,1]),'%H%M%S')
# 繪製量能圖
plot(QTime,Qty[,3],type='h')