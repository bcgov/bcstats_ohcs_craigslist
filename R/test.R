# 0) track existing blobs
# 1) need to search for / match new blobs
# 2) need to search for / match blobs that have already been produced
# 3) check that sublet vs apa are distinguished in the merged product
meta_file <- "craigslist-bc-sublets-data-mar.csv"
html_file <- "craigslist-sublet-data-bc-html-mar.csv"

library(Rcpp) # install.packages("Rcpp")
library(reticulate) # install.packages("reticulate")

# platform specific path separator
p_sep <- .Platform$file.sep

mod<-function(x, m){
  return(x - floor(x / m) * m)
}

# source a cpp function
src<-function(x){
  cat(paste("src(\"", x, "\")\n", sep="")) # , quote=FALSE)
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
if(FALSE){
  extract(html_file)
}
print("extract html complete.", quote=FALSE)



# test parsing, python!
print("if you're prompted to install Miniconda, please say yes")
py_discover_config()
py_available(initialize=TRUE)
if(!py_available()){
  print("Error: python not initialized", quote=FALSE)
  quit()
}
source_python("py/test.py")

src("cpp/lc.cpp") # wc -l analog
n_records <-lc(meta_file)




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
