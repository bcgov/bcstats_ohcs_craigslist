# how NOT to run a python function in parallel, from R
library(parallel) # Detect the number of available cores, create "cluster"
cl <- parallel::makeCluster(detectCores(), type='PSOCK')

# Parallel
x <- c(1, 2, 3, 4);

library(reticulate)
source_python("python_function.py")
python_function(5)

y <-parallel::parLapply(cl, x,
	function(z){
  	return(python_function(z))
	}
)
stopCluster(cl)
print(y) # show the results
