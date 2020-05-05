## setup.R 
## usage windows:
## run with administrator at cmd.exe!
## cmd Rscript setup.R 

## usage mac/linux:
##   sudo Rscript setup.R 

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

library(reticulate) # just this one?

if(Sys.info()[[1]] == "Linux"){
  if(length(Sys.which("anaconda")) < 1){
    system("sudo apt install curl")
    if(!file.exists("conda.sh")){
      download.file("https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh", "conda.sh", method="curl")
    }
    system("chmod 755 conda.sh")
    system("./conda.sh")
  }
}

## install Python stuff
conda_list()
conda_create("r-reticulate") # conda_activate("r-reticulate")
use_condaenv("r-reticulate")
cat("checking that python libraries are installed..\n")
conda_install("r-reticulate", "bs4") # py_install("bs4")
conda_install("r-reticulate", "html5lib") # py_install("html5lib")
conda_install("r-reticulate", "lxml") # py_install("lxml")
cat("got past the python libraries installation\n")
cat("setup.R complete\n")
