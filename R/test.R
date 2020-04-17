p_sep <- .Platform$file.sep

library(Rcpp)
Rcpp::sourceCpp("cpp/insist.cpp")
Rcpp::sourceCpp("cpp/csv_cat.cpp")

print(paste("test", p_sep, "A.csv", sep=""))


# test csv concatenation
csv_cat(c(paste("test", p_sep, "A.csv", sep=""),
	  paste("test", p_sep, "B.csv", sep=""),
	  paste("test", p_sep, "C.csv", sep="")))

x <- read.csv("test/C.csv", header=TRUE)

insist(x[1, 1] == 1)
insist(x[1, 2] == 2)
insist(x[2, 1] == 3)
insist(x[2, 2] == 4)
insist(x[3, 1] == 5)
insist(x[3, 2] == 6)
insist(x[4, 1] == 7)
insist(x[4, 2] == 8)

# should be able to automatically generate:
# Rcpp::sourceCpp("name of cpp file")
# #include<Rcpp.h>
# using namespace Rcpp;
# //[[Rcpp::export]]


# http://adv-r.had.co.nz/Rcpp.html
# http://dirk.eddelbuettel.com/papers/rcpp_sydney-rug_jul2013.pdf
# https://gallery.rcpp.org/articles/working-with-Rcpp-StringVector/
# http://dirk.eddelbuettel.com/code/rcpp.html
# http://dirk.eddelbuettel.com/code/rcpp/Rcpp-quickref.pdf

