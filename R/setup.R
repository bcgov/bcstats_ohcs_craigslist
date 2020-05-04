## setup.R 
## usage mac/linux:
##   sudo Rscript setup.R 
## usage windows:
## run with administrator at cmd.exe!
## cmd Rscript setup.R 

## install R stuff
pkg_reqd<-c("Rcpp", "reticulate")
to_install<-pkg_reqd[!(pkg_reqd %in% installed.packages()[,"Package"])]
if(length(to_install)){
  cat("required packages to install:\n")
  print(to_install)
  cat("press return to install required packages:\n")
  cat("** NOTE: if this doesn't work, please re-run the script with administrator / super-user privileges..\n")
  install.packages(to_install)
}

library(reticulate)

## install Python stuff
conda_create("r-reticulate") # conda_activate("r-reticulate")
use_condaenv("r-reticulate")
cat("checking that python libraries are installed..\n")
conda_install("r-reticulate", "bs4") # py_install("bs4")
conda_install("r-reticulate", "html5lib") # py_install("html5lib")
conda_install("r-reticulate", "lxml") # py_install("lxml")
cat("got past the python libraries installation\n")
cat("setup.R complete\n")
