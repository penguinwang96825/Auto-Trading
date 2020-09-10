# 讀取資料
I020 <- read.csv('Futures_20170815_I020.csv')
# 設定高低點初始值
highprice=0
lowprice=99999999
for (i in 1:nrow(I020)){
 if(highprice<I020[i,5]){highprice=I020[i,5]}
 if(lowprice>I020[i,5]){lowprice=I020[i,5]}
 cat(I020[i,1],"High Price:",highprice,"Low Price",lowprice,"\n")
}