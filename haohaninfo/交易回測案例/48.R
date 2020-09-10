png(file = paste0("PlotAddBS.png"), bg = "transparent", width = 1024, height = 768)

ChartTime <- strptime(sprintf('%08d',I020[,1]),"%H%M%S")
plot(ChartTime,A01[,2],type='l')
points(strptime(sprintf('%08d',OrderTime),"%H%M%OS"),OrderPrice,col='red',pch=24,cex=3,bg="red")
points(strptime(sprintf('%08d',CoveryTime),"%H%M%OS"),CoveryPrice,col='blue',pch=25,cex=3,bg="blue")

dev.off()