setwd("資料夾路徑")
I020 <- read.csv('./Futures_20170815_I020.csv')
p1 <- subset(I020,INFO_TIME>8590000 &INFO_TIME<=9000000)
c(p1[1,]$Match_Price,max(p1$Match_Price),min(p1$Match_Price),p1[nrow(p1),]$Match_Price,sum(p1$QTY))