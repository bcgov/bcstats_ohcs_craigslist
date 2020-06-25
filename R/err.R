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
