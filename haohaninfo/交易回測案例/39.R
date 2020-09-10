RS <- read.csv("profit.log",header=FALSE)
colnames(RS) <- c("SerialNumber","Good","ODate","OTime","OPrice","BorS","Number","
CDate","CTime","CPrice")
profit <- numeric(0)
for( i in 1:nrow(RS)){
 if(RS[i,]$BorS=="B"){
  profit <- c(profit,RS[i,]$CPrice - RS[i,]$OPrice)
 }else{
  profit <- c(profit,RS[i,]$OPrice - RS[i,]$CPrice)
 }
}
cumsum(profit)
plot(cumsum(profit),type='l',main='performance')