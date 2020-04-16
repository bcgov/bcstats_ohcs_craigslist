# Rscript vroom.R [input csv file name]
library(vroom)
library(tictoc)

if(length(args)==0){
  stop("vroom.R [input csv file name]");
}

# parameters
VROOM_THREADS = 4
VROOM_SHOW_PROGRESS = TRUE

tic()
x <- vroom(args[1], delim=",", altrep = TRUE)
a <- head(x)
print(a)
toc()
