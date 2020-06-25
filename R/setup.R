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



## setup.R
## usage:
##   Rscript setup.R # might need to run with admin privilege if you get permissions error
## on Windows might need to run Rscript setup.R, Rscript run.R from system prompt within RStudio
## Notes: please install R 4.0.0, and RStudio first!


## Check if packages are installed
requireNamespace("Rcpp")
requireNamespace("reticulate")
cat("* package check complete\n")

## install miniconda / python if necessary
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
