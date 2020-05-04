wait_return <- function(){
  cat('press [return] to continue')
  return(scan("stdin", character(), nlines=1, quiet=TRUE))
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
