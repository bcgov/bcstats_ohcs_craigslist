err <- function(msg){
  cat(paste("Error:", msg, "\n", sep=""))
  quit()
}

# include other files if their member functions not yet def'd
for(f in Sys.glob("*.R")){
  if(f != parent.frame(2)$ofile && !(f %in% c("run.R", "setup.R"))){
    if(!exists(strsplit(f, "\\.")[[1]][1], inherits=TRUE)) source(f)
  }
}
