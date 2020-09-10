#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始格式
inDesk<-0
outDesk<-0

while(TRUE){
 #取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- Mdata[[1]][1]
 MatchPrice <- as.numeric(Mdata[[1]][2])
 MatchQty <- as.numeric(Mdata[[1]][3])
 
 #取得上下五檔價資訊
 UpDn5data<-GetUpDn5Data(DataPath,Date) 
 Dn1Price<- as.numeric(UpDn5data[[1]][2])
 Up1Price<- as.numeric(UpDn5data[[1]][12])

 #進行內外盤判斷
 if ( MatchPrice >= Up1Price ){
  outDesk <- outDesk+MatchQty
 }else if( MatchPrice <= Dn1Price){
  inDesk <- inDesk+MatchQty
 }

 print(paste(MatchTime,MatchPrice,outDesk,inDesk))

}

