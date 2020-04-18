p_sep <- .Platform$file.sep

# get the name of a variable
namae<-function(x){
  return(deparse(substitute(x)))
}

pr<-function(x){
  print(paste(paste(namae(x), "="), x), quote=FALSE)	
}

mod<-function(x, m){
  return(x - floor(x / m) * m)
}


library(Rcpp)
Rcpp::sourceCpp("cpp/insist.cpp", cacheDir='tmp')  # assertion
Rcpp::sourceCpp("cpp/csv_cat.cpp", cacheDir='tmp') # merge arbitrarily large csv files, keeping one copy of header only

print(paste("test", p_sep, "A.csv", sep=""))


# test csv concatenation
csv_cat(c(paste("test", p_sep, "A.csv", sep=""),
	  paste("test", p_sep, "B.csv", sep=""),
	  paste("test", p_sep, "C.csv", sep="")))

x <- read.csv("test/C.csv", header=TRUE)

for(i in 0: 7){
  a <- ceiling((i + 1)/ 2)
  b <- b <- 1 + mod(i, 2)
  insist(x[a, b] == i + 1)
}

# should be able to automatically generate:
# Rcpp::sourceCpp("name of cpp file")
# #include<Rcpp.h>
# using namespace Rcpp;
# //[[Rcpp::export]]
# need to add cacheDir as well (need to make the directory, too)!


# http://adv-r.had.co.nz/Rcpp.html
# http://dirk.eddelbuettel.com/papers/rcpp_sydney-rug_jul2013.pdf
# https://gallery.rcpp.org/articles/working-with-Rcpp-StringVector/
# http://dirk.eddelbuettel.com/code/rcpp.html
# http://dirk.eddelbuettel.com/code/rcpp/Rcpp-quickref.pdf
