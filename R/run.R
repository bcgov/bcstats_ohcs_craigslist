## Rscript run.R ## todo: check for nonunique records

# include other files if their member functions not yet def'd
my_fn <- parent.frame(2)$ofile
scripts <- c("run.R", "setup.R")
for(f in Sys.glob("*.R")){
  if(! is.null(my_fn)) if(f == my_fn) next
  if(!(f %in% scripts)){
    if(!exists(strsplit(f, "\\.")[[1]][1], inherits=TRUE)) source(f)
  }
}

library(Rcpp)
library(reticulate)
use_condaenv("r-reticulate")
p_sep <- .Platform$file.sep # platform specific path sep

rmrf<-function(d){
  cat(paste("rm -rf ", d, "\n", sep=""))
  unlink(d, recursive=TRUE, force=TRUE)
}

mod<-function(x, m){
  return(x - floor(x / m) * m)
}

## thanks to Sam Albers and Craig Hutton for helping solve this
pr<-function(x){
  print(paste(paste(deparse(substitute(x)), "="), x))
}

## source a c++ function
src<-function(x){
  cat(paste("src(\"", x, "\")\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

## parse craigslist data as supplied by Harmari, inc.
harmari_craigslist_parsing<-function(html_file, meta_file){
  cat("harmari_craigslist_parsing", html_file, meta_file, "\n", sep=",")

  join_file = paste(meta_file, "_join.csv", sep="")

  ## check if already extracted
  if(file.exists(join_file)){
    cat(paste("file extracted:", join_file[1], sep=""), "\n")
    return(0)
  }

  ## c++ functionality
  src("cpp/lc.cpp") # wc -l analog to avoid R.utils dep
  src("cpp/head.cpp") # head -1 analog
  src("cpp/insist.cpp") # assertion
  src("cpp/extract.cpp")
  src("cpp/csv_cat.cpp") # merge arb. large csv: assert headers match, keep first hdr
  src("cpp/find_start.cpp") # index an HTML nested in csv, find <HTML> byte start locs

  ## python functionality
  cat("Note: if prompted to install Miniconda, please say yes!\n")
  py_discover_config()
  py_available(initialize=TRUE)
  if(!py_available()){
    err("python not initialized")
  }
  import_from_path("py")
  source_python("py/join.py")
  source_python("py/html_parse.py")

  ## test big-data resilient csv-file concatenation, on small data ironically
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

  ## 1) index the html file
  message("1. start index step..")
  tag_file <-paste(html_file, "_tag", sep="")
  if(!file.exists(tag_file)){
    find_start(html_file)
  }
  message(" 1. end index step..")

  ## 2) extract html files
  message("2. start extract step..")
  mkdir("html")
  mkdir("otherAttributes")

  extract(html_file) ## HTML file extraction
  message(" 2. end extract step..")

  ## 3) count records from "meta" file
  message("3. count records step..")
  n_records <-lc(meta_file)
  message(" 3. end count records step..")

  ## 4) parse the html files using multithreading
  message("4. parse html step..")
  mkdir("parsed")
  html_parse(paste(html_file, n_records, sep=","))
  message(" 4. end parse html step")

  ## 5) join the HTML data with the metadata from the other file
  message("5. join html and metadata step..")
  join(paste(html_file, meta_file, n_records, sep=','))
  message(" 5. end join html and metadata step..")

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
  ## files are now categorized

  cat("html-type files:", html, "\n") # cat is for printing. paste() is for catting!
  cat("meta-type files:", meta, "\n")
  cat("output files:", outp, "\n")

  html_match<-character(0)
  meta_match<-character(0)

  chunks<-function(str, chunk_len){
    s<-str
    s<-gsub("[.]", "-", s)
    x<-strsplit(s, "-")
    for(k in 1:length(x[[1]])){
      x[[1]][k] <- substr(x[[1]][k], 1, chunk_len)
    }
    return(x)
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

  for(i in 1:length(html)){
    s<-html[i]
    x<-chunks(s, 3)
    n_x<-length(x[[1]])
    max_j <- 0
    max_s <- 0.

    for(j in 1:length(meta)){
      score<-0
      mj <- meta[j]
      x1 <- x[[1]]
      y <- chunks(mj, 3)
      n_y <- length(y[[1]])

      for(k in 1:length(y[[1]])){
        if(within(x1, y[[1]][k])){
          score <- score + 1
        }
      }

      ## scale score with respect to length of strings
      score <- 2. * score / (n_x + n_y)

      if(score > max_s){
        max_j <- j
        max_s <- score
      }
      cat(paste("**score:", score, " html: ", html[i], " meta: ", meta[j], "\n", sep=""))
    }
    cat(paste("->score:", score, " html: ", html[i], " meta: ", meta[max_j], "\n", sep=""))
    html_match[length(html_match) + 1] <- html[i]
    meta_match[length(meta_match) + 1] <- meta[max_j]
  }

  ## error if the correspondence is not 1-1
  if(length(html_match) != length(unique(html_match))){
    err("automatic file-matching failed")
  }
  if(length(meta_match) != length(unique(meta_match))){
    err("automatic file-matching failed")
  }

  ## check if number of unique elements in dom and rng are same
  cat("\n\n\t** To be executed after pressing [return] (press ctrl-c to abort):\n")
  for(i in 1:length(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]
    cat(paste("harmari_craigslist_parsing(", html_file, ",", meta_file, ")\n"), sep='')
  }
  cat("N.B. if you wish to abort, please press ctrl-c (and then return). If not, please just press return.\n")

  wait_return()

  join_files = character(0)

  for(i in 1:length(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]

    ## clear intermediary folders before proceeding
    rmrf<-function(d){
      unlink(d, recursive=TRUE, force=TRUE)
    }
    rmrf("html")
    rmrf("otherAttributes")
    rmrf("parsed")

    ## n.b. if join_file already exists, this iteration of harmari_craigslist_parsing will return without performing any action
    join_file = paste(meta_file, "_join.csv", sep="")
    harmari_craigslist_parsing(html_file, meta_file)

    join_files[length(join_files) + 1] <- join_file
  }

  ## 6) concatenate csv files together
  message("6. concatenate csv files together")
  src("cpp/csv_cat.cpp")
  join_files[length(join_files) + 1] <- "merge.csv"
  csv_cat(join_files)
  message(" 6. end concatenate csv files together")
  message("output file: merge.csv")
  cat("done\n")
  wait_return()

  ## 7. find unique elements-- big data resilient (unique.cpp)
}

match_infiles(".")