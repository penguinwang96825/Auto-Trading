# 載入計量金融套件
library(quantmod)
# 載入成交價量資料
I020 <- read.csv('Futures_20170815_I020.csv')
# 時間轉秒數
TimeToNumber <- function(Time)
{
 T<-as.numeric(substring(Time,1,2))*360000+as.numeric(substring(Time,3,4))*6000+as.numeric(substring(Time,5,6))*100+as.numeric(substring(Time,7,8))
 return(T)
}
# 秒數轉時間
NumberToTime <- function(T)
{
 T1<-sprintf("%02d",T%%100)
 TT<-trunc(T/100)
 T2<-TT%%60
 TT<-trunc(TT/60)
 T3<-TT%%60
 T4<-trunc(TT/60)
 T2<-sprintf("%02d",T2)
 T3<-sprintf("%02d",T3)
 T4<-sprintf("%02d",T4)
 return(paste(T4,T3,T2,T1,sep=''))
}
# 定義相關變數
Date = "20170815" # 繪製日期
STime <- TimeToNumber('08450000') # 起始時間
ETime <- TimeToNumber('13450000') # 結束時間，指數期貨結算日13:30 收盤
cycle <- 6000 # 週期為分鐘
len <- ( ETime-STime )/6000 # 每日資料筆數
OHLC <- numeric(0)
# 開始進行資料轉換
for (i in 0:(len-1)){
 Tmp <- subset ( I020 , as.numeric(I020$INFO_TIME) >= as.numeric(NumberToTime(STime+(cycle*i))) & as.numeric(I020$INFO_TIME) < as.numeric(NumberToTime(STime+cycle*(i+1))) )
 OHLC <- rbind( OHLC , paste0(Date," ",NumberToTime(STime+(cycle*(i+1))),",",Tmp[1,]$PRICE,",",max(Tmp$PRICE),",",min(Tmp$PRICE),",",Tmp[nrow(Tmp),]$PRICE,",",sum(Tmp$QTY)) )
}
# 將開高低收轉換為zoo 時間序列資料
OHLC1 <- read.zoo(text=OHLC,sep=",",header=F,tz=' ',format="%Y%m%d %H%M%S")
# 定義欄位名稱
colnames(OHLC1)<-c("Open","High","Low","Close","Volume")
# 定義圖片表頭
titles<-paste0(cycle/100," seconds K-line on ",Date)
# 繪製圖表
chartSeries(OHLC1, theme = chartTheme("white", up.col='red',dn.col='green'),name=
titles,show.grid = TRUE)