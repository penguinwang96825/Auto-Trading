move_avg <- function(x){
for(i in 1:length(x)){
 if(i != 1) x[i] <- (x[i] + x[i-1])/i
}
 return(x)
}