z#取得即時報價，詳細在技巧51
source("function.R")

#設定初始倉位，若為0則為無在倉部位
index <- 0

#設定進場時機點
trendEndTime <- strptime('09:09:00.00','%H:%M:%OS')

#高低點設定
highPrice <- NA
lowPrice <- NA

#進場條件判斷
while (index==0){
 #取得及時成交資訊
 Mdata<-GetMatchData(DataPath,Date)
 #因為要進行比較，所以透過R內建函數strptime轉為R語言的時間格式
 #最小單位可至秒數以下兩位
 MatchTime <- strptime(Mdata[[1]][1],'%H:%M:%OS')
 MatchPrice <- as.numeric(Mdata[[1]][2])


 #在9:00之前，判斷價格高低點
 if (MatchTime >= trendEndTime){
  if (is.na(highPrice)){
   #取得最高最低價 
   highPrice <- as.numeric(Mdata[[1]][7])
   lowPrice <- as.numeric(Mdata[[1]][8])
  }else{
   if (MatchPrice > highPrice){
    index <- 1
    print("Order Buy Success!")
    break
   }else if (MatchPrice < lowPrice){
    index <- (-1)
    print("Order Sell Success!")
    break
   }
  } 
 }
}

#接著以下為出場條件判斷，本章不做介紹