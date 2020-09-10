#取得即時報價，詳細在技巧51
source("function.R")

#設定初始的資料格式
Qty <- matrix(, nrow = 0, ncol = 2)

while(TRUE){
 #取得成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 MatchAmount <- as.numeric(Mdata[[1]][4]) 
 #設置方便進行判斷的時間格式 
 HMTime <- as.numeric(paste0(substr(Mdata[[1]][1],1,2),substr(Mdata[[1]][1],4,5)))

 #若為初始值，即更新最新一筆資訊
 if(nrow(Qty)==0){
  lastQty <- MatchAmount
  Qty <- rbind(Qty,c(HMTime,0))
 }else{
  #若非初始值，即更新最新一筆資訊
  #換分鐘則新增一筆資料
  if(HMTime > Qty[nrow(Qty),1]){
   Qty <- rbind(Qty ,c(HMTime,MatchAmount-lastQty))
   lastQty <- MatchAmount
  }else{
   Qty[nrow(Qty),2] <- MatchAmount-lastQty

  }
 }
 print(Qty)

}
