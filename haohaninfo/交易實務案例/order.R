#設定下單程式位置
ExecPath <- "./bin/"

#市價委託單
OrderMKT<-function(Product,BorS,Qty){
 OrderNo<-system2(paste0(ExecPath,'Order.exe') ,args=paste(Product,BorS,'0',Qty,'MKT','IOC','1'),stdout = TRUE)
 Match<-system2(paste0(ExecPath,'GetAccount.exe'),args=paste(OrderNo),stdout = TRUE)
 return(Match)
}

#限價委託單
OrderLMT<-function(Product,BorS,Price,Qty){
 OrderNo<-system2(paste0(ExecPath,'Order.exe')  ,args=paste(Product,BorS,Price,Qty,'LMT','ROD','1'),stdout = TRUE)
 return(OrderNo)
}

#單筆帳務查詢
QueryOrder<-function(OrderNo){
 Match<-system2(paste0(ExecPath,'GetAccount.exe'),args=paste(OrderNo),stdout = TRUE)
 return(Match)
}

#總帳務查詢
QueryAllOrder<-function(){
 Match<-system2(paste0(ExecPath,'GetAccount.exe'),args=paste("ALL"),stdout = TRUE)
 return(Match)
}

#未平倉查詢
QueryOnOpen<-function(){
 onopeninfo<-system2(paste0(ExecPath,'OnOpenInterest.exe'),stdout = TRUE)
 return(onopeninfo)
}

#權益數查詢
QueryRight<-function(){
 rightinfo<-system2(paste0(ExecPath,'FutureRights.exe'),stdout = TRUE)
 return(rightinfo)
}

#取消委託單
CancelOrder<-function(OrderNo){
 system2(paste0(ExecPath,'Order.exe')  ,args=paste('Delete',OrderNo),stdout = TRUE)
}

#查詢是否成交
QueryMatch<-function(OrderNo){
 Match<-system2(paste0(ExecPath,'GetAccount.exe'),args=paste(OrderNo),stdout = TRUE)
 if(Match=="Nodata"){
  return(FALSE)
 }else{
  return(TRUE)
 }
}

#限價單到期轉市價單
LMT2MKT <- function(Product,BorS,Price,Qty,Sec){
 OrderNo<-system2(paste0(ExecPath,'Order.exe')  ,args=paste(Product,BorS,Price,Qty,'LMT','ROD','1'),stdout = TRUE)
 to <- Sys.time()
 while(as.numeric(difftime(Sys.time(), to, u = 'secs')) < Sec){
  if(isTRUE(QueryMatch(OrderNo))){
   return(QueryOrder(OrderNo))
  }
 }
 CancelOrder(OrderNo)
 Match<-OrderMKT(Product,BorS,Qty)
 return(Match)
}

#限價單到期轉刪單
LMT2DEL <- function(Product,BorS,Price,Qty,Sec){
 OrderNo<-system2(paste0(ExecPath,'Order.exe')  ,args=paste(Product,BorS,Price,Qty,'LMT','ROD','1'),stdout = TRUE)
 to <- Sys.time()
 while(as.numeric(difftime(Sys.time(), to, u = 'secs')) < Sec){
  if(isTRUE(QueryMatch(OrderNo))){
   return(QueryOrder(OrderNo))
  }
 }
 CancelOrder(OrderNo)
 return(FALSE)
}
