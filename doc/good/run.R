# 20200717 how to run a python function in parallel, inside R

library(parallel) # Detect the number of available cores, create "cluster"
cl <- parallel::makeCluster(detectCores(), type='PSOCK')

# Parallel
x <- c(1, 2, 3, 4);

y <-parallel::parLapply(cl, x,
	function(z){
  	library(reticulate)
  	source_python("python_function.py")
  	return(python_function(z))
	}
)
stopCluster(cl)
print(y) # show the results
