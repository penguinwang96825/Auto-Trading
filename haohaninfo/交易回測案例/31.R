# 取委託資訊
I030 <- read.csv('Futures_20170815_I030.csv')
# 定義X 軸時間格式
Time <- strptime(sprintf('%08d',I030$INFO_TIME),'%H%M%S')
# 繪製買方比重線圖
plot(Time,I030$BUY_QTY/I030$BUY_ORDER,type='l',col='red')
# 疊加賣方比重線
lines(Time,I030$SELL_QTY/I030$SELL_ORDER,col='green')