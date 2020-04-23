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

# thanks to Sam Albers and Craig Hutton for helping solve this
pr<-function(x){
  print(paste(paste(deparse(substitute(x)), "="), x))
}

# source a c++ function
src<-function(x){
  cat(paste("src(\"", x, "\")\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

# parse craigslist data as supplied by Harmari, inc.
harmari_craigslist_parsing<-function(html_file, meta_file){

  # c++ functionality    
  src("cpp/lc.cpp") # wc -l analog to avoid R.utils dep
  src("cpp/head.cpp") # head -1 analog
  
  head(html_file)
  err("done")

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

  # test big-data resilient csv-file concatenation
  test_csv_cat<-function(){
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
  
  mkdir<-function(fn){
    dir.create(fn, showWarnings = FALSE)
  }

  # 1) index the html file
  tag_file <-paste(html_file, "_tag", sep="")
  if(!file.exists(tag_file)){
    find_start(html_file)
  }

  # 2) extract html files
  mkdir("html")
  mkdir("otherAttributes")
  extract(html_file)  # HTML file extraction

  # 3) count records from "meta" file
  n_records <-lc(meta_file)

  # 4) parse the html files using multithreading
  mkdir("parsed")
  html_parse(paste(html_file, n_records, sep=","))

  # 5) join the HTML data with the metadata from the other file
  join(paste(html_file, meta_file, n_records, sep=','))
}

match_infiles<-function(in_dir){
  print(list.files(in_dir, pattern="*.csv$"))
}

match_infiles(".")

meta_file <- "craigslist-bc-sublets-data-mar.csv"
html_file <- "craigslist-sublet-data-bc-html-mar.csv"
# harmari_craigslist_parsing(html_file, meta_file)
