NumberToTime <- function(T)
{
 T1<-sprintf("%02d",T%%100)
 TT<-trunc(T/100)
 T2<-TT%%60
 TT<-trunc(TT/60)
 T3<-TT%%60
 T4<-trunc(TT/60)
 T2<-sprintf("%02d",T2)
 T3<-sprintf("%02d",T3)
 T4<-sprintf("%02d",T4)
 return(paste(T4,T3,T2,T1,sep=''))
}