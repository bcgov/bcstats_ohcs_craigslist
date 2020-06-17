## setup.R
## usage: 
##   Rscript setup.R # might need to run with admin privilege if you get permissions error
## on Windows might need to run Rscript setup.R, Rscript run.R from system prompt within RStudio
## Notes: please install R 4.0.0, and RStudio first!


## install R packages
pkg_reqd<-c("Rcpp", "reticulate")
to_install<-pkg_reqd[!(pkg_reqd %in% installed.packages()[,"Package"])]
if(length(to_install)){
  print(paste("install.packages(", to_install, ")", sep=""))
  install.packages(to_install)
}
cat("* package check complete\n")

## install miniconda / python if necessary
library(reticulate)
py_config()
## conda_create("r-reticulate") ## think py_config() does this automatically
## conda_activate("r-reticulate") ## think py_config() does this automatically too
cat("* Miniconda check complete\n")

## install Python packages
## conda_list() ## could use this for debugging
use_condaenv("r-reticulate")
conda_install("r-reticulate", "bs4") ## instead of py_install("bs4")
conda_install("r-reticulate", "html5lib") ## instead of py_install("html5lib")
conda_install("r-reticulate", "lxml") ## instead of py_install("lxml")
cat("* setup.R complete\n")

## 
## system("conda config --set channel_priority false")
## system("conda config --set auto_update_conda false")