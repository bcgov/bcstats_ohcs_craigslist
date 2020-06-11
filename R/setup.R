## setup.R
## usage windows:
## run at cmd.exe! Possibly may need to run as administrator
## cmd Rscript setup.R

## usage mac/linux:
## Rscript setup.R # don't run as sudo: need to enter sudo password if prompted

## install R stuff
pkg_reqd<-c("Rcpp", "reticulate")
to_install<-pkg_reqd[!(pkg_reqd %in% installed.packages()[,"Package"])]
if(length(to_install)){
  print(paste("install.packages(", to_install, ")", sep=""))
  install.packages(to_install)
}
cat("* package check complete\n")
library(reticulate)
if(Sys.info()[[1]] == "Darwin"){
  install_miniconda(path = miniconda_path(), update = TRUE, force = FALSE)
}
else if(Sys.info()[[1]] == "Linux"){
  print(system("which anaconda", intern=TRUE))
  if(file.exists(Sys.which("anaconda")[[1]]) != TRUE){
    cat("anaconda not found\n")
    system("sudo apt install curl")
    if(!file.exists("conda.sh")){
      download.file("https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh", "conda.sh", method="curl")
    }
    system("chmod 755 conda.sh")
    system("./conda.sh -u")
    Sys.setenv(BASH_ENV="~/.bashrc")
    if(file.exists(Sys.which("anaconda")[[1]]) != TRUE){
      cat("Error: can't find conda\n")
      quit()
    }
  }
}
else{
  # look for r-reticulate environment in miniconda
  # if the environment doesn't exist, and the user hasn't requested a separate
  # environment, then we'll prompt for installation of miniconda
  miniconda <- miniconda_conda()
  if (!file.exists(miniconda)) {

    can_install_miniconda <-
    interactive() &&
    length(python_versions) == 0 &&
    miniconda_enabled() &&
    miniconda_installable()

    if (can_install_miniconda)
    miniconda_install_prompt()

  }

  # if the earlier branch installed miniconda, it may exist now -- if so,
  # try to activate it
  if (file.exists(miniconda)) {

    # create the conda environment if necessary
    envpath <- miniconda_python_envpath()
    if (!file.exists(envpath)) {
      python <- miniconda_python_package()
      conda_create(envpath, packages = c(python, "numpy"), conda = miniconda)
    }

    # bind to it
    miniconda_python <- conda_python(envpath, conda = miniconda)
    config <- python_config(miniconda_python, NULL, miniconda_python) # return(config)
  }
}

cat("* OS check complete\n")

## install Python stuff
conda_list()
conda_create("r-reticulate") # conda_activate("r-reticulate")
use_condaenv("r-reticulate")
conda_install("r-reticulate", "bs4") # py_install("bs4")
conda_install("r-reticulate", "html5lib") # py_install("html5lib")
conda_install("r-reticulate", "lxml") # py_install("lxml")
cat("* python check complete\n")
cat("* setup.R complete\n")