#設置當天日期，取用當天的檔案名稱
Date <- gsub("-","",Sys.Date())
#檔案位置
DataPath <- "D:/data/"
#tail執行檔位置
tailPath <- "./bin/"

#取得成交資訊
GetMatchData <- function(DataPath,Date)
{

 data <- system(paste0(tailPath,'tail.exe -n1 ',DataPath,Date,"_Match.txt"),intern=TRUE)
 mdata <- strsplit(data,",")
 return(mdata)

}

#取得委託資訊
GetOrderData <- function(DataPath,Date)
{

 data <- system(paste0(tailPath,'tail.exe -n1 ',DataPath,Date,"_Commission.txt"),intern=TRUE)
 mdata <- strsplit(data,",")
 return(mdata)

}

#取得上下五檔價資訊
GetUpDn5Data <- function(DataPath,Date)
{

 data <- system(paste0(tailPath,'tail.exe -n1 ',DataPath,Date,"_UpDn5.txt"),intern=TRUE)
 mdata <- strsplit(data,",")
 return(mdata)

}
