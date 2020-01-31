library(vroom)
library(dplyr)
library(tictoc)

VROOM_THREADS = 4
VROOM_SHOW_PROGRESS = TRUE

tic()
file <- "craigslist-apa-and-sublet-data-bc.csv_merge.csv";
x <- vroom(file, delim=",", altrep = TRUE)
a <- head(x)
print(a)
toc()
