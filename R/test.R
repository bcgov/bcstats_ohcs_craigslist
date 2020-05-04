library(Rcpp)

## source a c++ function
src<-function(x){
  cat(paste("src(\"", x, "\")\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

src("cpp/lc.cpp")

