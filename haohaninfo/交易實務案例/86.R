#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始值
index <- 0
lastBCount<-0
lastSCount<-0
accB <- 0
accS <- 0

while(index ==0){

 #取得即時報價資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <-strptime( Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])
 MatchQty <- as.numeric(Mdata[[1]][3])
 MatchBCount <- as.numeric(Mdata[[1]][5])
 MatchSCount <- as.numeric(Mdata[[1]][6])

 #若為第一次紀錄，不計算跳過
 #防呆機制，重複資料不計算
 if(lastBCount==0 | is.na(lastBCount) | lastBCount == MatchBCount){
  lastBCount <- MatchBCount
  lastSCount <- MatchSCount
  next
 }

 #計算單筆買賣方筆數
 diffBCount <- MatchBCount - lastBCount
 diffSCount <- MatchSCount - lastSCount

 #計算大單量口數，分別列出單筆以及總量
 if( MatchQty>=10 ){
  if (diffBCount ==1 & diffSCount>1){
   accB <- accB + MatchQty
   #當數量超過30口，並且趨勢相同進場
   if (accB > accS & MatchQty >30 ){
    index <- 1
    print("Order Buy Success!")
    break
   }
   print(paste(MatchTime,MatchQty,0,accB,accS))
  }else if(diffSCount==1 & diffBCount>1){
   accS <- accS + MatchQty
   #當數量超過30口，並且趨勢相同進場
   if (accB < accS & MatchQty >30){
    index <- (-1)
    print("Order Sell Success!")
    break
   }
   print(paste(MatchTime,0,MatchQty,accB,accS))
  }

 }

 

 #紀錄每次最後的買賣方筆數
 lastBCount <- MatchBCount
 lastSCount <- MatchSCount
}
