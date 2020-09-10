#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始格式
inDesk<-0
outDesk<-0
#設定趨勢判斷時間
trendEndTime <- strptime('09:00:00.00','%H:%M:%OS')
trend <- NA

while(TRUE){
 #取得即時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
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

 if( MatchTime >= trendEndTime & is.na(trend) ){
  if(outDesk > inDesk){
   trend <- 1
  }else if(outDesk < inDesk){
   trend <- (-1)
  }else{
   trend <- 0
  }

 }

 if(!is.na(trend)){
  print(trend)
 }
}
