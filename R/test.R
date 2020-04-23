# 0) track existing blobs
# 1) need to search for / match new blobs
# 2) need to search for / match blobs that have already been produced
# 3) check that sublet vs apa are distinguished in the merged product
# 4) retain only non-redundant records
# 5) remove intermed. files, after "join"

library(Rcpp) # install.packages("Rcpp")
library(reticulate) # install.packages("reticulate")

p_sep <- .Platform$file.sep # platform specific path separator

mod<-function(x, m){
  return(x - floor(x / m) * m)
}

err<-function(m){
  cat(paste("Error:", m, "\n"))
  quit()
}

pr<-function(x){
  # thanks to Sam Albers and Craig Hutton for helping solve this:
  print(paste(paste(deparse(substitute(x)), "="), x))
}

src<-function(x){
  # source a cpp function
  cat(paste("src(\"", x, "\")\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

harmari_craigslist_parsing<-function(html_file, meta_file){

  # c++ functionality    
  src("cpp/lc.cpp") # wc -l analog to avoid R.utils dep
  src("cpp/extract.cpp")
  src("cpp/insist.cpp") # assertion
  src("cpp/csv_cat.cpp") # merge arb. large csv: assert headers match, keep first hdr
  src("cpp/find_start.cpp") # index an HTML nested in csv, find <HTML> byte start locs

  # python functionality
  cat("Note: if prompted to install Miniconda, please say yes!\n")
  py_discover_config()
  py_available(initialize=TRUE)
  if(!py_available()){
    err("python not initialized")
  }
  import_from_path("py")
  source_python("py/join.py")
  source_python("py/html_parse.py")

  test_csv_cat<-function(){
    # test big-data resilient csv-file concatenation
  
    print(paste("test", p_sep, "A.csv", sep=""))
    csv_cat(c(paste("test", p_sep, "A.csv", sep=""),
    paste("test", p_sep, "B.csv", sep=""),
    paste("test", p_sep, "C.csv", sep="")))

    x <- read.csv(paste("test", p_sep, "C.csv", sep=""), header=TRUE)
    for(i in 0: 7){
      a <- ceiling((i + 1)/ 2)
      b <- b <- 1 + mod(i, 2)
      insist(x[a, b] == i + 1)
    }
  }
  test_csv_cat()
      
  # test file indexing
  tag_file <-paste(html_file, "_tag", sep="")
  if(!file.exists(tag_file)){
    find_start(html_file)
  }

  extract(html_file)  # HTML file extraction

  # count number of records from "meta" file
  n_records <-lc(meta_file)
  html_parse(paste(html_file, n_records, sep=","))
  join(paste(html_file, meta_file, n_records, sep=','))
}


meta_file <- "craigslist-bc-sublets-data-mar.csv"
html_file <- "craigslist-sublet-data-bc-html-mar.csv"
harmari_craigslist_parsing(html_file, meta_file)
