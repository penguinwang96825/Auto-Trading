# 讀取I080 資料
I080 <- read.csv('Futures_20170815_I080.csv')
# 設定X 軸時間格式
Time <- strptime(sprintf('%08d',I080$INFO_TIME),'%H%M%S')
# 首先繪製上五檔量
par(fig=c(0,10,4.5,10)/10)
plot(Time,I080$BUY_QTY1 + I080$BUY_QTY2 + I080$BUY_QTY3 + I080$BUY_QTY4 + I080$BUY_QTY5,type='h',col='red',ylab="B",xaxt="n",xlab="")
# 接著繪製下五檔量
par(fig=c(0,10,0,5.5)/10)
par(new=T)
plot(Time,(I080$SELL_QTY1 + I080$SELL_QTY2 + I080$SELL_QTY3 + I080$SELL_QTY4 + I080$SELL_QTY5 ) *-1,type='h',col='green',ylab="S")