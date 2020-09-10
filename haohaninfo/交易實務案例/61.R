#取得即時報價，詳細在技巧51
source("function.R")

while(TRUE){

#取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- Mdata[[1]][1]
 MatchPrice <- as.numeric(Mdata[[1]][2])

#取得即時上下五檔價資訊
 UpDn5data<-GetUpDn5Data(DataPath,Date) 
 allDnPrice <- 0
 allUpPrice <- 0
 allDnQty <- 0
 allUpQty <- 0

 #計算上下五檔平均成本
 for ( i in 1:5 ){
  allDnPrice <- allDnPrice + as.numeric(UpDn5data[[1]][i*2])*as.numeric(UpDn5data[[1]][i*2+1])
  allUpPrice <- allUpPrice + as.numeric(UpDn5data[[1]][i*2+10])*as.numeric(UpDn5data[[1]][i*2+11])
  allDnQty <- allDnQty + as.numeric(UpDn5data[[1]][i*2+1])
  allUpQty <- allUpQty + as.numeric(UpDn5data[[1]][i*2+11])
 }

 print(paste(MatchTime,MatchPrice,allDnPrice/allDnQty,allUpPrice/allUpQty))

}
