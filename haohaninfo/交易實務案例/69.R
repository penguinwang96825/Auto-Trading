#取得即時報價，詳細在技巧51
source("function.R")

#設定變數初始值
trendStartTime <- strptime('08:45:00.00','%H:%M:%OS')
trendStartPrice <- NA 
trendEndTime <- strptime('09:00:00.00','%H:%M:%OS')
trendEndPrice <- NA
#用變數作為趨勢標籤
trend <- NA

while(TRUE){

 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])
 
 #取得開盤時間
 if (is.na(trendStartPrice) & MatchTime > trendStartTime ){
  trendStartPrice <- MatchPrice
 }

 #趨勢判斷時間點到，進行趨勢判斷
 if (is.na(trendEndPrice) & MatchTime > trendEndTime ){
  trendEndPrice <- MatchPrice
  #當前價大於開盤價，趨勢看多，用數字1作為標記
  if(trendEndPrice > trendStartPrice){
   trend <- 1 
  #當前價小於開盤價，趨勢看空，用數字-1作為標記
  }else if (trendEndPrice < trendStartPrice){
   trend <- (-1)
  #若價格相同，則為沒有趨勢，用數字0作為標記
  }else{
   trend <- 0
  }
 }

 #確認趨勢判斷
 if(!is.na(trend)){
  print(trend)
 }

}


