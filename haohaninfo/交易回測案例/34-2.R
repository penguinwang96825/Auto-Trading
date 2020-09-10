# 讀取I020、I080 資料
I020 <- read.csv('Futures_20170815_I020.csv')
I080 <- read.csv('Futures_20170815_I080.csv')
# 設定X 軸時間格式
I020Time <- strptime(sprintf('%08d',I020$INFO_TIME),'%H%M%S')
I080Time <- strptime(sprintf('%08d',I080$INFO_TIME),'%H%M%S')
# 繪製價格折線圖
par(fig=c(0,10,5,10)/10)
plot(I020Time,I020$PRICE,type="l",ylab="Price",xaxt="n",xlab="")
# 繪製上五檔量
par(fig=c(0,10,2.5,6)/10)
par(new=T)
plot(I080Time,I080$BUY_QTY1 + I080$BUY_QTY2 + I080$BUY_QTY3 + I080$BUY_QTY4 + I080$BUY_QTY5,type='h',col='red',ylab="B",xaxt="n",xlab="")
# 接著繪製下五檔量
par(fig=c(0,10,0,3.5)/10)
par(new=T)
plot(I080Time,(I080$SELL_QTY1 + I080$SELL_QTY2 + I080$SELL_QTY3 + I080$SELL_QTY4 + I080$SELL_QTY5 ) *-1,type='h',col='green',ylab="S")