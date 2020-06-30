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



## Rscript run.R ## todo: check for nonunique records
## .libPaths() to find deps loc
## instructions: open script in RStudio,
##    session-> set working directory --> to Source location
## Note: when you run this script, if you are prompted to download additional tools to build R packages, please accept
## Please run setup.R first
## may need to run as administrator, the first time

# include other files if their member functions not yet def'd
my_fn <- parent.frame(2)$ofile
scripts <- c("run.R", "setup.R", "functions.R")
for(f in Sys.glob("*.R")){
  if(! is.null(my_fn)) if(f == my_fn) next
  if(!(f %in% scripts)){
    if(!exists(strsplit(f, "\\.")[[1]][1], inherits=TRUE)) source(f)
  }
}

# Load packages and condaenv
library(Rcpp)
library(reticulate)
use_condaenv("r-reticulate")
p_sep <- .Platform$file.sep # platform specific path sep

# Actually run the processing script
match_infiles()
