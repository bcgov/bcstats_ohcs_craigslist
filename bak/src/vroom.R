# Rscript vroom.R [input csv file name]
library(vroom)
library(tictoc)
args = commandArgs(trailingOnly=TRUE)

if(length(args)==0){
  stop("vroom.R [input csv file name]");
}
fn <- args[1]

# vroom parameters
VROOM_THREADS = 4
VROOM_SHOW_PROGRESS = TRUE

tic()
x <- vroom(fn, delim=",", altrep = TRUE)
a <- head(x)
print(a)
toc()
