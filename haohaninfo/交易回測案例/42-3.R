# 導入資料主體
I020 <- read.csv(" 檔案名稱")
# 起始時間至結束時間
AllTime <- subset(I020, INFO_TIME>=as.numeric(StartTime) & INFO_TIME<=as.numeric(EndTime))
# 進場判斷( 包含趨勢判斷)
for(i in 1:nrow(AllTime)){
 if( 進場條件)
 OrderTime <- AllTime[i]$INFO_TIME # 下單時間紀錄
 OrderPrice <- AllTime[i]$Price # 下單價格紀錄
 break
}
AfterOrder <- subset(AllTime, INFO_TIME>=as.numeric(OrderTime))
# 出場判斷( 包含停損停利判斷)
for(i in 1:nrow(AfterOrder)){
 if( 出場條件)
 CoveryTime <- AfterOrder[i]$INFO_TIME # 下單時間紀錄
 CoveryPrice <- AfterOrder[i]$Price # 下單價格紀錄
 break
}