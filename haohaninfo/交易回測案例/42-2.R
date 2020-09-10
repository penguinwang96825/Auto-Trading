I020 <- read.csv('Futures_20170815_I020.csv')
sellTrendQty=0
buyTrendQty=0
for (i in 2:nrow(I020))
{
 if(I020[i-1,5]<I020[i,5]){sellTrendQty=sellTrendQty+I020[i,6]}
 if(I020[i-1,5]>I020[i,5]){buyTrendQty=buyTrendQty+I020[i,6]}
 cat(I020[i,1],"Out Disk Qty:",sellTrendQty,"In Disk Qty:",buyTrendQty,"\n")
}