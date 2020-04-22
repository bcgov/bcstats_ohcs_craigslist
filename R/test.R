# 0) track existing blobs
# 1) need to search for / match new blobs
# 2) need to search for / match blobs that have already been produced
# 3) check that sublet vs apa are distinguished in the merged product
# 4) retain only non-redundant records
# 5) remove intermed. files, after "join"

meta_file <- "craigslist-bc-sublets-data-mar.csv"
html_file <- "craigslist-sublet-data-bc-html-mar.csv"

library(Rcpp) # install.packages("Rcpp")
library(reticulate) # install.packages("reticulate")

p_sep <- .Platform$file.sep  # platform specific path separator

pr<-function(x){
  # thanks to Sam Albers and Craig Hutton for helping solve this:
  print(paste(paste(deparse(substitute(x)), "="), x))
}

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
src("cpp/csv_cat.cpp") # merge arbitrarily large csv: assert headers match, keep first header

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

# count number of records from "meta" file
src("cpp/lc.cpp") # wc -l analog
n_records <-lc(meta_file)
print(n_records)

# test parsing, python!
print("if you're prompted to install Miniconda, please say yes")
py_discover_config()
py_available(initialize=TRUE)
if(!py_available()){
  print("Error: python not initialized", quote=FALSE)
  quit()
}
import_from_path("py")
source_python("py/html_parse.py")
html_parse(paste(html_file, n_records, sep=","))

source_python("py/join.py")
join(paste(html_file, meta_file, n_records, sep=','))
