nothing<-function(){
  print("nothing function()")
}

# include other files if the function in them with same name, not yet defined
files <- Sys.glob("*.R")
my_fn <- parent.frame(2)$ofile
scripts <- c("run.R", "setup.R")
for(f in files){
  if(f != my_fn && !(f %in% scripts)){
    fn <- strsplit(f, "\\.")[[1]][1] # primary function name
    if(!exists(fn, inherits=TRUE)){
      source(f)
    }
  }
}
