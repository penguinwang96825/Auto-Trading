#取得即時報價，詳細在技巧51
source("function.R")

#假設目前開倉並且開倉價位在10000
index <- 1
orderPrice <- 10000

#設定變數初始格式
inDesk<-0
outDesk<-0

while(index!=0){
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

 #判斷內外盤量反轉
 if(index ==1 ){
  if(outDesk < inDesk){
   index <- 0
   print("Cover Buy Success!")
   break
  }
 }else if(index==(-1)){
  if(outDesk > inDesk){
   index <- 0
   print("Cover Sell Success!")
   break
  }
 }


}
