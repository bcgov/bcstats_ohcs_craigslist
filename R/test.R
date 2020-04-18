# still need to search for / match the different pairs of files! and need to search for and match the compiled blobs!
# also need to check that merged APA vs SUB are distinguished in the product
html_file <- "craigslist-sublet-data-bc-html-mar.csv"

p_sep <- .Platform$file.sep

# get the name of a variable
name<-function(x){
  return(deparse(substitute(x)))
}
pr<-function(x){
  print(paste(paste(name(x), "="), x), quote=FALSE)
}

mod<-function(x, m){
  return(x - floor(x / m) * m)
}

library(Rcpp)
src<-function(x){
  print(paste("src(\"", x, ")\"", sep=""), quote=FALSE)
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

# test big-data resilient csv-file concatenation
src("cpp/insist.cpp") # assertion
src("cpp/csv_cat.cpp") # merge arbitrarily large csv, asserting headers matching, keeping one copy of header only

print(paste("test", p_sep, "A.csv", sep=""))
csv_cat(c(paste("test", p_sep, "A.csv", sep=""),
	  paste("test", p_sep, "B.csv", sep=""),
	  paste("test", p_sep, "C.csv", sep="")))

x <- read.csv(paste("test", p_sep, "C.csv", sep=""),
	      header=TRUE)
for(i in 0: 7){
  a <- ceiling((i + 1)/ 2)
  b <- b <- 1 + mod(i, 2)
  insist(x[a, b] == i + 1)
}

# test file indexing
src("cpp/find_start.cpp") # index a file with HTML nested inside csv, finding locations of <HTML> start tags
tag_file <-paste(html_file, "_tag", sep="")
if(!file.exists(tag_file)){
  find_start(html_file)
}


# test HTML file extraction
src("cpp/extract.cpp")
extract(html_file)





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
