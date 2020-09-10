source("function.R")

lastBCount<-0
lastSCount<-0
accB <- 0
accS <- 0

while(TRUE){

 Mdata<-GetMatchData(DataPath,Date)
 MatchTime <- Mdata[[1]][1]
 MatchPrice <- as.numeric(Mdata[[1]][2])
 MatchQty <- as.numeric(Mdata[[1]][3])
 MatchBCount <- as.numeric(Mdata[[1]][5])
 MatchSCount <- as.numeric(Mdata[[1]][6])

 if(lastBCount==0 | is.na(lastBCount) | lastBCount == MatchBCount){
  lastBCount <- MatchBCount
  lastSCount <- MatchSCount
  next
 }

 diffBCount <- MatchBCount - lastBCount
 diffSCount <- MatchSCount - lastSCount

 if( MatchQty>=10 ){
  if (diffBCount ==1 & diffSCount>1){
   accB <- accB + MatchQty
   print(paste(MatchTime,MatchQty,0,accB,accS))
  }else if(diffSCount==1 & diffBCount>1){
   accS <- accS + MatchQty
   print(paste(MatchTime,0,MatchQty,accB,accS))
  }

 }

 lastBCount <- MatchBCount
 lastSCount <- MatchSCount
}


