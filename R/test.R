# 0) track existing blobs
# 1) need to search for / match new blobs
# 2) need to search for / match blobs that have already been produced
# 3) check that sublet vs apa are distinguished in the merged product
# 4) retain only non-redundant records
# 5) remove intermed. files, after "join"

args = commandArgs(trailingOnly=TRUE)
if(length(args)==0){
  # stop("test.R [input directory name]");
}

library(Rcpp) # install.packages("Rcpp")
library(reticulate) # install.packages("reticulate")

p_sep <- .Platform$file.sep # platform specific path separator

wait_return <- function(){
  cat('press [return] to continue')
  return(scan("stdin", character(), nlines=1, quiet=TRUE))
  # b <- scan("stdin", character(), n=1)
}

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
  join_file = paste(meta_file, "_join.csv", sep="")

  # check if already extracted
  if(file.exists(join_file)){
    cat(paste("file extracted:", join_file[1], sep=""), "\n")
    return(0)
  }

  # c++ functionality
  src("cpp/lc.cpp") # wc -l analog to avoid R.utils dep
  src("cpp/head.cpp") # head -1 analog
  src("cpp/insist.cpp") # assertion
  src("cpp/extract.cpp")
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
  extract(html_file) # HTML file extraction

  # 3) count records from "meta" file
  n_records <-lc(meta_file)

  # 4) parse the html files using multithreading
  mkdir("parsed")
  html_parse(paste(html_file, n_records, sep=","))

  # 5) join the HTML data with the metadata from the other file
  join(paste(html_file, meta_file, n_records, sep=','))
}

match_infiles<-function(in_dir){
  html<-character(0)
  meta<-character(0)
  outp<-character(0)

  src("cpp/head.cpp") # head -1 analog
  files<-list.files(in_dir, pattern="*.csv$")
  for(f in files){
    hdr<-head(f)
    if(hdr == "id,html,otherAttributes"){
      html[length(html) + 1]<-f
    }
    else if(hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng"){
      meta[length(meta) + 1]<-f
    }
    else if(hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng,h_price,h_bed,h_bath,h_title,h_map_accuracy,h_map_address,h_map_latitude,h_map_longitude,h_map_zoom,h_movein_date,h_notices,h_postingbody,h_attrgroup,h_mapbox,h_housing,otherAttributes"){
      outp[length(outp) +1]<-f
    }
    else{
      cat("Warning: Unrecognized file: ", f, "\n")
      print(cat(f, " ", hdr, "\n"))
    }
  }
  # files are now categorized

  cat("html-type files:", html, "\n") # cat is for printing. paste() is for catting!
  cat("meta-type files:", meta, "\n")
  cat("output files:", outp, "\n")

  html_match<-character(0)
  meta_match<-character(0)

  chunks<-function(str){
    s<-str
    s<-gsub("[.]", "-", s)
    return(strsplit(s, "-"))
  }

  within<-function(x, s){
    find<-FALSE
    for(i in 1:length(x)){
      if(x[i] == s){
        find<-TRUE
      }
    }
    return(find)
  }

  # could hypothetically match on ID but we'll match on name and warn

  # at this point, need to restrict string chunks to length 3, if not numeric

  # might also need to adapt metric to handle potentially varying number of chunks (try it on all data files with original names, and see if it works!!!)
  for(i in 1:length(html)){
    s<-html[i]
    x<-chunks(s)
    max_j <- 0
    max_s <- 0.
    
    for(j in 1:length(meta)){
      score<-0
      mj <- meta[j]
      x1 <- x[[1]]
      y <- chunks(mj)

      for(k in 1:length(y[[1]])){
        if(within(x1, y[[1]][k])){
          score <- score + 1
        }
      }

      if(score > max_s){
	max_j <- j
        max_s <- score 
      }
    }
    html_match[length(html_match) + 1] <- html[i]
    meta_match[length(meta_match) + 1] <- meta[max_j]
  }

  # *** at this point, need to flag if the correspondence is not 1-1

  # check if number of unique elements in dom and rng are same
  cat("\n\n\t** To be executed after pressing [return] (press ctrl-c to abort):\n")
  for(i in 1:length(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]
    cat(paste("harmari_craigslist_parsing(", html_file, ",", meta_file, ")\n"), sep='')
  }
  wait_return()

  for(i in 1:length(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]
    harmari_craigslist_parsing(html_file, meta_file)
  }


  # when the program runs, it generates a new file: meta_file_name + "_join.csv"
  # therefore, a non-identified output file, is a concatenated file


  # csv_slice: extract? if matching on ID
  # concatenate all-- big data resilient
  # find unique elements-- big data resilient (unique.cpp)
}


match_infiles(".")
