# 取得成交資訊
I020 <- read.csv('Futures_20170815_I020.csv')
# 定義X 軸時間格式
Time <- strptime(sprintf('%08d',I020$INFO_TIME),'%H%M%S')
# 繪製圖表
plot(Time,I020$PRICE,type='l')