# 取得委託資訊
I030 <- read.csv('Futures_20170815_I030.csv')
# 定義X 軸時間格式
OrderTime <- strptime(sprintf('%08d',I030$INFO_TIME),'%H%M%S')
# 繪製量差圖表
plot(OrderTime,I030$SELL_QTY-I030$BUY_QTY,type='l')