src_test <- function(){
  library(Rcpp)
  ## source a c++ function
  src<-function(x){
    cat(paste("src(", x, ")\n", sep=""))
    Rcpp::sourceCpp(x, cacheDir='tmp')
  }
  src("cpp/lc.cpp") # wc -l analog to avoid R.utils dep
  src("cpp/head.cpp") # head -1 analog
  src("cpp/insist.cpp") # assertion
  src("cpp/extract.cpp")
  src("cpp/csv_cat.cpp") # merge arb. large csv: assert headers match, keep first hdr
  src("cpp/find_start.cpp") # index an HTML nested in csv, find <HTML> byte start locs
  src("cpp/head.cpp") # head -1 analog
  src("cpp/fileSize.cpp") # file size
  src("cpp/csv_cat.cpp")
}


# include other files if their member functions not yet def'd
my_fn <- parent.frame(2)$ofile
scripts <- c("run.R", "setup.R")
for(f in Sys.glob("*.R")){
  if(! is.null(my_fn)) if(f == my_fn) next
  if(!(f %in% scripts)){
    if(!exists(strsplit(f, "\\.")[[1]][1], inherits=TRUE)) source(f)
  }
}