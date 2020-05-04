err <- function(msg){
  cat(paste("Error:", msg, "\n", sep=""))
  quit()
}

first_idx <- function(e, x){
  ret <- NULL
  for(i in 1:length(x)){
    if(x[i] == e){
      ret <- i
    }
  }
  return(ret)
}


# include other files if their member functions not yet def'd
c("run.R", "setup.R")
for(f in Sys.glob("*.R")){
  if(f != parent.frame(2)$ofile && !(f %in% scripts)){
    if(!exists(strsplit(f, "\\.")[[1]][1], inherits=TRUE)) source(f)
  }
}
