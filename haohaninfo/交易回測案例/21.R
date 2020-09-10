TimeToNumber <- function(Time)
{
 T<-as.numeric(substring(Time,1,2))*360000+as.numeric(substring(Time,3,4))*6000+as.numeric(substring(Time,5,6))*100+as.numeric(substring(Time,7,8))
 return(T)
}