# 取得成交資訊
I020 <- read.csv('Futures_20170815_I020.csv')
# 定義X 軸時間格式
Time <- strptime(sprintf('%08d',I020$INFO_TIME),'%H%M%S')
# 繪製圖表
plot(Time,I020$PRICE,type='l')
# 計算買筆及賣筆的差額
I020 <- cbind(I020,c(I020$MATCH_BUY_CNT)-c(0,I020[-nrow(I020),]$MATCH_BUY_CNT))
I020 <- cbind(I020,c(I020$MATCH_SELL_CNT)-c(0,I020[-nrow(I020),]$MATCH_SELL_CNT))
# 轉換時間軸的單位
BPointTime <- strptime(sprintf('%08d',I020[which(I020[,10]==1&I020[,11]>=30),]$INFO_TIME),"%H%M%S")
SPointTime <- strptime(sprintf('%08d',I020[which(I020[,11]==1&I020[,10]>=30),]$INFO_TIME),"%H%M%S")
# 轉換價格的單位
BPointPrice <- I020[which(I020[,10]==1&I020[,11]>=30),]$PRICE
SPointPrice <- I020[which(I020[,11]==1&I020[,10]>=30),]$PRICE
# 標記點位
points(BPointTime,BPointPrice,col='red',bg='red',cex=1.5,pch=21)
points(SPointTime,SPointPrice,col='green',bg='green',cex=1.5,pch=21)