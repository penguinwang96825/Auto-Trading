setwd("資料夾路徑")
I020 <- read.csv('Futures_20170815_I020.csv')
p1 <- subset(I020,INFO_TIME<=9000000)
p1[nrow(p1),]