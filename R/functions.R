# Copyright 2020 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


## source a c++ function
src<-function(x){
  cat(paste("src(", x, ")\n", sep=""))
  Rcpp::sourceCpp(x, cacheDir='tmp')
}

test_csv_cat<-function(){
  print(file.path("test", "A.csv"))
  csv_cat(c(file.path("test", "A.csv"),
            file.path("test", "B.csv"),
            file.path("test", "C.csv")))

  x <- read.csv(file.path("test", "C.csv"), header=TRUE)
  for(i in 0: 7){
    a <- ceiling((i + 1)/ 2)
    b <- b <- 1 + mod(i, 2)
    insist(x[a, b] == i + 1)
  }
}


mkdir<-function(fn){
  dir.create(fn, showWarnings = FALSE)
}


chunks<-function(str, chunk_len){
  s<-str
  s<-gsub("[.]", "-", s)
  x<-strsplit(s, "-")
  for(k in seq_along(x[[1]])){
    x[[1]][k] <- substr(x[[1]][k], 1, chunk_len)
  }
  return(x)
}

within<-function(x, s){
  find<-FALSE
  for(i in seq_along(x)){
    if(x[i] == s){
      find<-TRUE
    }
  }
  return(find)
}

rmrf<-function(d){
  unlink(d, recursive=TRUE, force=TRUE)
}

## parse craigslist data as supplied by Harmari, inc.
harmari_craigslist_parsing<-function(html_file, meta_file){
  cat("harmari_craigslist_parsing", html_file, meta_file, "\n", sep=",")

  join_file = paste0(meta_file, "_join.csv")

  ## check if already extracted
  if(file.exists(join_file)){
    cat(paste0("file extracted:", join_file[1]), "\n")
    return(invisible(TRUE))
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
    stop("python not initialized")
  }
  import_from_path("py")
  source_python("py/join.py")
  source_python("py/html_parse.py")

  ## test big-data resilient csv-file concatenation, on small data ironically
  test_csv_cat()

  ## 1) index the html file
  message("1. start index step..")
  tag_file <-paste0(html_file, "_tag")
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
  to_parse <-html_parse(paste(html_file, n_records, sep=","))

  library(parallel) # Detect the number of available cores and create cluster
  cl <- parallel::makeCluster(detectCores(), type='PSOCK')

  # Parallel
  parallel::parLapply(cl, to_parse, function(x){
    library(reticulate)
    import_from_path("py")
    source_python("py/html_parse.py")
    parse_file(x)
    })
  stopCluster(cl)
  message(" 4. end parse html step")

  ## 5) join the HTML data with the metadata from the other file
  message("5. join html and metadata step..")
  join(paste(html_file, meta_file, n_records, sep=','))
  message(" 5. end join html and metadata step..")

}

match_infiles<-function(in_dir = "."){
  html<-character(0)
  meta<-character(0)
  outp<-character(0)

  src("cpp/head.cpp") # head -1 analog
  src("cpp/fileSize.cpp") # file size

  files<-list.files(in_dir, pattern="*.csv$")
  if(length(files) < 1){
    return(invisible(TRUE))
  }

  for(f in files){
    hdr<-head(f)
    if(hdr == "id,html,otherAttributes"){
      html[length(html) + 1] <- f
    }
    else if(hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng"){
      meta[length(meta) + 1] <- f
    }
    else if(hdr == "id,title,url,postDate,categoryId,cityId,location,phoneNumbers,contactName,emails,hyperlinks,price,parsedAddress,mapAddress,mapLatLng,h_price,h_bed,h_bath,h_title,h_map_accuracy,h_map_address,h_map_latitude,h_map_longitude,h_map_zoom,h_movein_date,h_notices,h_postingbody,h_attrgroup,h_mapbox,h_housing,otherAttributes"){
      outp[length(outp) +1] <- f
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


  for(i in seq_along(html)){
    s<-html[i]
    x<-chunks(s, 3)
    n_x<-length(x[[1]])
    max_j <- 0
    max_s <- 0.

    for(j in seq_along(meta)){
      score<-0
      mj <- meta[j]
      x1 <- x[[1]]
      y <- chunks(mj, 3)
      n_y <- length(y[[1]])

      for(k in seq_along(y[[1]])){
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
    stop("automatic file-matching failed")
  }
  if(length(meta_match) != length(unique(meta_match))){
    stop("automatic file-matching failed")
  }

  ## check if number of unique elements in dom and rng are same
  cat("\n\n\t** To be executed after pressing [return] (press ctrl-c to abort):\n")
  for(i in seq_along(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]
    cat(paste("harmari_craigslist_parsing(", html_file, ",", meta_file, ")\n"), sep='')
  }

  # past_file_names = c('craigslist-bc-sublets-html-jun.csv', 'craigslist-bc-sublets-data-jun.csv', 'craigslist-bc-apartment-html-jun.csv', 'craigslist-bc-apartment-data-jun.csv', 'craigslist-apa-data-bc-html-mar.csv', 'craigslist-bc-apartment-data-mar.csv', 'craigslist-bc-sublets-data-mar.csv', 'craigslist-sublet-data-bc-html-mar.csv', 'craigslist-apa-data-bc.csv', 'craigslist-sublet-data-bc.csv', 'craigslist-apa-data-bc-html-othermeta.csv', 'craigslist-sublet-data-bc-html-othermeta.csv', 'craigslist-apa-data-bc-html-jan.csv', 'craigslist-apa-data-bc-html-sep.csv', 'craigslist-bc-apa-data-jan.csv', 'craigslist-sublet-data-bc-html-jan.csv', 'craigslist-bc-sublet-data-sep.csv', 'craigslist-bc-sublet-data-jan.csv', 'craigslist-bc-apa-data-sep.csv', 'craigslist-sublet-data-bc-html-sep.csv', 'craigslist-bc-apartment-data-apr.csv', 'craigslist-bc-sublets-data-apr.csv', 'craigslist-sublet-data-bc-html-apr.csv', 'craigslist-apa-data-bc-html-apr.csv', 'craigslist-bc-apartment-data-may.csv', 'craigslist-bc-sublets-data-may.csv', 'craigslist-bc-apartment-html-may.csv', 'craigslist-bc-sublets-html-may.csv')

  # past_file_sizes = c(18627692, 190242, 657825017, 6866935, 1313723416, 14167108, 540821, 337123080, 301100188, 15806712, 22868906488, 1207390218, 3277267614, 1913701273, 35371689, 115374402, 727855, 1196955, 21663494, 65148136, 6931814, 218584, 308603553, 648129837, 8114544, 179446, 763264057, 17573827)

  past_file_names = c('2020-craigslist-bc-apartment-data-jul.csv', '2020-craigslist-bc-apartment-html-jul.csv', '2020-craigslist-bc-sublets-data-jul.csv', '2020-craigslist-bc-sublets-html-jul.csv', 'craigslist-bc-sublets-html-jun.csv', 'craigslist-bc-sublets-data-jun.csv', 'craigslist-bc-apartment-html-jun.csv', 'craigslist-bc-apartment-data-jun.csv', 'craigslist-apa-data-bc-html-mar.csv', 'craigslist-bc-apartment-data-mar.csv', 'craigslist-bc-sublets-data-mar.csv', 'craigslist-sublet-data-bc-html-mar.csv', 'craigslist-apa-data-bc.csv', 'craigslist-sublet-data-bc.csv', 'craigslist-apa-data-bc-html-othermeta.csv', 'craigslist-sublet-data-bc-html-othermeta.csv', 'craigslist-apa-data-bc-html-jan.csv', 'craigslist-apa-data-bc-html-sep.csv', 'craigslist-bc-apa-data-jan.csv', 'craigslist-sublet-data-bc-html-jan.csv', 'craigslist-bc-sublet-data-sep.csv', 'craigslist-bc-sublet-data-jan.csv', 'craigslist-bc-apa-data-sep.csv', 'craigslist-sublet-data-bc-html-sep.csv', 'craigslist-bc-apartment-data-apr.csv', 'craigslist-bc-sublets-data-apr.csv', 'craigslist-sublet-data-bc-html-apr.csv', 'craigslist-apa-data-bc-html-apr.csv', 'craigslist-bc-apartment-data-may.csv', 'craigslist-bc-sublets-data-may.csv', 'craigslist-bc-apartment-html-may.csv', 'craigslist-bc-sublets-html-may.csv')
  
  past_file_sizes = c(8091843, 774760440, 223473, 21837717, 18627692, 190242, 657825017, 6866935, 1313723416, 14167108, 540821, 337123080, 301100188, 15806712, 22868906488, 1207390218, 3277267614, 1913701273, 35371689, 115374402, 727855, 1196955, 21663494, 65148136, 6931814, 218584, 308603553, 648129837, 8114544, 179446, 763264057, 17573827)
    
  ## check expected file sizes
  sink("data_file_sizes.txt")
  cat("meta_file,html_file,meta_file_size,html_file_size")
  sink()
  for(i in seq_along(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]
    mfs <- fileSize(c(meta_file))
    hfs <- fileSize(c(html_file))

    mfi <- first_idx(meta_file, past_file_names)
    hfi <- first_idx(html_file, past_file_names)
      
    if(mfs != past_file_sizes[[mfi]]) stop("file size mismatch")
    if(hfs != past_file_sizes[[hfi]]) stop("file size mismatch")

    sink("data_file_sizes.txt", append=TRUE)
    cat(paste("\n", meta_file, html_file, mfs, hfs, sep=","))
    sink()
  }

  ## cat("N.B. if you wish to abort, please press ctrl-c (and then return). If not, please just press return.\n")
  ## wait_return()

  join_files = character(0)
  for(i in seq_along(html_match)){
    meta_file <- meta_match[i]
    html_file <- html_match[i]

    ## clear intermediary folders before proceeding
    rmrf("html")
    rmrf("otherAttributes")
    rmrf("parsed")

    ## n.b. if join_file already exists, this iteration of harmari_craigslist_parsing will return without performing any action
    join_file = paste(meta_file, "_join.csv", sep="")
    harmari_craigslist_parsing(html_file, meta_file)

    join_files[length(join_files) + 1] <- join_file

    join_null_file <- paste(join_file, "_null.csv", sep="")

    # python3 py/select_null.py craigslist-apa-data-bc.csv_join.csv postDate > craigslist-apa-data-bc.csv_join.csv_null.csv
    cmd <- paste("python3", "py/select_null.py", join_file, "postDate >", join_null_file, sep=" ")
    system(cmd)
  }

  ## 6) concatenate csv files together
  message("6. concatenate csv files together")
  src("cpp/csv_cat.cpp")
  join_files[length(join_files) + 1] <- "merge.csv"
  csv_cat(join_files)
  message(" 6. end concatenate csv files together")
  message("output file: merge.csv")
  cat("done\n")
  ## wait_return()

  ## 7. find unique elements-- big data resilient (unique.cpp)
}
